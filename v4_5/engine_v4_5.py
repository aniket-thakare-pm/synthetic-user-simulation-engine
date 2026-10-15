"""
v4_5/engine_v4_5.py
Engine V4.5: Master Staged Walk-Forward Cognitive Choice Architecture

Features:
1. Adaptive Elasticity (Beta = 0.25 grounded archetypes, Beta = 0.75 zero-shot exploratory).
2. Domain Cohort Census Stratification (Empirically weights relevant demographic segments).
3. Sigmoidal Willpower & Fatigue Depletion (Non-linear surrender curve for dark patterns).
4. Economic Distress Elasticity (Captures liquidity constraints in healthcare/debt choices).
5. Dynamic Consensus Amplification with Voluntary Guardrails.
6. Full Nobel-Econometric McFadden Random Utility Choice Model.
"""

import math
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class PersonaEvaluationV4_5:
    persona_name: str
    occupation: str
    weight: float
    decision_stance: str
    persona_shift: float       # -2.0 to +2.0
    scaled_friction: float     # 0.5 to 10.0
    response_text: str
    primary_objection: str

@dataclass
class QuestionContextV4_5:
    question_id: str
    title: str
    benchmark_source: str
    ground_truth: float
    is_grounded_archetype: bool
    v_0: float
    loss_lambda: float
    is_dark_pattern: bool = False
    is_involuntary_error: bool = False
    is_economic_distress: bool = False
    cohort_domain: Optional[str] = None  # 'tech_digital', 'healthcare_senior', 'general'
    evaluations: List[PersonaEvaluationV4_5] = None

# Domain-specific Census Cross-Tab Weights (Pew & US Census Bureau panel baselines)
COHORT_WEIGHT_PROFILES = {
    "tech_digital": {
        "Sarah Jenkins": 0.15,
        "Alex Rivera": 0.30,
        "David Miller": 0.10,
        "Elena Rostova": 0.20,
        "Marcus Chen": 0.25
    },
    "healthcare_senior": {
        "Sarah Jenkins": 0.20,
        "Alex Rivera": 0.10,
        "David Miller": 0.30,
        "Elena Rostova": 0.25,
        "Marcus Chen": 0.15
    },
    "finance_banking": {
        "Sarah Jenkins": 0.25,
        "Alex Rivera": 0.20,
        "David Miller": 0.20,
        "Elena Rostova": 0.20,
        "Marcus Chen": 0.15
    }
}

def compute_v4_5_choice_prob(
    v_0: float,
    persona_shift: float,
    scaled_friction: float,
    loss_lambda: float,
    is_grounded: bool = True,
    consensus_boost: float = 0.0,
    is_dark_pattern: bool = False,
    is_economic_distress: bool = False
) -> Dict[str, float]:
    """
    Computes choice probability under V4.5 McFadden Random Utility formulation
    with S-curve willpower depletion and economic distress elasticity.
    """
    beta_persona = 0.25 if is_grounded else 0.75

    # 1. Sigmoidal Willpower / Cognitive Exhaustion Damping
    if is_dark_pattern and persona_shift < 0:
        # Non-linear S-curve: resistance collapses when friction exceeds threshold
        damping_factor = 0.50 + (0.25 / (1.0 + math.exp(scaled_friction - 3.5)))
        effective_friction = scaled_friction * damping_factor
    else:
        effective_friction = scaled_friction

    # 2. Economic Distress Amplification for Involuntary Choices
    effective_lambda = loss_lambda * 1.25 if (is_economic_distress and persona_shift < 0) else loss_lambda

    # 3. Scaled Friction Penalty
    scaled_penalty = (effective_friction / 10.0) * 0.15 * effective_lambda

    # 4. Total Deterministic Utility
    delta_v = v_0 + (beta_persona * persona_shift) + consensus_boost - scaled_penalty

    # 5. McFadden Econometric Logistic Choice
    prob = (1.0 / (1.0 + math.exp(-1.0 * delta_v))) * 100.0
    prob_clamped = round(max(5.0, min(95.0, prob)), 1)

    return {
        "beta_used": beta_persona,
        "effective_friction": round(effective_friction, 3),
        "effective_lambda": round(effective_lambda, 3),
        "scaled_penalty": round(scaled_penalty, 3),
        "consensus_boost": round(consensus_boost, 3),
        "delta_v": round(delta_v, 3),
        "probability": prob_clamped
    }

def evaluate_question_v4_5(q: QuestionContextV4_5) -> Dict[str, Any]:
    """
    Evaluates a single question under Engine V4.5, resolving consensus dynamics,
    domain cohort census weighting, and persona utility rollups.
    """
    yes_count = sum(1 for p in q.evaluations if p.decision_stance == "YES")
    total_personas = len(q.evaluations)

    consensus_boost = 0.0
    # Consensus boost only applies to voluntary social choices, not involuntary errors or grounded archetypes
    if not q.is_grounded_archetype and not getattr(q, 'is_involuntary_error', False):
        if yes_count == total_personas:
            consensus_boost = +0.45 if q.loss_lambda >= 2.0 else +0.65
        elif yes_count == 0:
            consensus_boost = -0.45 if q.loss_lambda >= 2.0 else -0.65
        elif yes_count >= total_personas - 1:
            consensus_boost = +0.25
        elif yes_count <= 1:
            consensus_boost = -0.25

    # Check for cohort weight profile
    cohort_weights = COHORT_WEIGHT_PROFILES.get(q.cohort_domain, None)

    weighted_score = 0.0
    total_weight = 0.0
    persona_logs = []

    for p in q.evaluations:
        weight = cohort_weights.get(p.persona_name, p.weight) if cohort_weights else p.weight

        calc = compute_v4_5_choice_prob(
            v_0=q.v_0,
            persona_shift=p.persona_shift,
            scaled_friction=p.scaled_friction,
            loss_lambda=q.loss_lambda,
            is_grounded=q.is_grounded_archetype,
            consensus_boost=consensus_boost,
            is_dark_pattern=q.is_dark_pattern,
            is_economic_distress=getattr(q, 'is_economic_distress', False)
        )
        prob = calc["probability"]
        weighted_score += prob * weight
        total_weight += weight

        persona_logs.append({
            "persona": p.persona_name,
            "occupation": p.occupation,
            "weight": weight,
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
        "cohort_domain": q.cohort_domain,
        "persona_logs": persona_logs
    }
