import os
import json
import time
import urllib.request
import urllib.error
from typing import Dict, Any
from persona_schema import Persona, InterviewResponse
from guardrail_box import run_deterministic_precheck, build_guardrailed_system_prompt

import functools

@functools.lru_cache(maxsize=4)
def get_available_gemini_models(api_key: str) -> tuple:
    """
    Dynamically queries the Gemini API to list models.
    Excludes TTS, Audio, Embedding, and Image generation models.
    """
    api_key = api_key.strip().strip("'").strip('"')
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            models = []
            for m in data.get("models", []):
                name = m.get("name", "").replace("models/", "")
                name_lower = name.lower()
                if any(x in name_lower for x in ["tts", "audio", "embed", "imagen", "transcribe"]):
                    continue
                if "generateContent" in m.get("supportedGenerationMethods", []):
                    models.append(name)
            return tuple(models)
    except Exception:
        return ()

def call_gemini_api(api_key: str, system_prompt: str, user_question: str, model_name: str = None) -> Dict[str, Any]:
    """
    Calls the Gemini API directly via HTTP REST endpoint.
    Includes exponential backoff retries and model fallback on 503/429/Timeout errors.
    """
    api_key = api_key.strip().strip("'").strip('"')
    available_models = get_available_gemini_models(api_key)
    
    dashboard_models = [
        "gemini-2.5-flash",
        "gemini-flash-latest",
        "gemini-3.6-flash",
        "gemini-3.5-flash"
    ]
    
    candidate_models = []
    if model_name:
        candidate_models.append(model_name)
        
    for m in dashboard_models:
        if m in available_models and m not in candidate_models:
            candidate_models.append(m)

    if not candidate_models:
        for m in available_models:
            if m not in candidate_models and not any(x in m.lower() for x in ["tts", "audio", "embed", "imagen", "transcribe", "gemma", "lyria", "robotics", "computer-use", "antigravity", "deep-research"]):
                candidate_models.append(m)
                
    if not candidate_models:
        candidate_models = ["gemini-2.5-flash"]
        
    last_error = None
    
    for model in candidate_models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        
        payload = {
            "system_instruction": {
                "parts": [{"text": system_prompt}]
            },
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": f"User Interview Question:\n'{user_question}'\n\nProvide your response in JSON format."}]
                }
            ],
            "generationConfig": {
                "temperature": 0.3,
                "responseMimeType": "application/json"
            }
        }
        
        headers = {"Content-Type": "application/json"}
        data = json.dumps(payload).encode("utf-8")
        
        max_retries = 5
        for attempt in range(max_retries):
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            try:
                # Set explicit 15-second timeout on urlopen to prevent terminal hangs
                with urllib.request.urlopen(req, timeout=15) as resp:
                    resp_bytes = resp.read()
                    resp_data = json.loads(resp_bytes.decode("utf-8"))
                    
                    candidates = resp_data.get("candidates", [])
                    if not candidates:
                        raise ValueError(f"Gemini API returned no response candidates for model '{model}'.")
                    
                    text_content = candidates[0]["content"]["parts"][0]["text"]
                    return json.loads(text_content)
            except urllib.error.HTTPError as e:
                error_body = e.read().decode("utf-8")
                last_error = f"Gemini API HTTP Error ({e.code}) for model '{model}': {error_body}"
                
                if e.code in (503, 429):
                    if attempt < max_retries - 1:
                        # Extract suggested retryDelay if present in JSON error response
                        wait_sec = 20
                        try:
                            err_json = json.loads(error_body)
                            for d in err_json.get("error", {}).get("details", []):
                                if "retryDelay" in d:
                                    delay_str = d["retryDelay"].replace("s", "")
                                    wait_sec = max(5, int(float(delay_str)) + 2)
                        except Exception:
                            wait_sec = 20
                        time.sleep(wait_sec)
                        continue
                    else:
                        break
                elif e.code == 404:
                    break
                else:
                    raise RuntimeError(last_error)
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
            
    raise RuntimeError(f"All model attempts failed. Last error: {last_error}")

def interview_persona_stateless(persona: Persona, question_text: str, api_key: str) -> InterviewResponse:
    """
    Executes a single-turn, stateless interview run for a guardrailed persona,
    returning continuous McFadden logit probability splits, directional vectors, and macro workaround descriptions.
    """
    auto_rejected, precheck_reason = run_deterministic_precheck(persona, question_text)
    system_prompt = build_guardrailed_system_prompt(persona, precheck_reason=precheck_reason)
    json_output = call_gemini_api(api_key, system_prompt, question_text)
    
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
