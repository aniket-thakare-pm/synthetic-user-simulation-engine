"""
v4_4/engine_v4_4.py
Engine V4.4: Master Cognitive Choice Architecture

Features:
1. Adaptive Elasticity (Beta = 0.25 for grounded empirical archetypes; Beta = 0.75 for zero-shot).
2. Unanimous Consensus Amplification (Reinforces utility when 100% of demographic personas agree).
3. Dark Pattern / Cognitive Exhaustion Scaling (Accounts for real-world willpower depletion).
4. Full Nobel-Econometric McFadden Random Utility Choice Model.
"""

import math
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class PersonaEvaluationV4_4:
    persona_name: str
    occupation: str
    weight: float
    decision_stance: str
    persona_shift: float       # -2.0 to +2.0
    scaled_friction: float     # 0.5 to 10.0
    response_text: str
    primary_objection: str

@dataclass
class QuestionContextV4_4:
    question_id: str
    title: str
    benchmark_source: str
    ground_truth: float
    is_grounded_archetype: bool
    v_0: float
    loss_lambda: float
    is_dark_pattern: bool = False
    is_involuntary_error: bool = False
    evaluations: List[PersonaEvaluationV4_4] = None

def compute_v4_4_choice_prob(
    v_0: float,
    persona_shift: float,
    scaled_friction: float,
    loss_lambda: float,
    is_grounded: bool = True,
    consensus_boost: float = 0.0,
    is_dark_pattern: bool = False
) -> Dict[str, float]:
    """
    Computes choice probability with Adaptive Elasticity, Consensus Boost,
    and Cognitive Fatigue Damping.
    """
    beta_persona = 0.25 if is_grounded else 0.75
    
    # In dark pattern scenarios, high resistance is damped by cognitive exhaustion
    effective_friction = scaled_friction * 0.65 if (is_dark_pattern and persona_shift < 0) else scaled_friction
    
    scaled_penalty = (effective_friction / 10.0) * 0.15 * loss_lambda
    delta_v = v_0 + (beta_persona * persona_shift) + consensus_boost - scaled_penalty

    # Choice probability via standard McFadden econometric logit
    prob = (1.0 / (1.0 + math.exp(-1.0 * delta_v))) * 100.0
    prob_clamped = round(max(5.0, min(95.0, prob)), 1)

    return {
        "beta_used": beta_persona,
        "scaled_penalty": round(scaled_penalty, 3),
        "consensus_boost": round(consensus_boost, 3),
        "delta_v": round(delta_v, 3),
        "probability": prob_clamped
    }

def evaluate_question_v4_4(q: QuestionContextV4_4) -> Dict[str, Any]:
    """
    Evaluates a single benchmark question across all persona evaluations,
    applying consensus detection and weighted population rollup.
    """
    # 1. Detect demographic consensus across all personas
    yes_count = sum(1 for p in q.evaluations if p.decision_stance == "YES")
    total_personas = len(q.evaluations)
    
    consensus_boost = 0.0
    # Consensus boost only applies to voluntary social choices, not involuntary errors or grounded archetypes
    if not q.is_grounded_archetype and not getattr(q, 'is_involuntary_error', False):
        if yes_count == total_personas:
            # 100% Unanimous YES -> Moderate boost (+0.45) to prevent over-shooting
            consensus_boost = +0.45 if q.loss_lambda >= 2.0 else +0.65
        elif yes_count == 0:
            # 100% Unanimous NO -> Moderate negative boost (-0.45 to -0.65)
            consensus_boost = -0.45 if q.loss_lambda >= 2.0 else -0.65
        elif yes_count >= total_personas - 1:
            # 4/5 Supermajority YES
            consensus_boost = +0.25
        elif yes_count <= 1:
            # 4/5 Supermajority NO
            consensus_boost = -0.25

    weighted_score = 0.0
    total_weight = 0.0
    persona_logs = []

    for p in q.evaluations:
        calc = compute_v4_4_choice_prob(
            v_0=q.v_0,
            persona_shift=p.persona_shift,
            scaled_friction=p.scaled_friction,
            loss_lambda=q.loss_lambda,
            is_grounded=q.is_grounded_archetype,
            consensus_boost=consensus_boost,
            is_dark_pattern=q.is_dark_pattern
        )
        prob = calc["probability"]
        weighted_score += prob * p.weight
        total_weight += p.weight

        persona_logs.append({
            "persona": p.persona_name,
            "occupation": p.occupation,
            "weight": p.weight,
            "stance": p.decision_stance,
            "shift": p.persona_shift,
            "scaled_friction": p.scaled_friction,
            "score": prob,
            "response": p.response_text,
            "objection": p.primary_objection
        })

    predicted_rate = round(weighted_score / total_weight, 1) if total_weight > 0 else 50.0
    error = round(abs(predicted_rate - q.ground_truth), 1)
    accuracy = round(max(0.0, 100.0 - error), 1)

    return {
        "question_id": q.question_id,
        "title": q.title,
        "source": q.benchmark_source,
        "ground_truth": q.ground_truth,
        "predicted_rate": predicted_rate,
        "error": error,
        "accuracy": accuracy,
        "is_grounded": q.is_grounded_archetype,
        "consensus_boost": consensus_boost,
        "persona_logs": persona_logs
    }
