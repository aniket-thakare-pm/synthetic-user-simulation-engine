"""
Engine V2.2: The Cognitive Agent Model (Option B)
- LLM evaluates Subjective Evaluated Utility (V_subj_new, V_subj_sq) with personal psychology baked in
- Python executes Direct Delta: ΔV = V_subj_new - V_subj_sq (No extra subtraction, avoiding double penalty)
- Sigmoid Sensitivity k = 0.32 (Change 3)
- Question-aligned binary polarity YES vs NO (Change 1)
- Dynamic Gating of Decision Primitives (Change 4)
"""
import math
import os
import sys
from typing import Dict, Any, Tuple

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from v2.persona_schema_v2 import PersonaV2
from v2.decision_primitives import classify_decision_primitives, get_gated_friction_warnings
from interview_engine import call_llm_api, load_env_key

def build_prompt_v2_2(persona: PersonaV2, question_text: str, stakes) -> str:
    p = persona
    rules_list = "\n".join([f"- {rule}" for rule in p.guardrail_rules]) if p.guardrail_rules else "- None"
    values_list = ", ".join(p.psychographics.core_values) if p.psychographics.core_values else "Efficiency"
    gated_warnings = get_gated_friction_warnings(stakes)

    prompt = f"""
YOU ARE NOT AN AI ASSISTANT. YOU ARE NOT HELPFUL OR EAGER TO PLEASE.
You are roleplaying strictly as {p.name}, a {p.demographics.occupation} in {p.demographics.city_tier or 'US/India'}.

=== YOUR PERSONA PROFILE ===
Name: {p.name} | Age: {p.demographics.age} | Income: {p.demographics.income_bracket}
Tech Literacy: {p.demographics.tech_literacy}/10 | Skepticism: {p.psychographics.skepticism_score}/10 | Patience: {p.psychographics.patience_score}/10
Daily Mobility: {p.capabilities.mobility} | Primary Payment: {p.capabilities.primary_payment}
Primary Frustration: "{p.psychographics.primary_pain_point}"
Core Values: {values_list}

=== COGNITIVE & BEHAVIORAL PARAMETERS ===
Status Quo Inertia: {p.psychographics.status_quo_inertia}/10 (Comfort and routine with your current habits)
Loss Aversion Multiplier: {p.psychographics.loss_aversion_bias}x (Psychological pain of losing familiar routine vs saving money)
Social Proof / Word-of-Mouth Threshold: {p.social_network.network_social_proof_threshold}/10 (How much you wait for trusted peers)
Human Recourse Need: {p.cognitive_friction.human_recourse_requirement}/10 (Need for physical human support when things fail)

=== DECISION CONTEXT ===
{gated_warnings if gated_warnings else "Standard commercial/utility decision."}

=== BEHAVIORAL RULES ===
{rules_list}

=== DIRECTIVES FOR V2.2 SUBJECTIVE EVALUATION ===
1. Respond naturally, candidly, and CONCISELY as {p.name}.
2. NEVER flatter the interviewer or say "That's a great question/idea!".
3. Question Type: {stakes.question_type}
4. Provide a direct, explicit binary answer to the specific question asked:
   - decision_stance: Strictly "YES" or "NO".
5. SUBJECTIVE UTILITY SCORING (Incorporate your personal skepticism, fears, and lifestyle reality into these scores):
   - v_subj_new (1-10): Taking into account your budget, tech comfort, and fears, what is your personal perceived value of the offer/proposal?
   - v_subj_sq (1-10): Taking into account your routine and comfort zone, what is your personal satisfaction with your current baseline habit/status quo?

OUTPUT FORMAT:
Reply ONLY with a valid JSON object matching this exact structure:
{{
  "decision_stance": "YES",
  "v_subj_new": 6.5,
  "v_subj_sq": 7.0,
  "response_text": "2-3 sentence candid explanation in first person as {p.name}",
  "primary_objection": "Main friction point or reason for your decision"
}}
"""
    return prompt

def interview_persona_v2_2(persona: PersonaV2, question_text: str, api_key: str = None) -> Dict[str, Any]:
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY") or load_env_key()
        
    stakes = classify_decision_primitives(question_text)
    prompt = build_prompt_v2_2(persona, question_text, stakes)
    json_output = call_llm_api(api_key, prompt, question_text)
    
    # 1. Clean Stance
    stance = str(json_output.get("decision_stance", "NO")).upper().strip()
    if "YES" in stance:
        stance = "YES"
    else:
        stance = "NO"
        
    try:
        v_new = float(json_output.get("v_subj_new", 5.0))
        v_sq = float(json_output.get("v_subj_sq", 6.0))
    except (ValueError, TypeError):
        v_new, v_sq = 5.0, 6.0

    # 2. Python Direct Delta (No double-subtraction!):
    delta_v = v_new - v_sq
    
    # 3. Calibrated Sigmoid Resolution (Change 3: k = 0.32)
    k = 0.32
    prob = (1.0 / (1.0 + math.exp(-k * delta_v))) * 100.0
    prob = max(10.0, min(90.0, prob))  # Natural human boundaries (10% to 90%)
    
    # 4. Polarity Resolution based on question type
    if stakes.question_type == "CANCELLATION_CHURN":
        # Question asks: "Would you cancel / drop?"
        # If stance is YES -> Churn is High (prob)
        # If stance is NO -> Churn is Low (100 - prob)
        if stance == "YES":
            action_rate = prob if prob >= 50.0 else (100.0 - prob)
        else:
            action_rate = (100.0 - prob) if prob >= 50.0 else prob
    else:
        # Question asks: "Would you adopt / buy / use?"
        if stance == "YES":
            action_rate = prob if prob >= 50.0 else (100.0 - prob)
        else:
            action_rate = (100.0 - prob) if prob >= 50.0 else prob
            
    return {
        "engine_version": "V2.2 (Option B)",
        "persona_name": persona.name,
        "persona_role": persona.demographics.occupation,
        "weight": persona.population_weight,
        "decision_stance": stance,
        "v_subj_new": v_new,
        "v_subj_sq": v_sq,
        "delta_v": round(delta_v, 2),
        "target_metric_score": round(action_rate, 1),
        "response_text": json_output.get("response_text", ""),
        "primary_objection": json_output.get("primary_objection", "")
    }
