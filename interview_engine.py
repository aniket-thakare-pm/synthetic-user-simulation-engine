import os
import json
import time
import urllib.request
import urllib.error
from typing import Dict, Any
from persona_schema import Persona, InterviewResponse
from guardrail_box import run_deterministic_precheck, build_guardrailed_system_prompt

def get_available_gemini_models(api_key: str) -> list:
    """
    Dynamically queries the Gemini API to list models.
    Silently returns empty list if ListModels is restricted for the API key.
    """
    api_key = api_key.strip().strip("'").strip('"')
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            models = []
            for m in data.get("models", []):
                if "generateContent" in m.get("supportedGenerationMethods", []):
                    name = m.get("name", "").replace("models/", "")
                    models.append(name)
            return models
    except Exception:
        return []

def call_gemini_api(api_key: str, system_prompt: str, user_question: str, model_name: str = None) -> Dict[str, Any]:
    """
    Calls the Gemini API directly via HTTP REST endpoint.
    Includes exponential backoff retries and model fallback on 503/429 errors.
    """
    api_key = api_key.strip().strip("'").strip('"')
    available_models = get_available_gemini_models(api_key)
    
    dashboard_models = [
        "gemini-1.5-flash",
        "gemini-2.0-flash",
        "gemini-2.5-flash",
        "gemini-3.6-flash",
        "gemini-3.5-flash",
        "gemini-2.5-flash-lite"
    ]
    
    candidate_models = []
    if model_name:
        candidate_models.append(model_name)
        
    for m in dashboard_models:
        if m not in candidate_models:
            candidate_models.append(m)
            
    for m in available_models:
        if m not in candidate_models:
            candidate_models.append(m)
        
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
        
        max_retries = 3
        for attempt in range(max_retries):
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            try:
                with urllib.request.urlopen(req) as resp:
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
                        time.sleep(2 ** attempt)
                        continue
                    else:
                        break
                elif e.code == 404:
                    break
                else:
                    raise RuntimeError(last_error)
            except Exception as e:
                last_error = str(e)
                break
            
    raise RuntimeError(f"All model attempts failed. Last error: {last_error}")

def interview_persona_stateless(persona: Persona, question_text: str, api_key: str) -> InterviewResponse:
    """
    Executes a single-turn, stateless interview run for a guardrailed persona.
    """
    auto_rejected, precheck_reason = run_deterministic_precheck(persona, question_text)
    system_prompt = build_guardrailed_system_prompt(persona, precheck_reason=precheck_reason)
    json_output = call_gemini_api(api_key, system_prompt, question_text)
    
    return InterviewResponse(
        persona_id=persona.id,
        persona_name=persona.name,
        persona_role=persona.demographics.occupation,
        response_text=json_output.get("response_text", "No response provided."),
        primary_objection=json_output.get("primary_objection", precheck_reason if auto_rejected else None),
        deterministic_rule_triggered=precheck_reason
    )
