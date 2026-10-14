"""
Engine V3.1: Clean Discrete Choice Architecture (Thaler-Train Random Utility Model)
- Pure formulation of Kenneth Train's Discrete Choice Theory (2009) & Richard Thaler's Mental Accounting.
- Explicitly frames every choice as Action A (Target Action / Innovation) vs Baseline B (Counterfactual Status Quo).
- Calculates ΔV = (V_A - V_B) - (F_eff / 10.0 * LossAversion).
- Computes P(Action A) directly via Calibrated McFadden Sigmoid (k = 0.32).
- Zero polarity hacks, zero '100 - prob' flips. 100% mathematically consistent and explainable.
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
    CATEGORY_REGISTRY
)
from interview_engine import call_llm_api, load_env_key

def derive_action_and_baseline(question_text: str, action_label: Optional[str] = None, baseline_label: Optional[str] = None) -> Tuple[str, str]:
    """
    Derives explicit definitions for Action A (the target behavior being measured)
    and Baseline B (the counterfactual/status quo baseline).
    """
    if action_label and baseline_label:
        return action_label, baseline_label

    text = question_text.lower()
    
    # Cancellation / Churn / Abandonment
    if any(k in text for k in ["abandon your", "abandon the", "cancel your", "cancel the", "drop your", "drop the", "stop using", "unsubscribe"]):
        a = "Taking the cancellation/abandonment action described in the question"
        b = "Completing the purchase, keeping the service, or maintaining the status quo despite the friction"
    # Ad-Tier / Plan Switch
    elif any(k in text for k in ["switch to that ad-supported", "switch to", "downgrade"]):
        a = "Switching to the new option / plan proposed in the question"
        b = "Keeping your current plan / current method as-is"
    # Adoption / Purchase / Investment / Consulting
    elif any(k in text for k in ["buy", "adopt", "consult", "use", "invest in", "switch to an electric", "switch to"]):
        a = "Adopting / buying / using the new offering or process asked in the question"
        b = "Sticking with your existing baseline habit / status quo (offline clinic, petrol vehicle, paying upfront, traditional bank)"
    # Habit / Check / Reliance
    elif any(k in text for k in ["check customer reviews", "subscribe just to watch", "frequently sign up"]):
        a = "Engaging in the specific behavior described in the question"
        b = "Not engaging in that behavior / following standard default routine"
    else:
        a = "Choosing Option A (taking the action / innovation described in the question)"
        b = "Choosing Option B (sticking with the default baseline / status quo)"
        
    return a, b

def compute_mental_accounting_friction(
    persona: PersonaV3,
    account: CategoryMentalAccount,
    raw_switching_friction: float
) -> Tuple[float, Dict[str, Any]]:
    """
    Computes effective friction under the active Category Mental Account using Dominant Bottleneck RMS.
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

def build_prompt_v3_1(
    persona: PersonaV3,
    question_text: str,
    action_a: str,
    baseline_b: str,
    account: CategoryMentalAccount
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

=== DECISION CHOICE TO EVALUATE ===
Question: "{question_text}"

You are choosing between two mutually exclusive alternatives:
• ACTION A: {action_a}
• BASELINE B: {baseline_b}

=== DIRECTIVES FOR DISCRETE CHOICE EVALUATION ===
1. Respond naturally, candidly, and CONCISELY as {p.name}.
2. NEVER flatter the interviewer or say "That's a great question/idea!".
3. Provide your explicit choice:
   - decision_stance: "YES" if you choose/lean towards Action A, or "NO" if you choose/lean towards Baseline B.
4. REAL-WORLD OUTCOME VALUATION (Opportunity Cost & Sunk Effort):
   - You must evaluate the REAL-WORLD FUNCTIONAL OUTCOME of both choices, not just theoretical annoyance:
   - If Action A means abandoning, walking away, or canceling: evaluate the real functional outcome of leaving empty-handed without the product or service you needed (which solves zero needs and wastes the time you spent searching).
   - If Baseline B means completing the purchase or maintaining your habit: evaluate the real functional utility of receiving the product or maintaining your service, despite the friction.
   - Do NOT give high utility (e.g. 8/10) to leaving empty-handed out of spite; walking away empty-handed is low functional utility.
5. OBJECTIVE SCORING (Rate the raw facts without double-counting your emotional panic):
   - v_action_a (1-10): Raw objective functional utility to you of the outcome of Action A.
   - v_baseline_b (1-10): Raw objective functional utility to you of the outcome of Baseline B.
   - switching_friction (1-10): The setup hassle, learning curve, or physical effort involved in Action A.

OUTPUT FORMAT:
Reply ONLY with a valid JSON object matching this exact structure:
{{
  "decision_stance": "YES",
  "v_action_a": 6.5,
  "v_baseline_b": 5.0,
  "switching_friction": 3.0,
  "response_text": "2-3 sentence candid explanation in first person as {p.name}",
  "primary_objection": "Main friction point or reason for your decision"
}}
"""
    return prompt

def interview_persona_v3_1(
    persona: PersonaV3,
    question_text: str,
    action_label: Optional[str] = None,
    baseline_label: Optional[str] = None,
    category: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY") or load_env_key()

    account = detect_or_resolve_category(question_text, explicit_category=category, api_key=api_key)
    action_a, baseline_b = derive_action_and_baseline(question_text, action_label, baseline_label)

    prompt = build_prompt_v3_1(persona, question_text, action_a, baseline_b, account)
    json_output = call_llm_api(api_key, prompt, question_text)

    # Clean Stance
    raw_stance = str(json_output.get("decision_stance", "NO")).upper().strip()
    stance = "YES" if "YES" in raw_stance else "NO"

    try:
        v_a = float(json_output.get("v_action_a", json_output.get("v_obj_new", 5.0)))
        v_b = float(json_output.get("v_baseline_b", json_output.get("v_obj_sq", 5.0)))
        raw_friction = float(json_output.get("switching_friction", 3.0))
    except (ValueError, TypeError):
        v_a, v_b, raw_friction = 5.0, 5.0, 3.0

    # 1. Effective Friction via Dominant Bottleneck RMS
    f_eff, breakdown = compute_mental_accounting_friction(persona, account, raw_friction)
    loss_mult = persona.psychographics.loss_aversion_bias
    friction_penalty = (f_eff / 10.0) * loss_mult

    # 2. Kenneth Train (2009) Random Utility Subtraction:
    # ΔV = (V_A - V_B) - Friction Penalty
    delta_v = (v_a - v_b) - friction_penalty

    # 3. Pure McFadden Sigmoid Resolution (k = 0.32):
    # P(Action A) = 1 / (1 + exp(-k * ΔV))
    # Direct, un-inverted, clean choice probability!
    k = 0.32
    p_action_a = (1.0 / (1.0 + math.exp(-k * delta_v))) * 100.0
    p_action_a = max(10.0, min(90.0, p_action_a))  # Natural human bounds

    return {
        "engine_version": "V3.1 (Clean Discrete Choice RUM)",
        "category": account.category_key,
        "category_display": account.display_name,
        "persona_name": persona.name,
        "persona_role": persona.demographics.occupation,
        "weight": persona.population_weight,
        "action_a_label": action_a,
        "baseline_b_label": baseline_b,
        "decision_stance": stance,
        "v_action_a": v_a,
        "v_baseline_b": v_b,
        "raw_switching_friction": raw_friction,
        "effective_friction": round(f_eff, 2),
        "friction_penalty": round(friction_penalty, 2),
        "delta_v": round(delta_v, 2),
        "target_metric_score": round(p_action_a, 1),
        "friction_breakdown": breakdown,
        "response_text": json_output.get("response_text", ""),
        "primary_objection": json_output.get("primary_objection", "")
    }
