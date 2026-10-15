"""
v4_6/personas.py
Immutable Demographic Persona Bank for Engine V4.6

These profiles represent fixed empirical archetypes. They are FROZEN and cannot be modified per question.
"""

from dataclasses import dataclass
from typing import Dict, List

@dataclass(frozen=True)
class PersonaProfile:
    id: str
    name: str
    age: int
    occupation: str
    location: str
    annual_income_usd: int
    demographic_weight: float   # US Census representative general baseline
    tech_literacy: str          # "High", "Medium", "Low"
    price_sensitivity: str      # "Extreme", "Moderate", "Low"
    risk_tolerance: str         # "High", "Moderate", "Very Low"
    biography: str
    core_values: List[str]

PERSONA_BANK: Dict[str, PersonaProfile] = {
    "sarah_jenkins": PersonaProfile(
        id="sarah_jenkins",
        name="Sarah Jenkins",
        age=42,
        occupation="Senior Corporate Accountant",
        location="Suburban Columbus, OH",
        annual_income_usd=95000,
        demographic_weight=0.25,
        tech_literacy="Medium",
        price_sensitivity="Moderate",
        risk_tolerance="Very Low",
        biography=(
            "Mother of two with a rigorous approach to household budgeting. Audits bank and credit card "
            "statements monthly. Highly intolerant of hidden fees, unexpected subscription renewals, or "
            "deceptive UX. Values institutional stability, clear pricing, and reliable customer recourse."
        ),
        core_values=["Financial discipline", "Accountability", "Family budget predictability", "Privacy"]
    ),
    "alex_rivera": PersonaProfile(
        id="alex_rivera",
        name="Alex Rivera",
        age=29,
        occupation="Full-Stack Software Engineer",
        location="Urban Seattle, WA",
        annual_income_usd=145000,
        demographic_weight=0.20,
        tech_literacy="High",
        price_sensitivity="Low",
        risk_tolerance="High",
        biography=(
            "Digital native living in a tech hub. Values speed, clean API integrations, and frictionless UI. "
            "Willing to pay a premium for high productivity tools and seamless digital experiences. Quick to "
            "try new software but quickly abandons clumsy or dated legacy workflows."
        ),
        core_values=["Frictionless UX", "Time efficiency", "Technological elegance", "Modern conveniences"]
    ),
    "david_miller": PersonaProfile(
        id="david_miller",
        name="David Miller",
        age=68,
        occupation="Retired High School Teacher",
        location="Rural Lancaster County, PA",
        annual_income_usd=48000,
        demographic_weight=0.20,
        tech_literacy="Low",
        price_sensitivity="Moderate",
        risk_tolerance="Very Low",
        biography=(
            "Living on a defined-benefit pension and Social Security with Medicare. Deeply loyal to familiar, "
            "brick-and-mortar relationships (banked at same credit union for 40 years). Highly skeptical of "
            "AI, automated screening, and mandatory smartphone apps. Prefers physical paper receipts and dials."
        ),
        core_values=["Legacy trust", "Physical customer service", "Financial prudence", "Simplicity"]
    ),
    "elena_rostova": PersonaProfile(
        id="elena_rostova",
        name="Elena Rostova",
        age=37,
        occupation="ER Registered Nurse",
        location="Metro Chicago, IL",
        annual_income_usd=82000,
        demographic_weight=0.20,
        tech_literacy="Medium",
        price_sensitivity="Moderate",
        risk_tolerance="Moderate",
        biography=(
            "Working 12-hour shifts while managing three young children. Chronic time poverty and high mental "
            "exhaustion. Pragmatic adopter of anything that saves physical time (curbside pickup, 1-click ordering). "
            "Has deep medical literacy; will not compromise on healthcare clinical safety or family schedule."
        ),
        core_values=["Time-saving pragmatism", "Family health", "Reliability", "Zero complexity"]
    ),
    "marcus_chen": PersonaProfile(
        id="marcus_chen",
        name="Marcus Chen",
        age=21,
        occupation="Undergraduate Student & Barista",
        location="Austin, TX",
        annual_income_usd=18000,
        demographic_weight=0.15,
        tech_literacy="High",
        price_sensitivity="Extreme",
        risk_tolerance="Moderate",
        biography=(
            "College junior balancing tuition, rent, and a tight checking balance. Mobile-first digital consumer. "
            "Extremely sensitive to out-of-pocket costs and will switch platforms for a $10 coupon or free trial. "
            "Low switching friction because he has few legacy commitments or property ties."
        ),
        core_values=["Cost minimization", "Mobile accessibility", "Immediate utility", "Flexibility"]
    )
}
