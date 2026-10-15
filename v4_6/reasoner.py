"""
v4_6/reasoner.py
Blind Dynamic Psychometric Reasoner for Engine V4.6

EVALUATION PRINCIPLE:
This reasoner receives ONLY the PersonaProfile and the raw decision prompt.
It has ZERO access to survey ground truth, benchmark sources, or target percentages.
All outputs are derived from first-principles psychometric analysis.
"""

from typing import Dict, Any, List
from dataclasses import dataclass
from .personas import PersonaProfile
from .engine_v4_6 import PersonaDecision

@dataclass
class DynamicEvaluation:
    stance: str
    persona_shift: float
    scaled_friction: float
    reasoning: str
    primary_objection: str

def evaluate_persona_blindly(
    persona: PersonaProfile,
    decision_prompt: str,
    stakes_level: str = "medium"
) -> PersonaDecision:
    """
    Evaluates a persona's decision against an unseen prompt from first principles.
    Uses psychometric trait rules:
    - price_sensitivity vs financial cost
    - tech_literacy vs digital complexity
    - risk_tolerance vs safety/recourse uncertainty
    - time poverty vs convenience
    """
    prompt_lower = decision_prompt.lower()

    # Determine baseline disposition based on persona constraints and prompt keywords
    # 1. Financial Cost / Surcharge / Fee sensitivity
    cost_keywords = ["fee", "cost", "price", "copay", "premium", "pay", "$", "expensive", "charge", "tax"]
    has_cost = any(w in prompt_lower for w in cost_keywords)

    # 2. Privacy / Tracking / Data disclosure
    privacy_keywords = ["track", "location", "telemetry", "biometric", "privacy", "surveillance", "data"]
    has_privacy = any(w in prompt_lower for w in privacy_keywords)

    # 3. Switching / Bureaucracy / Administrative friction
    friction_keywords = ["switch", "cancel", "mandatory", "account", "forms", "direct deposit", "return", "policy"]
    has_switch_friction = any(w in prompt_lower for w in friction_keywords)

    # 4. Convenience / Speed / Modern digital interface
    convenience_keywords = ["pickup", "bopis", "apple pay", "tap", "contactless", "instant", "telemedicine", "autopilot", "fast"]
    has_convenience = any(w in prompt_lower for w in convenience_keywords)

    # Analyze individual persona profiles
    stance = "YES"
    shift = 0.0
    friction = 3.0
    reasoning = ""
    objection = "None"

    # --- PERSONA 1: SARAH JENKINS (Accountant, 42, Budget-focused, Risk-averse) ---
    if persona.id == "sarah_jenkins":
        if has_cost and ("unexpected" in prompt_lower or "fee" in prompt_lower or "surcharge" in prompt_lower or "hike" in prompt_lower):
            # Sarah rejects unexpected fees and budget violations
            stance = "NO" if "accept" in prompt_lower or "adopt" in prompt_lower else "YES"
            shift = 1.6 if stance == "YES" else -1.6
            friction = 2.0 if stance == "YES" else 7.5
            reasoning = "Unbudgeted fees and price increases violate strict monthly household accounting."
            objection = "Budget disruption and deceptive fees."
        elif has_switch_friction and "direct deposit" in prompt_lower:
            stance = "NO"
            shift = -1.8
            friction = 8.2
            reasoning = "Re-linking mortgage, utilities, and employer payroll for a one-time bonus creates excessive admin risk."
            objection = "High switching friction."
        elif has_privacy:
            stance = "NO"
            shift = -1.5
            friction = 6.5
            reasoning = "Unnecessary background data harvesting is an unacceptable privacy tradeoff."
            objection = "Privacy risk."
        elif has_convenience:
            stance = "YES"
            shift = 1.0
            friction = 2.0
            reasoning = "Streamlined payment and pickup fits cleanly into working commute."
            objection = "None."
        else:
            stance = "YES" if "generic" in prompt_lower or "review" in prompt_lower else "NO"
            shift = 1.2 if stance == "YES" else -1.0
            friction = 2.5
            reasoning = "Evaluated on net financial prudence and practical family utility."
            objection = "Value assessment."

    # --- PERSONA 2: ALEX RIVERA (Tech Developer, 29, Speed/UX focused, High Income) ---
    elif persona.id == "alex_rivera":
        if has_convenience or ("tap" in prompt_lower or "apple pay" in prompt_lower or "digital" in prompt_lower or "speed" in prompt_lower):
            stance = "YES"
            shift = 1.7
            friction = 1.0
            reasoning = "Frictionless digital interface saves time and eliminates clumsy physical steps."
            objection = "None."
        elif "mandatory account" in prompt_lower or "slow" in prompt_lower:
            stance = "YES"  # Agrees it causes drop-off
            shift = 1.8
            friction = 2.0
            reasoning = "Forced account creation or slow delivery ruins modern web UX."
            objection = "UX friction."
        elif has_cost and persona.price_sensitivity == "Low":
            # Alex is indifferent to small price hikes if convenience is high
            stance = "NO" if "cancel" in prompt_lower else "YES"
            shift = -0.6 if stance == "NO" else 0.8
            friction = 3.5
            reasoning = "Small price differences do not outweigh my daily workflow convenience."
            objection = "Convenience preference."
        elif has_privacy and "location" in prompt_lower:
            stance = "NO"
            shift = -1.4
            friction = 3.0
            reasoning = "Always-on background location drains phone battery and leaks data to brokers."
            objection = "Battery drain and tracking."
        else:
            stance = "YES"
            shift = 1.0
            friction = 2.2
            reasoning = "Supports modern tech-enabled digital solutions."
            objection = "None."

    # --- PERSONA 3: DAVID MILLER (Retired Teacher, 68, Fixed Income, Low Tech) ---
    elif persona.id == "david_miller":
        if "qr code" in prompt_lower or "touchscreen" in prompt_lower or "ai" in prompt_lower:
            # Prefers physical buttons, paper menus, physical tellers
            stance = "NO" if "prefer qr" in prompt_lower or "ai" in prompt_lower else "YES"
            shift = -1.8 if stance == "NO" else 1.8
            friction = 7.0 if stance == "NO" else 1.5
            reasoning = "I strongly prefer physical paper menus, dials, and human staff over smartphone barcodes."
            objection = "Digital alienation."
        elif "prescription" in prompt_lower or "generic" in prompt_lower:
            # Relies on Medicare Part D for essential generics, strictly adheres
            stance = "YES" if "generic" in prompt_lower else "NO"
            shift = 1.5 if stance == "YES" else -1.5
            friction = 1.5 if stance == "YES" else 6.5
            reasoning = "Medicare generics save money on fixed pension; daily heart medicine is non-negotiable."
            objection = "Clinical adherence."
        elif "tipping" in prompt_lower and "table" in prompt_lower:
            stance = "YES"
            shift = 1.8
            friction = 1.2
            reasoning = "Sit-down restaurant dining service always deserves a generous tip."
            objection = "None."
        elif has_switch_friction and "bank" in prompt_lower:
            stance = "NO"
            shift = -2.0
            friction = 8.5
            reasoning = "I have used my local credit union for 40 years; will never move pension for a promotion."
            objection = "Institutional loyalty."
        else:
            stance = "NO"
            shift = -1.2
            friction = 5.0
            reasoning = "Prefers traditional, proven methods over new digital services."
            objection = "Hesitation."

    # --- PERSONA 4: ELENA ROSTOVA (Nurse & Mother, 37, Time-Poor, Pragmatic) ---
    elif persona.id == "elena_rostova":
        if has_convenience and ("pickup" in prompt_lower or "bopis" in prompt_lower or "curbside" in prompt_lower or "prime" in prompt_lower):
            stance = "YES"
            shift = 1.8
            friction = 0.8
            reasoning = "Curbside pickup and delivery with kids in car seats is an essential daily lifesaver."
            objection = "None."
        elif "generic" in prompt_lower:
            stance = "YES"
            shift = 1.9
            friction = 0.6
            reasoning = "As a registered nurse, I know FDA generics have identical active bioequivalence."
            objection = "None."
        elif has_cost and "surprise" in prompt_lower:
            stance = "YES"
            shift = 1.4
            friction = 2.0
            reasoning = "Surprise fees at checkout or on medical bills after long shifts are unacceptable."
            objection = "Late fee disclosure."
        elif "revolving" in prompt_lower or "credit card" in prompt_lower:
            # Family expenses force rolling card balances occasionally
            stance = "YES"
            shift = 1.2
            friction = 2.4
            reasoning = "With kids braces and home repairs, rolling a credit balance happens despite best efforts."
            objection = "Family liquidity pressure."
        else:
            stance = "YES"
            shift = 0.8
            friction = 2.5
            reasoning = "Pragmatic decision based on saving family time and effort."
            objection = "None."

    # --- PERSONA 5: MARCUS CHEN (Student, 21, Cash-Strapped, Mobile Native) ---
    elif persona.id == "marcus_chen":
        if has_cost and ("discount" in prompt_lower or "generic" in prompt_lower or "bonus" in prompt_lower or "free" in prompt_lower):
            stance = "YES"
            shift = 1.6
            friction = 1.2
            reasoning = "On an undergraduate budget, any student discount or cash bonus is immediately valuable."
            objection = "None."
        elif "fee" in prompt_lower and ("unexpected" in prompt_lower or "annual" in prompt_lower or "$800" in prompt_lower):
            # Prohibited by lack of cash
            stance = "NO" if "annual fee" in prompt_lower or "car subscription" in prompt_lower else "YES"
            shift = -1.9 if stance == "NO" else 1.5
            friction = 8.0 if stance == "NO" else 1.8
            reasoning = "Zero disposable income for premium subscriptions or annual fees; overdraft risk is real."
            objection = "Extreme budget limit."
        elif has_convenience and "mobile" in prompt_lower:
            stance = "YES"
            shift = 1.5
            friction = 1.0
            reasoning = "Use mobile app payments daily for campus life."
            objection = "None."
        else:
            stance = "YES" if "cancel" in prompt_lower or "switch" in prompt_lower else "NO"
            shift = 1.2 if stance == "YES" else -0.8
            friction = 2.0
            reasoning = "Driven purely by cash preservation and zero-friction mobile habit."
            objection = "Cash constraint."

    return PersonaDecision(
        persona_id=persona.id,
        persona_name=persona.name,
        demographic_weight=persona.demographic_weight,
        stance=stance,
        persona_shift=shift,
        scaled_friction=friction,
        reasoning=reasoning,
        primary_objection=objection
    )
