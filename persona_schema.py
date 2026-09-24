from typing import List, Optional
from pydantic import BaseModel, Field

class Demographics(BaseModel):
    age: int = Field(..., description="Age of the persona")
    occupation: str = Field(..., description="Job title or role")
    income_bracket: str = Field(..., description="Income level (e.g. Low, Mid, High, Enterprise)")
    tech_literacy: int = Field(..., ge=1, le=10, description="Tech literacy score from 1 to 10")

class Psychographics(BaseModel):
    patience_score: int = Field(..., ge=1, le=10, description="Patience score from 1 (impatient) to 10 (very patient)")
    skepticism_score: int = Field(..., ge=1, le=10, description="Skepticism from 1 (naive) to 10 (highly cynical)")
    price_ceiling_monthly: float = Field(..., description="Max monthly budget willingness in USD")
    primary_pain_point: str = Field(..., description="Main frustration or goal driving decisions")
    core_values: List[str] = Field(default_factory=list, description="Key values (e.g. Speed, Privacy, Simplicity)")
    # Behavioral Economics Parameters (Kahneman & Tversky Prospect Theory Integration)
    status_quo_inertia: int = Field(default=7, ge=1, le=10, description="Resistance to changing current habits/subscriptions (1=instant switcher, 10=extreme inertia)")
    loss_aversion_bias: float = Field(default=2.25, description="Prospect Theory loss aversion multiplier (overvaluing loss of habit/access vs saving money)")
    system_1_habit_strength: int = Field(default=7, ge=1, le=10, description="Degree to which decisions are driven by automatic habit vs active rational auditing")

class Persona(BaseModel):
    id: str = Field(..., description="Unique persona ID")
    name: str = Field(..., description="Full name")
    demographics: Demographics
    psychographics: Psychographics
    guardrail_rules: List[str] = Field(default_factory=list, description="Strict negative rules and behavioral boundaries")
    population_weight: float = Field(default=0.20, description="Demographic weight Wi of this persona segment (e.g., 0.20)")

class InterviewResponse(BaseModel):
    persona_id: str
    persona_name: str
    persona_role: str
    majority_percent: int = Field(default=70, description="Dominant population probability percentage (e.g. 70 for 70%)")
    minority_percent: int = Field(default=30, description="Conditional exception percentage (e.g. 30 for 30%)")
    primary_action_direction: str = Field(default="CANCEL", description="Directional stance: 'CANCEL'/'REJECT' vs 'KEEP'/'ACCEPT'")
    churn_or_rejection_percent: int = Field(default=50, description="Normalized probability (0-100%) for Cancellation / Rejection / Churn")
    majority_response: str = Field(..., description="Primary response or macro workaround method representing the majority split")
    minority_exception: str = Field(..., description="Conditional exception or alternative macro workaround representing the minority split")
    response_text: str = Field(..., description="Concise overall summary response from the persona")
    primary_objection: Optional[str] = Field(None, description="Main concern or objection if friction exists")
    deterministic_rule_triggered: Optional[str] = Field(None, description="Hard constraint triggered if applicable")
    population_weight: float = Field(default=0.20, description="Demographic weight Wi assigned to this persona")
