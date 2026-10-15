"""
v4_2/__init__.py
Engine V4.2: The Hybrid Cognitive Choice Architecture
Combines an audited Empirical Behavioral Archetype Library with an LLM Semantic Router.
"""

from .archetype_library_v4_2 import (
    EmpiricalReferenceArchetype,
    ARCHETYPE_LIBRARY_V4_2,
    get_archetype
)
from .semantic_router_v4_2 import route_question_semantically
from .engine_v4_2 import interview_persona_v4_2

__all__ = [
    "EmpiricalReferenceArchetype",
    "ARCHETYPE_LIBRARY_V4_2",
    "get_archetype",
    "route_question_semantically",
    "interview_persona_v4_2"
]
