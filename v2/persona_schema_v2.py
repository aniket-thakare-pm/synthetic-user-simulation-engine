from typing import List, Optional
from pydantic import BaseModel, Field

class Capabilities(BaseModel):
    primary_payment: str = Field(default="UPI (PhonePe/Paytm) & Cash", description="Primary payment method (e.g. UPI, Credit Card, COD)")
    digital_auth: str = Field(default="Mobile OTP", description="Preferred auth flow (e.g. Mobile OTP, Google SSO)")
    mobility: str = Field(default="Two-Wheeler", description="Daily transportation mode (e.g. Two-Wheeler, Car, Public Transit)")
    e_commerce_freq: int = Field(default=5, description="Average online purchase orders per month")
    language_pref: str = Field(default="English", description="UI language preference (e.g. English, Vernacular/Hindi)")
    device_connectivity_tier: str = Field(default="Budget 4G", description="Hardware & network tier (e.g. Flagship 5G, Budget 4G)")

class CulturalMindset(BaseModel):
    traditionalism_score: int = Field(default=5, ge=1, le=10, description="1=Hyper-Secular/Globalist, 10=Deeply Orthodox/Heritage-first")
    openness_to_experience: int = Field(default=5, ge=1, le=10, description="Big 5 Openness: 1=Rigid conventionalist, 10=Novelty seeker")
    ritual_sanctity_sensitivity: int = Field(default=5, ge=1, le=10, description="1=Purely utilitarian tool, 10=Sacred taboo boundary")
    political_cultural_leaning: str = Field(default="Centrist / Pragmatic", description="e.g. Traditionalist-Right, Progressive-Left, Apolitical")

class SocialProofAndNetwork(BaseModel):
    network_social_proof_threshold: int = Field(default=5, ge=1, le=10, description="1=Innovator (buys on Day 0 from online ads); 10=Late majority (needs 3+ trusted peers to use it first)")
    word_of_mouth_dependence: int = Field(default=5, ge=1, le=10, description="1=Zero reliance on friends/family; 10=Will never buy without word-of-mouth")

class CognitiveFriction(BaseModel):
    cognitive_bandwidth_scarcity: int = Field(default=5, ge=1, le=10, description="1=High mental energy/leisure time; 10=Exhausted 13-hour workday, zero energy to learn new tools")
    household_decision_autonomy: int = Field(default=5, ge=1, le=10, description="1=Must get elder/spouse permission for purchases; 10=Completely independent financial buyer")
    capital_asset_lock_in: int = Field(default=3, ge=1, le=10, description="1=Zero financial commitments/free to switch; 10=Currently locked into active multi-year EMI/contracts")
    human_recourse_requirement: int = Field(default=5, ge=1, le=10, description="1=Happy with automated chat bots; 10=Demands physical human face-to-face support when things break")
    formalization_paper_trail_anxiety: int = Field(default=4, ge=1, le=10, description="1=100% formal tax filer; 10=High anxiety regarding digital paper trails/tax scrutiny")

class Demographics(BaseModel):
    age: int = Field(..., description="Age of the persona")
    occupation: str = Field(..., description="Job title or role")
    income_bracket: str = Field(..., description="Income level (e.g. ₹6-8 LPA, ₹24 LPA)")
    tech_literacy: int = Field(..., ge=1, le=10, description="Tech literacy score from 1 to 10")
    geography: str = Field(default="India", description="Target region (e.g. India, US)")
    city_tier: Optional[str] = Field(default=None, description="City classification (e.g. Tier-1 Metro, Tier-2, Tier-3)")

class Psychographics(BaseModel):
    patience_score: int = Field(..., ge=1, le=10, description="Patience score from 1 (impatient) to 10 (very patient)")
    skepticism_score: int = Field(..., ge=1, le=10, description="Skepticism from 1 (naive) to 10 (highly cynical)")
    price_ceiling_monthly: float = Field(..., description="Max monthly budget willingness in local currency")
    primary_pain_point: str = Field(..., description="Main frustration or goal driving decisions")
    core_values: List[str] = Field(default_factory=list, description="Key values (e.g. Speed, Privacy, Simplicity)")
    # Behavioral Economics Parameters (Kahneman & Tversky Reference-Dependent Choice)
    status_quo_inertia: int = Field(default=7, ge=1, le=10, description="Resistance to changing current habits/methods (1=instant switcher, 10=extreme inertia)")
    loss_aversion_bias: float = Field(default=2.25, description="Prospect Theory loss aversion multiplier (overvaluing loss of habit vs potential upside)")
    system_1_habit_strength: int = Field(default=7, ge=1, le=10, description="Degree of passive daily routine vs active deliberate auditing")
    financial_literacy: int = Field(default=7, ge=1, le=10, description="Ability to evaluate interest math, fee transparency, and financial arbitrage (1-10)")
    liquidity_cash_flow_preference: int = Field(default=7, ge=1, le=10, description="Thaler Mental Accounting: Preference for preserving liquid cash in hand vs lump-sum hits (1-10)")

class PersonaV2(BaseModel):
    id: str = Field(..., description="Unique persona ID")
    name: str = Field(..., description="Full name")
    demographics: Demographics
    psychographics: Psychographics
    capabilities: Capabilities = Field(default_factory=Capabilities)
    cultural_mindset: CulturalMindset = Field(default_factory=CulturalMindset)
    social_network: SocialProofAndNetwork = Field(default_factory=SocialProofAndNetwork)
    cognitive_friction: CognitiveFriction = Field(default_factory=CognitiveFriction)
    guardrail_rules: List[str] = Field(default_factory=list, description="Strict negative rules and behavioral boundaries")
    population_weight: float = Field(default=0.20, description="Demographic weight Wi of this persona segment (e.g. 0.35 for 35%)")

class InterviewResponseV2(BaseModel):
    persona_id: str
    persona_name: str
    persona_role: str
    primary_action_direction: str = Field(..., description="Strictly 'ADOPT_INNOVATION' vs 'RETAIN_STATUS_QUO'")
    # Explicit Mathematical Utility Scores rated by the Persona's cognition
    v_new_utility: float = Field(..., ge=1, le=10, description="Perceived utility of the new innovation (1 to 10)")
    v_status_quo_utility: float = Field(..., ge=1, le=10, description="Perceived utility of existing baseline habit (1 to 10)")
    switching_friction_score: float = Field(..., ge=1, le=10, description="Perceived effort, risk, and onboarding friction (1 to 10)")
    # Computed strictly in Python via Sigmoid equation:
    delta_v_calculated: float = Field(..., description="Net utility delta calculated by Python formula")
    adoption_probability_percent: float = Field(..., description="Exact mathematical adoption probability calculated in Python (0-100%)")
    rejection_probability_percent: float = Field(..., description="100 - adoption_probability_percent")
    response_text: str = Field(..., description="Candid first-person summary explanation from the persona")
    primary_objection: Optional[str] = Field(None, description="Main friction point or reason for retaining status quo")
    population_weight: float = Field(default=0.20, description="Demographic weight Wi of this persona")
