"""
Decision Primitives Evaluator (V2.1 & V2.2)
Evaluates any question across the 5 Universal Psychological Decision Dimensions
and detects question polarity type (ADOPTION vs CANCELLATION_CHURN).
Includes Dynamic Gating (Change 4) to prevent friction over-injection.
"""
from typing import Dict, Any, List
from pydantic import BaseModel, Field

class DecisionStakesProfile(BaseModel):
    question_type: str = Field(default="ADOPTION", description="Strictly 'ADOPTION' vs 'CANCELLATION_CHURN'")
    downside_asymmetry: float = Field(default=0.2, ge=0.0, le=1.0, description="0 = minor loss (₹100), 1 = health/wealth catastrophe")
    sensory_tactile_need: float = Field(default=0.1, ge=0.0, le=1.0, description="0 = purely digital, 1 = requires physical touch/exam/test-drive")
    social_accountability: float = Field(default=0.2, ge=0.0, le=1.0, description="0 = private choice, 1 = judged by family/peers/law")
    reversibility_friction: float = Field(default=0.2, ge=0.0, le=1.0, description="0 = 1-click cancel, 1 = multi-year lock-in/irreversible")
    taboo_sanctity_weight: float = Field(default=0.1, ge=0.0, le=1.0, description="0 = purely transactional, 1 = touches religion, mortality, honor")

import re

def _has_word(words: List[str], text: str) -> bool:
    return any(re.search(r"\b" + re.escape(w) + r"\b", text, re.IGNORECASE) for w in words)

def classify_decision_primitives(question_text: str) -> DecisionStakesProfile:
    """
    Classifies question type (Adoption vs Churn) and profiles the 5 decision primitives
    using robust whole-word boundary matching.
    """
    text = question_text.lower()
    
    # Question Type Detection (Change 1)
    q_type = "ADOPTION"
    if any(k in text for k in ["cancel", "drop your", "abandon your", "unsubscribe", "stop using", "churn"]):
        q_type = "CANCELLATION_CHURN"

    # 1. Downside Asymmetry (Stakes)
    downside = 0.2
    if _has_word(["health", "doctor", "medical", "hospital", "life insurance", "invest", "mutual fund", "loan", "lending"], text):
        downside = 0.8
    elif _has_word(["scooter", "car", "cars", "vehicle", "two-wheeler", "property", "house"], text):
        downside = 0.6
    elif _has_word(["emi", "bnpl", "credit", "pay later"], text):
        downside = 0.35
        
    # 2. Sensory / Tactile Need
    sensory = 0.1
    if _has_word(["doctor", "clinic", "consultation", "stethoscope", "exam"], text):
        sensory = 0.85
    elif _has_word(["scooter", "car", "vehicle", "test drive", "fabric", "clothes", "furniture"], text):
        sensory = 0.70
        
    # 3. Social / Accountability Exposure
    accountability = 0.2
    if _has_word(["insurance", "term life", "family", "child", "baby", "marriage", "matrimony"], text):
        accountability = 0.8
    elif _has_word(["scooter", "car", "vehicle"], text):
        accountability = 0.45
        
    # 4. Reversibility Friction
    reversibility = 0.2
    if _has_word(["term life", "insurance", "10-year", "annual", "policy"], text):
        reversibility = 0.75
    elif _has_word(["scooter", "car", "vehicle"], text):
        reversibility = 0.70
    elif _has_word(["emi", "loan"], text):
        reversibility = 0.40
        
    # 5. Taboo / Sanctity Weight
    sanctity = 0.1
    if _has_word(["astrolog", "kundali", "baby name", "religion", "puja", "temple", "funeral", "will", "death"], text):
        sanctity = 0.9
    elif _has_word(["health", "medical", "life insurance"], text):
        sanctity = 0.45
        
    return DecisionStakesProfile(
        question_type=q_type,
        downside_asymmetry=downside,
        sensory_tactile_need=sensory,
        social_accountability=accountability,
        reversibility_friction=reversibility,
        taboo_sanctity_weight=sanctity
    )

def get_gated_friction_warnings(stakes: DecisionStakesProfile) -> str:
    """
    Change 4: Dynamic Gating.
    Only injects heavy friction notices when the question's primitives score >= 0.65.
    For routine e-commerce/streaming, returns an empty clean string.
    """
    warnings: List[str] = []
    if stakes.downside_asymmetry >= 0.65:
        warnings.append("⚠️ HIGH-STAKES CONTEXT: This decision involves health, legal, or major capital risk. Errors carry severe real-world consequences.")
    if stakes.sensory_tactile_need >= 0.65:
        warnings.append("⚠️ SENSORY DEFICIT: A purely digital screen cannot physically touch, examine, or test-drive this product.")
    if stakes.social_accountability >= 0.65:
        warnings.append("⚠️ ACCOUNTABILITY EXPOSURE: If this product fails, you face direct judgment from family elders or authorities.")
    if stakes.taboo_sanctity_weight >= 0.65:
        warnings.append("⚠️ SACRED/TABOO DOMAIN: This domain touches tradition, religion, or family heritage. Automation may be viewed as sacrilegious.")
        
    if not warnings:
        return ""
    return "\n" + "\n".join(warnings) + "\n"
