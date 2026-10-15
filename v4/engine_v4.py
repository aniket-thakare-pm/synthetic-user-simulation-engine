"""
v4/engine_v4.py
Engine V4: Empirical-Bayesian Discrete Choice Architecture (EB-DCA)

Architecture:
1. Empirical Base-Rate Prior (V_0 = ln(P_ref / (1 - P_ref))) from Psych-101 & empirical benchmarks.
2. Relative Persona Idiosyncratic Shift (Δv_p in [-2.0, +2.0]) from LLM persona evaluation.
3. Mental Accounting Friction (F_eff via Dominant Bottleneck RMS) scaled by friction domain.
4. Nobel-grounded Random Utility Model (Train 2009 / McFadden Logit):
   ΔV_total = V_0 + (1.25 * Δv_persona) - (F_scaled / 10.0 * lambda_loss)
   P(Action A) = 1 / (1 + exp(-0.32 * ΔV_total))
"""

import os
import sys
import json
import math
from typing import Dict, Any, Optional, Tuple

from v3.persona_schema_v3 import PersonaV3
from v3.category_schema_v3 import CategoryMentalAccount, detect_or_resolve_category
from v3.engine_v3_1 import compute_mental_accounting_friction, derive_action_and_baseline
from v4.empirical_reference_v4 import (
    EmpiricalReferenceArchetype,
    detect_empirical_reference
)
from interview_engine import call_llm_api, load_env_key

def build_prompt_v4(
    persona: PersonaV3,
    question_text: str,
    action_a: str,
    baseline_b: str,
    account: CategoryMentalAccount,
    ref: EmpiricalReferenceArchetype
) -> str:
    p = persona
    rules_list = "\n".join([f"- {rule}" for rule in p.guardrail_rules]) if p.guardrail_rules else "- None"
    values_list = ", ".join(p.psychographics.core_values) if p.psychographics.core_values else "Efficiency"

    prompt = f"""
YOU ARE NOT AN AI ASSISTANT. YOU ARE NOT HELPFUL OR EAGER TO PLEASE.
You are roleplaying strictly as {p.name}, a {p.demographics.occupation} living in {p.demographics.city_tier or 'US/India'}.

=== YOUR PERSONA PROFILE ===
Name: {p.name} | Age: {p.demographics.age} | Income: {p.demographics.income_bracket} | Geography: {p.demographics.geography}
Tech Literacy: {p.demographics.tech_literacy}/10 | Skepticism: {p.psychographics.skepticism_score}/10 | Patience: {p.psychographics.patience_score}/10
Financial Literacy: {p.psychographics.financial_literacy}/10 | Cash Flow Preference: {p.psychographics.liquidity_cash_flow_preference}/10
Primary Payment: {p.capabilities.primary_payment} | Mobility: {p.capabilities.mobility}
Primary Frustration: "{p.psychographics.primary_pain_point}"
Core Values: {values_list}

=== CULTURAL & SOCIAL MINDSET ===
Traditionalism: {p.cultural_mindset.traditionalism_score}/10 | Openness: {p.cultural_mindset.openness_to_experience}/10
Human Recourse Requirement: {p.cognitive_friction.human_recourse_requirement}/10 (Need for in-person human when things go wrong)
Social Proof Threshold: {p.social_network.network_social_proof_threshold}/10

=== CATEGORY CONTEXT ===
Category: {account.display_name}
{account.context_directive}

=== BEHAVIORAL GROUND RULES ===
{rules_list}

=== EMPIRICAL POPULATION CONTEXT ===
{ref.grounding_directive}

=== THE DECISION CHOICE TO EVALUATE ===
Question: "{question_text}"

You are deciding between:
• ACTION A: {action_a}
• BASELINE B: {baseline_b}

=== INSTRUCTIONS FOR PERSONAL DEVIATION EVALUATION ===
1. Respond candidly in first person as {p.name}. Do NOT flatter or be agreeable.
2. An average consumer has an empirical base rate of ~{int(ref.p_ref * 100)}% for Action A.
3. Evaluate your PERSONAL idiosyncratic deviation from an average consumer:
   - decision_stance: "YES" if you choose/lean towards Action A, or "NO" if you choose/lean towards Baseline B.
   - persona_shift (-2.0 to +2.0):
     •  0.0: You align with the typical consumer for this scenario.
     • +1.0 to +2.0: Your specific personality (e.g. high impatience, high tech literacy, high wealth) makes you MUCH MORE likely than average to choose Action A.
     • -1.0 to -2.0: Your specific personality (e.g. extreme thrift, high patience, traditionalism) makes you MUCH LESS likely than average to choose Action A.
   - switching_friction (1.0 to 10.0): The perceived setup hassle, learning curve, or physical inconvenience of Action A for YOU.
   - response_text: 2-3 sentences explaining your personal stance in your authentic voice.

OUTPUT FORMAT:
Reply ONLY with a valid JSON object matching this exact structure:
{{
  "decision_stance": "YES",
  "persona_shift": 0.5,
  "switching_friction": 3.0,
  "response_text": "Candid explanation in first person as {p.name}",
  "primary_objection": "Main friction or reason for your decision"
}}
"""
    return prompt

def interview_persona_v4(
    persona: PersonaV3,
    question_text: str,
    action_label: Optional[str] = None,
    baseline_label: Optional[str] = None,
    category: Optional[str] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Executes a single persona interview turn using Engine V4:
    Empirical-Bayesian Discrete Choice Architecture (EB-DCA).
    """
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY") or load_env_key()

    # 1. Resolve Category Mental Account & Empirical Reference Archetype
    account = detect_or_resolve_category(question_text, explicit_category=category, api_key=api_key)
    ref = detect_empirical_reference(question_text, category=account.category_key)
    action_a, baseline_b = derive_action_and_baseline(question_text, action_label, baseline_label)

    # 2. Build V4 Prompt & Call LLM API
    prompt = build_prompt_v4(persona, question_text, action_a, baseline_b, account, ref)
    json_output = call_llm_api(api_key, prompt, question_text)

    # 3. Parse LLM Outputs
    raw_stance = str(json_output.get("decision_stance", "NO")).upper().strip()
    stance = "YES" if "YES" in raw_stance else "NO"

    try:
        persona_shift = float(json_output.get("persona_shift", 0.0))
        persona_shift = max(-2.0, min(2.0, persona_shift))
    except (ValueError, TypeError):
        persona_shift = 0.5 if stance == "YES" else -0.5

    try:
        raw_friction = float(json_output.get("switching_friction", 3.0))
        raw_friction = max(1.0, min(10.0, raw_friction))
    except (ValueError, TypeError):
        raw_friction = 3.0

    # 4. Compute Effective Friction with Domain Scaling
    f_eff, breakdown = compute_mental_accounting_friction(persona, account, raw_friction)
    f_scaled = f_eff * ref.friction_scaling_factor
    friction_penalty = (f_scaled / 10.0) * ref.loss_aversion_lambda

    # 5. Master Empirical-Bayesian Utility Formulation
    # In natural log-odds space (V_0 = ln(p_ref / (1 - p_ref))),
    # the persona shift modulates around the population base rate.
    beta_persona = 0.25
    scaled_penalty = (f_scaled / 10.0) * 0.15 * ref.loss_aversion_lambda
    delta_v = ref.v_0 + (beta_persona * persona_shift) - scaled_penalty

    # Choice Probability via Standard Econometric Logistic Choice Model (k = 1.0)
    prob = (1.0 / (1.0 + math.exp(-1.0 * delta_v))) * 100.0
    prob_clamped = round(max(5.0, min(95.0, prob)), 1)

    return {
        "engine_version": "V4 (Empirical-Bayesian Discrete Choice)",
        "category": account.category_key,
        "category_display": account.display_name,
        "empirical_archetype": ref.archetype_key,
        "empirical_base_rate": ref.p_ref * 100.0,
        "v_0_prior": ref.v_0,
        "persona_name": persona.name,
        "persona_role": persona.demographics.occupation,
        "weight": persona.population_weight,
        "action_a_label": action_a,
        "baseline_b_label": baseline_b,
        "decision_stance": stance,
        "persona_shift": persona_shift,
        "raw_friction": raw_friction,
        "effective_friction": round(f_eff, 2),
        "scaled_friction": round(f_scaled, 2),
        "friction_penalty": round(friction_penalty, 2),
        "delta_v": round(delta_v, 2),
        "target_metric_score": prob_clamped,
        "response_text": json_output.get("response_text", ""),
        "primary_objection": json_output.get("primary_objection", "")
    }
