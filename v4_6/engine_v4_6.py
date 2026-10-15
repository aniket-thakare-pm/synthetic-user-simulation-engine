"""
v4_6/engine_v4_6.py
Engine V4.6: Master Global Cognitive Choice Architecture

Mathematical Foundations:
1. Nobel McFadden Random Utility Discrete Choice Model.
2. Stakes-Scaled Loss Aversion (irrevocable health/wealth vs discretionary media).
3. Universal Willpower Depletion S-Curve (Non-linear surrender under coercive fatigue).
4. Social Consensus Amplification (Voluntary social coordination dynamics).
5. Population-Weighted Demographic Rollup.

CRITICAL PRINCIPLE: Zero question-specific overrides. All rules are global and domain-agnostic.
"""

import math
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class QuestionSpec:
    question_id: str
    title: str
    decision_prompt: str           # The raw decision presented to the user
    benchmark_source: str
    ground_truth: float            # For scoring ONLY; NEVER passed to persona reasoner
    stakes_level: str = "medium"   # "high" (health/wealth), "medium" (commerce/subs), "low" (media/casual)
    is_fatigue_or_dark_pattern: bool = False
    is_involuntary_error: bool = False

@dataclass
class PersonaDecision:
    persona_id: str
    persona_name: str
    demographic_weight: float
    stance: str                 # "YES" or "NO"
    persona_shift: float        # -2.0 to +2.0
    scaled_friction: float      # 0.5 to 10.0
    reasoning: str
    primary_objection: str

def get_stakes_loss_lambda(stakes_level: str) -> float:
    """Universal loss aversion scaling: stakes govern risk sensitivity."""
    stakes_map = {
        "high": 2.1,    # Healthcare, primary banking, physical safety
        "medium": 1.6,  # E-commerce purchases, monthly subscriptions, travel
        "low": 1.2      # Casual apps, content feeds, voluntary polls
    }
    return stakes_map.get(stakes_level.lower(), 1.6)

def compute_choice_prob(
    persona_shift: float,
    scaled_friction: float,
    stakes_level: str = "medium",
    consensus_boost: float = 0.0,
    is_fatigue: bool = False,
    v_0: float = 0.0,
    beta: float = 0.75
) -> Dict[str, float]:
    """
    Computes individual choice probability under McFadden Random Utility Theory.
    """
    loss_lambda = get_stakes_loss_lambda(stakes_level)

    # 1. Asymmetric S-curve Willpower Depletion (Applies to dark pattern / fatigue exhaustion)
    if is_fatigue and persona_shift < 0:
        # Willpower collapses non-linearly when friction crosses threshold
        damping = 0.50 + (0.25 / (1.0 + math.exp(scaled_friction - 3.5)))
        effective_friction = scaled_friction * damping
    else:
        effective_friction = scaled_friction

    # 2. Scaled Friction Penalty (Loss-aversion weighted)
    scaled_penalty = (effective_friction / 10.0) * 0.15 * loss_lambda

    # 3. Net Deterministic Utility V
    delta_v = v_0 + (beta * persona_shift) + consensus_boost - scaled_penalty

    # 4. McFadden Econometric Logistic Choice
    prob = (1.0 / (1.0 + math.exp(-1.0 * delta_v))) * 100.0
    prob_clamped = round(max(5.0, min(95.0, prob)), 1)

    return {
        "loss_lambda": loss_lambda,
        "effective_friction": round(effective_friction, 3),
        "scaled_penalty": round(scaled_penalty, 3),
        "consensus_boost": round(consensus_boost, 3),
        "delta_v": round(delta_v, 3),
        "probability": prob_clamped
    }

def evaluate_question_v4_6(
    spec: QuestionSpec,
    decisions: List[PersonaDecision]
) -> Dict[str, Any]:
    """
    Aggregates dynamically evaluated persona decisions into a population forecast.
    """
    yes_count = sum(1 for d in decisions if d.stance == "YES")
    total_personas = len(decisions)

    # Consensus Amplification: only for voluntary social trends, not involuntary memory errors
    consensus_boost = 0.0
    if not spec.is_involuntary_error:
        loss_lambda = get_stakes_loss_lambda(spec.stakes_level)
        if yes_count == total_personas:
            consensus_boost = +0.45 if loss_lambda >= 2.0 else +0.65
        elif yes_count == 0:
            consensus_boost = -0.45 if loss_lambda >= 2.0 else -0.65
        elif yes_count >= total_personas - 1:
            consensus_boost = +0.25
        elif yes_count <= 1:
            consensus_boost = -0.25

    weighted_prob_sum = 0.0
    total_weight = 0.0
    logs = []

    for d in decisions:
        calc = compute_choice_prob(
            persona_shift=d.persona_shift,
            scaled_friction=d.scaled_friction,
            stakes_level=spec.stakes_level,
            consensus_boost=consensus_boost,
            is_fatigue=spec.is_fatigue_or_dark_pattern
        )
        prob = calc["probability"]
        weighted_prob_sum += prob * d.demographic_weight
        total_weight += d.demographic_weight

        logs.append({
            "persona_id": d.persona_id,
            "name": d.persona_name,
            "weight": d.demographic_weight,
            "stance": d.stance,
            "shift": d.persona_shift,
            "friction": d.scaled_friction,
            "computed_prob": prob,
            "reasoning": d.reasoning,
            "objection": d.primary_objection
        })

    predicted_rate = round(weighted_prob_sum / total_weight, 1) if total_weight > 0 else 50.0
    error = round(abs(predicted_rate - spec.ground_truth), 1)
    accuracy = round(max(0.0, 100.0 - error), 1)

    return {
        "question_id": spec.question_id,
        "title": spec.title,
        "source": spec.benchmark_source,
        "ground_truth": spec.ground_truth,
        "predicted_rate": predicted_rate,
        "error": error,
        "accuracy": accuracy,
        "consensus_boost": consensus_boost,
        "persona_logs": logs
    }
