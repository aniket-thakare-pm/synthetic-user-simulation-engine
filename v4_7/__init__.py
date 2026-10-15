"""
v4_7/__init__.py
Engine V4.7: The Enterprise Quantitative Core
Incorporates:
1. Continuous Power-Law Social Consensus Curve (Zero Step-Function Cliffs)
2. Samuelson-Zeckhauser Status Quo Incumbent Bias (V_inertia)
3. Weber-Fechner Relative Price Elasticity Formulation
4. Rigorous 95% Statistical Credible Intervals (Monte Carlo Standard Error)
"""

from .engine_v4_7 import (
    QuestionContextV4_7,
    PersonaEvaluationV4_7,
    compute_v4_7_choice_prob,
    evaluate_question_v4_7
)

__all__ = [
    "QuestionContextV4_7",
    "PersonaEvaluationV4_7",
    "compute_v4_7_choice_prob",
    "evaluate_question_v4_7"
]
