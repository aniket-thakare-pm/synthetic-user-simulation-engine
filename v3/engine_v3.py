"""
Engine V3: Category-Aware Mental Accounting Choice Architecture (Thaler-Train Model)
- Grounded in Richard Thaler's Mental Accounting (2017 Nobel Prize) and Kenneth Train's Discrete Choice (2009).
- Evaluates choices through explicit non-fungible Category Mental Accounts.
- Non-linear Dominant Bottleneck RMS Stacking of category-salient psychological frictions.
- Python Kenneth Train Subtraction: ΔV = (V_obj_new - V_obj_sq) - (F_eff / 10.0 * LossAversion).
- Calibrated McFadden Sigmoid Resolution (k = 0.32) bounded to [10%, 90%].
"""
import math
import os
import sys
from typing import Dict, Any, Tuple, Optional

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from v3.persona_schema_v3 import PersonaV3
from v3.category_schema_v3 import (
    CategoryMentalAccount, detect_or_resolve_category,
    classify_question_type, CATEGORY_REGISTRY
)
from interview_engine import call_llm_api, load_env_key

def compute_mental_accounting_friction(
    persona: PersonaV3,
    account: CategoryMentalAccount,
    raw_switching_friction: float
) -> Tuple[float, Dict[str, Any]]:
    """
    Computes effective friction under the active Category Mental Account:
    1. Extracts category salience weights (w_i).
    2. Applies persona countervailing capabilities (tech_literacy, financial_literacy, liquidity_preference).
    3. Stacks friction components via Dominant Bottleneck RMS to avoid compound over-penalization.
    """
    p = persona

    # 1. Operational Switching Friction (Balanced by Tech Literacy)
    tech_offset = 0.25 * (p.demographics.tech_literacy - 5.0)
    f_net_switch = max(1.0, min(10.0, raw_switching_friction - tech_offset))
    w_switch = 1.0
    h_switch = w_switch * f_net_switch

    # 2. Sensory / Diagnostic / Human Recourse Friction
    f_net_recourse = float(p.cognitive_friction.human_recourse_requirement)
    w_recourse = max(account.sensory_physical_need, account.human_recourse_need)
    h_recourse = w_recourse * f_net_recourse

    # 3. Fee Transparency & Debt Fear vs. Financial Literacy (Thaler Mental Accounting)
    fin_advantage = (
        (p.psychographics.financial_literacy - 5.0) +
        (p.psychographics.liquidity_cash_flow_preference - 5.0)
    ) / 2.0
    # In liquidity/credit accounts, financial capability offsets irrational debt fear
    f_net_financial = max(1.0, min(10.0, p.psychographics.skepticism_score - 0.50 * fin_advantage * account.liquidity_preservation_need))
    w_financial = account.fee_transparency_need
    h_financial = w_financial * f_net_financial

    # 4. Capital Lock-in / Irreversibility Friction
    f_net_lockin = float(p.cognitive_friction.capital_asset_lock_in)
    w_lockin = account.lock_in_irreversibility
    h_lockin = w_lockin * f_net_lockin

    # 5. Social Proof / Accountability Friction
    f_net_social = float(p.social_network.network_social_proof_threshold)
    w_social = account.social_accountability
    h_social = w_social * f_net_social

    # 6. Taboo / Cultural Traditionalism Friction
    f_net_trad = float(p.cultural_mindset.traditionalism_score)
    w_trad = account.taboo_sanctity
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

def build_prompt_v3(
    persona: PersonaV3,
    question_text: str,
    account: CategoryMentalAccount,
    q_type: str
) -> str:
    p = persona
    rules_list = "\n".join([f"- {rule}" for rule in p.guardrail_rules]) if p.guardrail_rules else "- None"
    values_list = ", ".join(p.psychographics.core_values) if p.psychographics.core_values else "Efficiency"

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

=== CATEGORY MENTAL ACCOUNT CONTEXT ===
Category: {account.display_name}
{account.context_directive}

=== BEHAVIORAL RULES ===
{rules_list}

=== DIRECTIVES FOR V3 OBJECTIVE EVALUATION ===
1. Respond naturally, candidly, and CONCISELY as {p.name}.
2. NEVER flatter the interviewer or say "That's a great question/idea!".
3. Question Type: {q_type}
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

def interview_persona_v3(
    persona: PersonaV3,
    question_text: str,
    category: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY") or load_env_key()

    account = detect_or_resolve_category(question_text, explicit_category=category, api_key=api_key)
    q_type = classify_question_type(question_text)

    prompt = build_prompt_v3(persona, question_text, account, q_type)
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

    # 2. Python Mental Accounting RMS Friction & Kenneth Train (2009) Subtraction:
    f_eff, breakdown = compute_mental_accounting_friction(persona, account, raw_friction)
    loss_mult = persona.psychographics.loss_aversion_bias
    friction_penalty = (f_eff / 10.0) * loss_mult
    delta_v = (v_new - v_sq) - friction_penalty

    # 3. Calibrated Sigmoid Resolution (k = 0.32)
    k = 0.32
    prob = (1.0 / (1.0 + math.exp(-k * delta_v))) * 100.0
    prob = max(10.0, min(90.0, prob))  # Natural human boundaries (10% to 90%)

    # 4. Polarity Resolution based on question type
    if q_type == "CANCELLATION_CHURN":
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
        "engine_version": "V3 (Mental Accounting Thaler-Train)",
        "category": account.category_key,
        "category_display": account.display_name,
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
