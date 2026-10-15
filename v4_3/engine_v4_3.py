"""
v4_3/engine_v4_3.py
Engine V4.3: Adaptive Elasticity & Autonomous Persona Engine

Key Innovations:
1. Adaptive Elasticity (Beta Scaling):
   - Grounded Archetype Match: Beta = 0.25 (Rigid adherence to audited empirical priors)
   - Zero-Shot / Novel Domain: Beta = 0.75, V_0 = 0.0 (Unleashes persona consensus to reach 10% to 90% extremes)
2. Clean Fallback: Never poisons unmatched queries with irrelevant medical/tech baselines.
3. In-Agent Engine: Supports direct persona evaluations with full Nobel-econometric math.
"""

import math
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class PersonaEvaluation:
    persona_name: str
    occupation: str
    weight: float
    decision_stance: str
    persona_shift: float       # -2.0 to +2.0
    raw_friction: float        # 1.0 to 10.0
    effective_friction: float
    scaled_friction: float
    response_text: str
    primary_objection: str

def compute_v4_3_choice_prob(
    v_0: float,
    persona_shift: float,
    scaled_friction: float,
    loss_lambda: float,
    is_grounded: bool = True
) -> Dict[str, float]:
    """
    Computes McFadden utility with Adaptive Elasticity.
    If is_grounded=True: Beta = 0.25 (anchored around empirical prior)
    If is_grounded=False: Beta = 0.75 (adaptive persona elasticity for novel domains)
    """
    beta_persona = 0.25 if is_grounded else 0.75
    scaled_penalty = (scaled_friction / 10.0) * 0.15 * loss_lambda
    delta_v = v_0 + (beta_persona * persona_shift) - scaled_penalty

    # Choice probability via standard McFadden logit
    prob = (1.0 / (1.0 + math.exp(-1.0 * delta_v))) * 100.0
    prob_clamped = round(max(5.0, min(95.0, prob)), 1)

    return {
        "beta_used": beta_persona,
        "scaled_penalty": round(scaled_penalty, 3),
        "delta_v": round(delta_v, 3),
        "probability": prob_clamped
    }
