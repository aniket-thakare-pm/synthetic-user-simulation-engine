"""
v4_2/semantic_router_v4_2.py
The LLM Semantic Router (The Intelligent Librarian for V4.2)

Classifies any product manager question or behavioral trade-off into the exact
canonical empirical archetype from ARCHETYPE_LIBRARY_V4_2 using zero-shot semantic intent.
Eliminates all brittle keyword/regex matching.
"""

import os
import json
from typing import Dict, Any, Optional

from v4_2.archetype_library_v4_2 import (
    ARCHETYPE_LIBRARY_V4_2,
    EmpiricalReferenceArchetype,
    get_archetype
)
from interview_engine import call_llm_api, load_env_key

# In-memory routing cache to ensure 0 ms latency on repeated queries
_ROUTING_CACHE: Dict[str, str] = {}

def build_semantic_router_prompt(question_text: str, action_a: Optional[str], baseline_b: Optional[str]) -> str:
    """Builds a compact prompt presenting the full taxonomy of archetypes."""
    taxonomy_lines = []
    for key, arch in ARCHETYPE_LIBRARY_V4_2.items():
        taxonomy_lines.append(f"- \"{key}\": {arch.semantic_criteria}")
    taxonomy_str = "\n".join(taxonomy_lines)

    prompt = f"""
YOU ARE AN EXPERT BEHAVIORAL ECONOMIST AND COGNITIVE SCIENTIST.
Your task is to classify a consumer decision scenario into the single most accurate behavioral economic archetype.

=== AVAILABLE BEHAVIORAL ARCHETYPES ===
{taxonomy_str}

=== THE DECISION SCENARIO TO CLASSIFY ===
Question: "{question_text}"
Action A: "{action_a or 'N/A'}"
Baseline B: "{baseline_b or 'N/A'}"

=== INSTRUCTIONS ===
1. Analyze the core psychological trade-off (e.g. monetary loss aversion, convenience vs password friction, unproven tech skepticism, habit inertia, privacy surveillance, nuisance fee avoidance).
2. Select the SINGLE BEST archetype key from the list above.
3. If no archetype matches closely, select "TECH_DISRUPTION_INSTITUTIONAL_TRUST".

OUTPUT FORMAT:
Reply ONLY with a valid JSON object matching this exact structure:
{{
  "selected_archetype": "EXACT_ARCHETYPE_KEY",
  "confidence": 0.95,
  "core_psychological_tradeoff": "Brief 1-sentence reason for this classification"
}}
"""
    return prompt

def route_question_semantically(
    question_text: str,
    action_a: Optional[str] = None,
    baseline_b: Optional[str] = None,
    api_key: Optional[str] = None
) -> EmpiricalReferenceArchetype:
    """
    Semantically routes an incoming question to its empirical archetype using the LLM.
    Uses an in-memory cache to guarantee zero latency on repeated calls.
    """
    cache_key = question_text.strip().lower()
    if cache_key in _ROUTING_CACHE:
        return get_archetype(_ROUTING_CACHE[cache_key])

    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY") or load_env_key()

    prompt = build_semantic_router_prompt(question_text, action_a, baseline_b)

    try:
        raw_res = call_llm_api(api_key, prompt, question_text)
        selected_key = raw_res.get("selected_archetype", "").strip()

        if selected_key in ARCHETYPE_LIBRARY_V4_2:
            _ROUTING_CACHE[cache_key] = selected_key
            return ARCHETYPE_LIBRARY_V4_2[selected_key]
    except Exception as e:
        print(f"[SemanticRouter Warning] Router call failed ({e}); falling back.")

    # Graceful Fallback if LLM classification fails
    fallback_key = "TECH_DISRUPTION_INSTITUTIONAL_TRUST"
    _ROUTING_CACHE[cache_key] = fallback_key
    return ARCHETYPE_LIBRARY_V4_2[fallback_key]
