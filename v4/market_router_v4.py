"""
v4/market_router_v4.py
Automated Market & Geographic Router for Engine V4

Ensures complete demographic isolation between Indian consumer personas
and US/Global consumer personas. Prevents cross-contamination.
"""

from typing import List, Optional, Tuple
from v3.persona_schema_v3 import PersonaV3
from v3.indian_personas_v3 import INDIAN_PERSONAS_V3
from v3.sample_personas_v3 import SAMPLE_PERSONAS_V3

INDIAN_GEOGRAPHIC_CUES = [
    "₹", "rupee", "rupees", "lakh", "crore", "lpa",
    "upi", "phonepe", "paytm", "gpay", "google pay",
    "kirana", "india", "tier-1", "tier-2", "tier-3",
    "ola", "ather", "tvs ev", "activa", "policybazaar",
    "groww", "zerodha", "sbi", "hdfc", "icici"
]

US_GEOGRAPHIC_CUES = [
    "$", "dollar", "dollars", "usd",
    "apple pay", "venmo", "paypal", "credit score", "401k",
    "suburban", "us", "usa", "american"
]

def resolve_market_and_personas(
    question_text: str,
    explicit_market: Optional[str] = None
) -> Tuple[str, List[PersonaV3]]:
    """
    Resolves the target market code ('IN' or 'US') and returns the dedicated
    statistically calibrated 5-persona panel for that market.
    """
    if explicit_market:
        market_clean = explicit_market.upper().strip()
        if market_clean in ("IN", "INDIA"):
            return "IN", INDIAN_PERSONAS_V3
        elif market_clean in ("US", "USA", "GLOBAL"):
            return "US", SAMPLE_PERSONAS_V3

    text_lower = question_text.lower()

    # Check for Indian markers
    has_indian_cues = any(cue in text_lower for cue in INDIAN_GEOGRAPHIC_CUES)
    has_us_cues = any(cue in text_lower for cue in US_GEOGRAPHIC_CUES)

    if has_indian_cues and not has_us_cues:
        return "IN", INDIAN_PERSONAS_V3
    elif has_us_cues and not has_indian_cues:
        return "US", SAMPLE_PERSONAS_V3
    elif has_indian_cues and has_us_cues:
        # Currency symbol wins
        if "₹" in text_lower or "rupee" in text_lower:
            return "IN", INDIAN_PERSONAS_V3
        return "US", SAMPLE_PERSONAS_V3

    # Default fallback to US panel
    return "US", SAMPLE_PERSONAS_V3
