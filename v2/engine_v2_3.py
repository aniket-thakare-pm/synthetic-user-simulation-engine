"""
Engine V2.3: The Salience-Weighted RMS Choice Model
- LLM evaluates Raw Objective Functional Utility (V_obj_new, V_obj_sq, raw_switching_friction)
- Decision Primitives (Kenneth Train, Keeney & Raiffa) map question stakes to Trait Salience Weights (w_i)
- Countervailing Capabilities (Financial Literacy, Liquidity Preference, Tech Literacy) offset irrational fear
- Non-linear Dominant Bottleneck RMS Stacking:
    F_eff = sqrt(0.65 * H_dom^2 + 0.35 * Mean(H_sec^2))
- Python executes Kenneth Train (2009) subtraction:
    ΔV = (V_obj_new - V_obj_sq) - (F_eff / 10.0 * LossAversion)
- Calibrated Sigmoid Sensitivity k = 0.32 with natural human bounds [10%, 90%]
"""
import math
import os
import sys
from typing import Dict, Any, Tuple

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from v2.persona_schema_v2 import PersonaV2
from v2.decision_primitives import classify_decision_primitives, get_gated_friction_warnings, DecisionStakesProfile
from interview_engine import call_llm_api, load_env_key

def compute_effective_friction(
    persona: PersonaV2,
    stakes: DecisionStakesProfile,
    raw_switching_friction: float
) -> Tuple[float, Dict[str, Any]]:
    """
    Computes effective friction using the Salience-Weighted RMS Bottleneck formula:
    1. Derives salience weights (w_i) from DecisionStakesProfile.
    2. Applies countervailing capabilities (tech_literacy, financial_literacy, liquidity_preference).
    3. Stacks friction via dominant bottleneck RMS to prevent infinite compounding.
    """
    p = persona

    # 1. Operational Switching Friction (Balanced by Tech Literacy)
    tech_offset = 0.25 * (p.demographics.tech_literacy - 5.0)
    f_net_switch = max(1.0, min(10.0, raw_switching_friction - tech_offset))
    w_switch = 1.0  # Onboarding/setup is baseline present in any adoption
    h_switch = w_switch * f_net_switch

    # 2. Sensory / Diagnostic / Human Recourse Friction
    f_net_recourse = float(p.cognitive_friction.human_recourse_requirement)
    w_recourse = float(stakes.sensory_tactile_need)
    h_recourse = w_recourse * f_net_recourse

    # 3. Financial Skepticism / Credit & Downside Risk Friction
    # In financial decisions, Financial Literacy & Liquidity Preference balance panic
    fin_adv = (
        (p.psychographics.financial_literacy - 5.0) +
        (p.psychographics.liquidity_cash_flow_preference - 5.0)
    ) / 2.0
    f_net_financial = max(1.0, min(10.0, p.psychographics.skepticism_score - 0.45 * fin_adv))
    w_financial = max(stakes.downside_asymmetry, stakes.reversibility_friction * 0.7)
    h_financial = w_financial * f_net_financial

    # 4. Capital Lock-in / Irreversibility Friction
    f_net_lockin = float(p.cognitive_friction.capital_asset_lock_in)
    w_lockin = float(stakes.reversibility_friction)
    h_lockin = w_lockin * f_net_lockin

    # 5. Social Proof / Accountability Exposure Friction
    f_net_social = float(p.social_network.network_social_proof_threshold)
    w_social = float(stakes.social_accountability)
    h_social = w_social * f_net_social

    # 6. Taboo / Traditionalism Friction
    f_net_trad = float(p.cultural_mindset.traditionalism_score)
    w_trad = float(stakes.taboo_sanctity_weight)
    h_trad = w_trad * f_net_trad

    hurdles = {
        "switch": h_switch,
        "recourse": h_recourse,
        "financial": h_financial,
        "lockin": h_lockin,
        "social": h_social,
        "trad": h_trad
    }

    # Dominant Bottleneck RMS Stacking
    sorted_hurdles = sorted(hurdles.values(), reverse=True)
    h_dom = sorted_hurdles[0]
    h_sec = [h for h in sorted_hurdles[1:] if h > 0.5]

    if h_sec:
        mean_sec_sq = sum(h ** 2 for h in h_sec) / len(h_sec)
        f_eff = math.sqrt(0.65 * (h_dom ** 2) + 0.35 * mean_sec_sq)
    else:
        f_eff = h_dom

    f_eff = max(1.0, min(10.0, f_eff))

    breakdown = {
        "f_eff": round(f_eff, 2),
        "h_dom": round(h_dom, 2),
        "hurdles": {k: round(v, 2) for k, v in hurdles.items()},
        "f_net_switch": round(f_net_switch, 2),
        "f_net_financial": round(f_net_financial, 2)
    }
    return f_eff, breakdown

def build_prompt_v2_3(persona: PersonaV2, question_text: str, stakes: DecisionStakesProfile) -> str:
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
Financial Literacy: {p.psychographics.financial_literacy}/10 | Cash Flow & Liquidity Preference: {p.psychographics.liquidity_cash_flow_preference}/10
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

=== DIRECTIVES FOR V2.3 OBJECTIVE EVALUATION ===
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
  "switching_friction": 4.0,
  "response_text": "2-3 sentence candid explanation in first person as {p.name}",
  "primary_objection": "Main friction point or reason for your decision"
}}
"""
    return prompt

def interview_persona_v2_3(persona: PersonaV2, question_text: str, api_key: str = None) -> Dict[str, Any]:
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY") or load_env_key()
        
    stakes = classify_decision_primitives(question_text)
    prompt = build_prompt_v2_3(persona, question_text, stakes)
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
        raw_friction = float(json_output.get("switching_friction", 4.0))
    except (ValueError, TypeError):
        v_new, v_sq, raw_friction = 5.0, 6.0, 4.0

    # 2. Python Salience-Weighted RMS Friction & Train (2009) Subtraction:
    f_eff, breakdown = compute_effective_friction(persona, stakes, raw_friction)
    loss_mult = persona.psychographics.loss_aversion_bias
    friction_penalty = (f_eff / 10.0) * loss_mult
    delta_v = (v_new - v_sq) - friction_penalty
    
    # 3. Calibrated Sigmoid Resolution (k = 0.32)
    k = 0.32
    prob = (1.0 / (1.0 + math.exp(-k * delta_v))) * 100.0
    prob = max(10.0, min(90.0, prob))  # Natural human boundaries (10% to 90%)
    
    # 4. Polarity Resolution based on question type
    if stakes.question_type == "CANCELLATION_CHURN":
        # Question asks: "Would you cancel / drop?"
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
        "engine_version": "V2.3 (Salience-Weighted RMS)",
        "persona_name": persona.name,
        "persona_role": persona.demographics.occupation,
        "weight": persona.population_weight,
        "decision_stance": stance,
        "v_obj_new": v_new,
        "v_obj_sq": v_sq,
        "raw_switching_friction": raw_friction,
        "effective_friction": round(f_eff, 2),
        "friction_penalty": round(friction_penalty, 2),
        "delta_v": round(delta_v, 2),
        "target_metric_score": round(action_rate, 1),
        "friction_breakdown": breakdown,
        "response_text": json_output.get("response_text", ""),
        "primary_objection": json_output.get("primary_objection", "")
    }
