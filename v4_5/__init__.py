"""
v4_5/__init__.py
Engine V4.5: The Staged Walk-Forward Cognitive Choice Architecture
Features:
1. Dynamic Cohort Census Weighting
2. Non-Linear Economic Distress Elasticity
3. Sigmoidal Willpower / Cognitive Exhaustion
4. Strict Staged Backward-Compatible Regression Architecture
"""

from .engine_v4_5 import (
    compute_v4_5_choice_prob,
    PersonaEvaluationV4_5,
    QuestionContextV4_5,
    evaluate_question_v4_5
)

__all__ = [
    "compute_v4_5_choice_prob",
    "PersonaEvaluationV4_5",
    "QuestionContextV4_5",
    "evaluate_question_v4_5"
]
