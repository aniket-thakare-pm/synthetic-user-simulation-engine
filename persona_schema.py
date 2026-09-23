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

class Persona(BaseModel):
    id: str = Field(..., description="Unique persona ID")
    name: str = Field(..., description="Full name")
    demographics: Demographics
    psychographics: Psychographics
    guardrail_rules: List[str] = Field(default_factory=list, description="Strict negative rules and behavioral boundaries")

class InterviewResponse(BaseModel):
    persona_id: str
    persona_name: str
    persona_role: str
    response_text: str = Field(..., description="Concise, realistic, direct response from the persona")
    primary_objection: Optional[str] = Field(None, description="Main concern or objection if friction exists")
    deterministic_rule_triggered: Optional[str] = Field(None, description="Hard constraint triggered if applicable")
