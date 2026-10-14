"""
Engine V2.1: The Pure Econometric Model (Option A)
- LLM evaluates Raw Objective Functional Utility (V_obj_new, V_obj_sq, SwitchingFriction)
- Python executes Kenneth Train (2009) subtraction: ΔV = (V_obj_new - V_obj_sq) - (Friction / 10 * LossAversion)
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

def build_prompt_v2_1(persona: PersonaV2, question_text: str, stakes) -> str:
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

=== CULTURAL & SOCIAL MINDSET ===
Traditionalism: {p.cultural_mindset.traditionalism_score}/10 | Openness: {p.cultural_mindset.openness_to_experience}/10
Social Proof / Word-of-Mouth Threshold: {p.social_network.network_social_proof_threshold}/10 (How much you wait for trusted peers)
Human Recourse Need: {p.cognitive_friction.human_recourse_requirement}/10 (Need for physical human when things fail)

=== DECISION CONTEXT ===
{gated_warnings if gated_warnings else "Standard commercial/utility decision."}

=== BEHAVIORAL RULES ===
{rules_list}

=== DIRECTIVES FOR V2.1 OBJECTIVE EVALUATION ===
1. Respond naturally, candidly, and CONCISELY as {p.name}.
2. NEVER flatter the interviewer or say "That's a great question/idea!".
3. Question Type: {stakes.question_type}
4. You must provide a direct, explicit binary answer to the specific question asked:
   - decision_stance: Strictly "YES" or "NO".
5. OBJECTIVE SCORING (Rate the facts without double-counting your emotional panic):
   - v_obj_new (1-10): On pure objective features, pricing, and specs, what is the raw utility of the offer/proposal?
   - v_obj_sq (1-10): On pure objective utility, how well does your current baseline habit/status quo solve your need today?
   - switching_friction (1-10): How much setup effort, learning curve, or physical hassle is required to switch?

OUTPUT FORMAT:
Reply ONLY with a valid JSON object matching this exact structure:
{{
  "decision_stance": "YES",
  "v_obj_new": 7.5,
  "v_obj_sq": 7.0,
  "switching_friction": 5.0,
  "response_text": "2-3 sentence candid explanation in first person as {p.name}",
  "primary_objection": "Main friction point or reason for your decision"
}}
"""
    return prompt

def interview_persona_v2_1(persona: PersonaV2, question_text: str, api_key: str = None) -> Dict[str, Any]:
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY") or load_env_key()
        
    stakes = classify_decision_primitives(question_text)
    prompt = build_prompt_v2_1(persona, question_text, stakes)
    json_output = call_llm_api(api_key, prompt, question_text)
    
    # 1. Clean Stance
    stance = str(json_output.get("decision_stance", "NO")).upper().strip()
    if "YES" in stance:
        stance = "YES"
    else:
        stance = "NO"
        
    try:
        v_new = float(json_output.get("v_obj_new", 5.0))
        v_sq = float(json_output.get("v_obj_sq", 6.0))
        friction = float(json_output.get("switching_friction", 5.0))
    except (ValueError, TypeError):
        v_new, v_sq, friction = 5.0, 6.0, 5.0

    # 2. Python Kenneth Train (2009) Subtraction:
    # ΔV = (V_obj_new - V_obj_sq) - (Friction / 10 * LossAversion)
    loss_mult = persona.psychographics.loss_aversion_bias
    friction_penalty = (friction / 10.0) * loss_mult
    delta_v = (v_new - v_sq) - friction_penalty
    
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
        "engine_version": "V2.1 (Option A)",
        "persona_name": persona.name,
        "persona_role": persona.demographics.occupation,
        "weight": persona.population_weight,
        "decision_stance": stance,
        "v_obj_new": v_new,
        "v_obj_sq": v_sq,
        "friction": friction,
        "friction_penalty": round(friction_penalty, 2),
        "delta_v": round(delta_v, 2),
        "target_metric_score": round(action_rate, 1),
        "response_text": json_output.get("response_text", ""),
        "primary_objection": json_output.get("primary_objection", "")
    }
