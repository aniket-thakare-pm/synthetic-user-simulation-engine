"""
v4_6/__init__.py
Engine V4.6: Autonomous Dynamic Prediction Engine
Features:
- Immutable Demographic Persona Bank
- Blind Dynamic Psychometric Reasoner (Zero Ground Truth Access)
- Universal Nobel-Econometric Choice Architecture
- Staged Walk-Forward Validation Harness
"""

from .personas import PERSONA_BANK, PersonaProfile
from .reasoner import evaluate_persona_blindly, DynamicEvaluation
from .engine_v4_6 import compute_choice_prob, evaluate_question_v4_6, QuestionSpec

__all__ = [
    "PERSONA_BANK",
    "PersonaProfile",
    "evaluate_persona_blindly",
    "DynamicEvaluation",
    "compute_choice_prob",
    "evaluate_question_v4_6",
    "QuestionSpec"
]
