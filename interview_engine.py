import os
import json
import time
import urllib.request
import urllib.error
from typing import Dict, Any, Optional
from persona_schema import Persona, InterviewResponse
from guardrail_box import run_deterministic_precheck, build_guardrailed_system_prompt

def load_env_key() -> str:
    """
    Loads API key from environment variable or local .env file.
    """
    key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if key:
        return key.strip().strip("'").strip('"')
    
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k_str = k.strip()
                    val_str = v.strip().strip("'").strip('"')
                    if k_str in ["OPENROUTER_API_KEY", "GEMINI_API_KEY"]:
                        os.environ[k_str] = val_str
                        return val_str
    return ""

def clean_json_response(raw_text: str) -> Dict[str, Any]:
    """
    Strips markdown fences and parses clean JSON dictionary.
    """
    text = raw_text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    return json.loads(text)

def call_openrouter_api(api_key: str, system_prompt: str, user_question: str, model_name: str = None) -> Dict[str, Any]:
    """
    Calls OpenRouter API chat completion endpoint with automatic fallback across allowed fast models.
    """
    api_key = api_key.strip().strip("'").strip('"')
    
    allowed_models = [
        "liquid/lfm-2.5-2.6b:free",
        "nex-agi/nex-n2.5-pro:free",
        "nex-agi/nex-n2.5-mini:free",
        "inclusionai/ling-3.0-flash-sante:free",
        "inclusionai/ling-3.0-flash-fin:free",
        "qwen/qwen3.8-27b:free",
        "google/gemma-4-31b-it:free"
    ]
    
    candidate_models = []
    if model_name:
        candidate_models.append(model_name)
    for m in allowed_models:
        if m not in candidate_models:
            candidate_models.append(m)

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://github.com/aniket-thakare-pm/synthetic-user-simulation-engine",
        "X-Title": "Synthetic User Simulation Engine",
        "Content-Type": "application/json"
    }

    last_error = None
    for model in candidate_models:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"User Interview Question:\n'{user_question}'\n\nProvide your response ONLY as a valid JSON object matching the requested schema."}
            ],
            "temperature": 0.3,
            "response_format": {"type": "json_object"}
        }

        data = json.dumps(payload).encode("utf-8")
        max_retries = 3
        for attempt in range(max_retries):
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            try:
                with urllib.request.urlopen(req, timeout=12) as resp:
                    resp_bytes = resp.read()
                    resp_data = json.loads(resp_bytes.decode("utf-8"))
                    
                    choices = resp_data.get("choices", [])
                    if not choices:
                        raise ValueError(f"OpenRouter API returned no response choices for model '{model}'.")
                    
                    text_content = choices[0]["message"]["content"]
                    return clean_json_response(text_content)
            except urllib.error.HTTPError as e:
                error_body = e.read().decode("utf-8")
                last_error = f"OpenRouter API Error ({e.code}) for model '{model}': {error_body}"
                if e.code in (429, 502, 503, 504):
                    if attempt < max_retries - 1:
                        time.sleep(1.5 * (attempt + 1))
                        continue
                    else:
                        break
                else:
                    break
            except (urllib.error.URLError, TimeoutError) as e:
                last_error = f"Network Timeout Error ({str(e)}) on model '{model}'"
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                else:
                    break
            except Exception as e:
                last_error = str(e)
                break

    raise RuntimeError(f"All OpenRouter model attempts failed. Last error: {last_error}")

def call_gemini_api(api_key: str, system_prompt: str, user_question: str, model_name: str = None) -> Dict[str, Any]:
    """
    Fallback Gemini REST API endpoint call.
    """
    api_key = api_key.strip().strip("'").strip('"')
    candidate_models = ["gemini-2.5-flash", "gemini-3.6-flash", "gemini-3.5-flash"]
    if model_name:
        candidate_models.insert(0, model_name)
        
    last_error = None
    for model in candidate_models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        payload = {
            "system_instruction": {"parts": [{"text": system_prompt}]},
            "contents": [{"role": "user", "parts": [{"text": f"User Interview Question:\n'{user_question}'\n\nProvide your response in JSON format."}]}],
            "generationConfig": {"temperature": 0.3, "responseMimeType": "application/json"}
        }
        headers = {"Content-Type": "application/json"}
        data = json.dumps(payload).encode("utf-8")
        
        for attempt in range(3):
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            try:
                with urllib.request.urlopen(req, timeout=12) as resp:
                    resp_bytes = resp.read()
                    resp_data = json.loads(resp_bytes.decode("utf-8"))
                    candidates = resp_data.get("candidates", [])
                    if not candidates:
                        raise ValueError("Gemini returned no response candidates.")
                    text_content = candidates[0]["content"]["parts"][0]["text"]
                    return clean_json_response(text_content)
            except Exception as e:
                last_error = str(e)
                time.sleep(1)
                break
    raise RuntimeError(f"All Gemini API attempts failed: {last_error}")

def call_llm_api(api_key: str, system_prompt: str, user_question: str, model_name: str = None) -> Dict[str, Any]:
    """
    Routes to OpenRouter or Gemini API based on key format.
    """
    if not api_key:
        api_key = load_env_key()
    
    if api_key.startswith("sk-or-"):
        return call_openrouter_api(api_key, system_prompt, user_question, model_name=model_name)
    else:
        return call_gemini_api(api_key, system_prompt, user_question, model_name=model_name)

def interview_persona_stateless(persona: Persona, question_text: str, api_key: str = None) -> InterviewResponse:
    """
    Executes a single-turn, stateless interview run for a guardrailed persona via OpenRouter/Gemini LLM.
    """
    if not api_key:
        api_key = load_env_key()
        
    auto_rejected, precheck_reason = run_deterministic_precheck(persona, question_text)
    system_prompt = build_guardrailed_system_prompt(persona, precheck_reason=precheck_reason)
    json_output = call_llm_api(api_key, system_prompt, question_text)
    
    maj_pct = json_output.get("majority_percent", 70)
    min_pct = json_output.get("minority_percent", 30)
    
    try:
        maj_pct = int(maj_pct)
        min_pct = int(min_pct)
    except (ValueError, TypeError):
        maj_pct, min_pct = 70, 30
        
    action_dir = str(json_output.get("primary_action_direction", "CANCEL")).upper().strip()
    churn_pct = json_output.get("churn_or_rejection_percent")
    
    if churn_pct is not None:
        try:
            churn_pct = int(churn_pct)
        except (ValueError, TypeError):
            churn_pct = None

    if churn_pct is None:
        if any(k in action_dir for k in ["KEEP", "ACCEPT", "ADOPT", "RETAIN", "STAY"]):
            churn_pct = 100 - maj_pct
        else:
            churn_pct = maj_pct

    if auto_rejected:
        maj_pct, min_pct = 100, 0
        action_dir = "REJECT"
        churn_pct = 100

    return InterviewResponse(
        persona_id=persona.id,
        persona_name=persona.name,
        persona_role=persona.demographics.occupation,
        majority_percent=maj_pct,
        minority_percent=min_pct,
        primary_action_direction=action_dir,
        churn_or_rejection_percent=churn_pct,
        majority_response=json_output.get("majority_response", json_output.get("response_text", "Primary approach.")),
        minority_exception=json_output.get("minority_exception", "Conditional exception or alternative approach."),
        response_text=json_output.get("response_text", "No response provided."),
        primary_objection=json_output.get("primary_objection", precheck_reason if auto_rejected else None),
        deterministic_rule_triggered=precheck_reason,
        population_weight=getattr(persona, "population_weight", 0.20)
    )
