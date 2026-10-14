import math
import json
import os
import sys
import time
from typing import Dict, Any

from v2.persona_schema_v2 import PersonaV2, InterviewResponseV2
from v2.decision_primitives import classify_decision_primitives
from v2.guardrail_v2 import build_guardrailed_prompt_v2

# Import API caller from base interview engine
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from interview_engine import call_llm_api, load_env_key

def calculate_mcfadden_sigmoid(
    v_new: float,
    v_status_quo: float,
    switching_friction: float,
    loss_aversion_multiplier: float,
    sensitivity_k: float = 0.65
) -> float:
    """
    Computes the exact Reference-Dependent Discrete Choice Sigmoid in Python:
    ΔV = (V_new - V_status_quo) - (Friction / 10 * LossAversion * 2.0)
    P(Adopt) = 1 / (1 + exp(-k * ΔV)) * 100
    """
    # Behavioral friction penalty weighted by Kahneman-Tversky loss aversion
    friction_penalty = (switching_friction / 10.0) * loss_aversion_multiplier * 1.8
    delta_v = (v_new - v_status_quo) - friction_penalty
    
    # Sigmoid function
    exp_term = math.exp(-sensitivity_k * delta_v)
    prob_adopt = (1.0 / (1.0 + exp_term)) * 100.0
    
    # Realistic boundary clamping (prevent robotic 0% or 100% unless hard block)
    prob_adopt = max(5.0, min(95.0, prob_adopt))
    return delta_v, round(prob_adopt, 1)

def interview_persona_v2(persona: PersonaV2, question_text: str, api_key: str = None) -> InterviewResponseV2:
    """
    Executes a V2 Stateless Interview Run with:
    1. Automatic Question Decision Primitives Profiling
    2. Reference-Dependent Choice Prompting
    3. Strict Action Enums (ADOPT_INNOVATION vs RETAIN_STATUS_QUO)
    4. Exact Python Sigmoid Resolution (No LLM round-number guessing).
    """
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY") or load_env_key()
        
    # Layer 1: Evaluate question stakes
    stakes = classify_decision_primitives(question_text)
    
    # Layer 2 & 3: Build guardrailed prompt
    system_prompt = build_guardrailed_prompt_v2(persona, question_text, stakes)
    
    # Call LLM
    json_output = call_llm_api(api_key, system_prompt, question_text)
    
    action_dir = str(json_output.get("primary_action_direction", "RETAIN_STATUS_QUO")).upper().strip()
    if "ADOPT" in action_dir:
        action_dir = "ADOPT_INNOVATION"
    else:
        action_dir = "RETAIN_STATUS_QUO"
        
    try:
        v_new = float(json_output.get("v_new_utility", 5.0))
        v_sq = float(json_output.get("v_status_quo_utility", 6.0))
        friction = float(json_output.get("switching_friction_score", 5.0))
    except (ValueError, TypeError):
        v_new, v_sq, friction = 5.0, 6.0, 5.0

    # Layer 4: Exact Python McFadden Reference-Dependent Sigmoid Calculation
    delta_v, prob_adopt = calculate_mcfadden_sigmoid(
        v_new=v_new,
        v_status_quo=v_sq,
        switching_friction=friction,
        loss_aversion_multiplier=persona.psychographics.loss_aversion_bias
    )
    
    # Alignment check: ensure direction matches probability polarity smoothly
    if action_dir == "RETAIN_STATUS_QUO" and prob_adopt > 50.0:
        prob_adopt = round(100.0 - prob_adopt, 1)
    elif action_dir == "ADOPT_INNOVATION" and prob_adopt < 50.0:
        prob_adopt = round(100.0 - prob_adopt, 1)
        
    prob_reject = round(100.0 - prob_adopt, 1)

    return InterviewResponseV2(
        persona_id=persona.id,
        persona_name=persona.name,
        persona_role=persona.demographics.occupation,
        primary_action_direction=action_dir,
        v_new_utility=v_new,
        v_status_quo_utility=v_sq,
        switching_friction_score=friction,
        delta_v_calculated=round(delta_v, 2),
        adoption_probability_percent=prob_adopt,
        rejection_probability_percent=prob_reject,
        response_text=json_output.get("response_text", "No response provided."),
        primary_objection=json_output.get("primary_objection"),
        population_weight=persona.population_weight
    )
