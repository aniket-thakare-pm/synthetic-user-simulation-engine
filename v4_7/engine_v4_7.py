"""
v4_7/engine_v4_7.py
Engine V4.7: The Enterprise Quantitative Core

Key Mathematical Foundations:
1. Continuous Social Consensus Curve:
   Replaces discrete integer step cliffs with a smooth, continuous power law:
   M = (N_YES - N_NO) / N in [-1.0, +1.0]
   Delta_V_consensus = sign(M) * c_lambda * |M|^1.5
   where c_lambda = 0.45 if loss_lambda >= 2.0 else 0.65.
   Continuous and valid for any sample size N.

2. Samuelson-Zeckhauser Status Quo Incumbent Bias (V_inertia):
   Applies an econometric inertia discount (V_inertia = -0.35) for zero-shot switching
   or cancellation decisions to capture real-world consumer inertia without manual friction distortion.

3. Weber-Fechner Relative Price Elasticity:
   Scales monetary friction logarithmically relative to base expenditure:
   ratio = delta_P / P_base
   F_price = 10.0 * ln(1 + ratio) / ln(1 + 2.0), clamped to [0.5, 10.0].

4. Rigorous 95% Statistical Credible Intervals:
   Calculates population-weighted mean, Kish effective persona sample size (N_eff),
   persona heterogeneity variance, and combined binomial survey standard error:
   CI_95 = [P_bar - 1.96 * SE, P_bar + 1.96 * SE].
"""

import math
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class PersonaEvaluationV4_7:
    persona_name: str
    occupation: str
    weight: float
    decision_stance: str
    persona_shift: float       # -2.0 to +2.0
    scaled_friction: float     # 0.5 to 10.0
    response_text: str
    primary_objection: str

@dataclass
class QuestionContextV4_7:
    question_id: str
    title: str
    benchmark_source: str
    ground_truth: float
    is_grounded_archetype: bool
    v_0: float
    loss_lambda: float
    is_dark_pattern: bool = False
    is_involuntary_error: bool = False
    is_status_quo_inertia: bool = False
    delta_price: Optional[float] = None
    base_price: Optional[float] = None
    evaluations: List[PersonaEvaluationV4_7] = None

def compute_v4_7_choice_prob(
    v_0: float,
    persona_shift: float,
    scaled_friction: float,
    loss_lambda: float,
    is_grounded: bool = True,
    consensus_boost: float = 0.0,
    is_dark_pattern: bool = False,
    v_inertia: float = 0.0,
    delta_price: Optional[float] = None,
    base_price: Optional[float] = None
) -> Dict[str, float]:
    """
    Computes choice probability under Nobel McFadden Random Utility Framework
    with Adaptive Elasticity, Continuous Consensus, Status Quo Inertia,
    and Weber-Fechner Price Elasticity.
    """
    beta_persona = 0.25 if is_grounded else 0.75

    # 1. Weber-Fechner Relative Price Friction (if explicit monetary delta/base provided)
    effective_friction = scaled_friction
    if delta_price is not None and base_price is not None and base_price > 0:
        ratio = max(0.0, delta_price / base_price)
        # Scaled on log base 3.0 (i.e. doubling price = ~6.3/10, tripling price = 10/10)
        wf_friction = 10.0 * (math.log(1.0 + ratio) / math.log(1.0 + 2.0))
        effective_friction = max(0.5, min(10.0, wf_friction))

    # 2. Dark Pattern Cognitive Fatigue Damping
    if is_dark_pattern and persona_shift < 0:
        effective_friction = effective_friction * 0.65

    # 3. Scaled Friction Penalty
    scaled_penalty = (effective_friction / 10.0) * 0.15 * loss_lambda

    # 4. Total Utility Delta_V
    delta_v = v_0 + v_inertia + (beta_persona * persona_shift) + consensus_boost - scaled_penalty

    # 5. McFadden Econometric Logit
    prob = (1.0 / (1.0 + math.exp(-1.0 * delta_v))) * 100.0
    prob_clamped = round(max(5.0, min(95.0, prob)), 1)

    return {
        "beta_used": beta_persona,
        "effective_friction": round(effective_friction, 2),
        "scaled_penalty": round(scaled_penalty, 3),
        "consensus_boost": round(consensus_boost, 3),
        "v_inertia": round(v_inertia, 3),
        "delta_v": round(delta_v, 3),
        "probability": prob_clamped
    }

def evaluate_question_v4_7(
    q: QuestionContextV4_7,
    sample_size: int = 1000
) -> Dict[str, Any]:
    """
    Evaluates a single benchmark question across all persona evaluations:
    - Calculates Continuous Social Consensus Power Curve
    - Applies Samuelson-Zeckhauser Status Quo Inertia
    - Computes Population-Weighted Rollup
    - Derives 95% Statistical Credible Intervals
    """
    total_personas = len(q.evaluations)
    yes_count = sum(1 for p in q.evaluations if p.decision_stance == "YES")
    no_count = sum(1 for p in q.evaluations if p.decision_stance == "NO")

    # 1. Continuous Social Consensus Curve
    # Margin M in [-1.0, +1.0]
    consensus_boost = 0.0
    if not q.is_grounded_archetype and not getattr(q, 'is_involuntary_error', False) and total_personas > 0:
        margin = (yes_count - no_count) / float(total_personas)
        c_lambda = 0.45 if q.loss_lambda >= 2.0 else 0.65
        # Continuous power law: Delta_V = sign(M) * c_lambda * |M|^1.5
        sign_m = 1.0 if margin > 0 else (-1.0 if margin < 0 else 0.0)
        consensus_boost = sign_m * c_lambda * (abs(margin) ** 1.5)

    # 2. Samuelson-Zeckhauser Status Quo Incumbent Bias
    # Only applies to ungrounded switching/cancellation decisions (v_0 == 0)
    v_inertia = 0.0
    if getattr(q, 'is_status_quo_inertia', False) and not q.is_grounded_archetype and q.v_0 == 0.0:
        v_inertia = -0.35

    weighted_score = 0.0
    total_weight = 0.0
    persona_logs = []
    persona_probs = []
    persona_weights = []

    for p in q.evaluations:
        calc = compute_v4_7_choice_prob(
            v_0=q.v_0,
            persona_shift=p.persona_shift,
            scaled_friction=p.scaled_friction,
            loss_lambda=q.loss_lambda,
            is_grounded=q.is_grounded_archetype,
            consensus_boost=consensus_boost,
            is_dark_pattern=q.is_dark_pattern,
            v_inertia=v_inertia,
            delta_price=getattr(q, 'delta_price', None),
            base_price=getattr(q, 'base_price', None)
        )
        prob = calc["probability"]
        weighted_score += prob * p.weight
        total_weight += p.weight

        persona_probs.append(prob)
        persona_weights.append(p.weight)

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

    # 3. 95% Statistical Credible Interval Calculation
    # Kish's Effective Sample Size and population-weighted variance
    if total_weight > 0 and len(persona_probs) > 1:
        norm_weights = [w / total_weight for w in persona_weights]
        # Kish N_eff = 1 / sum(w_i^2)
        n_eff = 1.0 / sum(w ** 2 for w in norm_weights)
        # Weighted persona variance
        var_persona = sum(w * ((p - predicted_rate) ** 2) for w, p in zip(norm_weights, persona_probs))
        se_persona = math.sqrt(var_persona / max(1.0, n_eff))
        
        # Binomial survey sampling variance (at sample_size N)
        p_dec = predicted_rate / 100.0
        var_binom = (p_dec * (1.0 - p_dec)) / float(sample_size) * 10000.0  # scaled to percentage points
        se_total = math.sqrt((se_persona ** 2) + var_binom)
        
        ci_lower = round(max(0.0, predicted_rate - (1.96 * se_total)), 1)
        ci_upper = round(min(100.0, predicted_rate + (1.96 * se_total)), 1)
    else:
        ci_lower = predicted_rate
        ci_upper = predicted_rate
        se_total = 0.0

    error = round(abs(predicted_rate - q.ground_truth), 1)
    accuracy = round(max(0.0, 100.0 - error), 1)

    return {
        "question_id": q.question_id,
        "title": q.title,
        "source": q.benchmark_source,
        "ground_truth": q.ground_truth,
        "predicted_rate": predicted_rate,
        "credible_interval_95": [ci_lower, ci_upper],
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "std_error": round(se_total, 2),
        "error": error,
        "accuracy": accuracy,
        "is_grounded": q.is_grounded_archetype,
        "consensus_boost": round(consensus_boost, 3),
        "v_inertia": round(v_inertia, 3),
        "persona_logs": persona_logs
    }
