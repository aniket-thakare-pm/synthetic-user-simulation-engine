"""
V3 Category Taxonomy & Mental Accounting Profiles (Thaler-Train Architecture)
Defines 6 MECE Consumer Categories and their underlying Mental Accounting Salience Weights.
Supports both explicit enterprise categorization and autonomous AI classification.
"""
import os
import json
from typing import Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field

from interview_engine import call_llm_api, load_env_key

class CategoryMentalAccount(BaseModel):
    category_key: str
    display_name: str
    mental_account_archetype: str
    context_directive: str
    # Psychological Salience Weights (w_i in [0.0, 1.0])
    sensory_physical_need: float = Field(ge=0.0, le=1.0)
    human_recourse_need: float = Field(ge=0.0, le=1.0)
    fee_transparency_need: float = Field(ge=0.0, le=1.0)
    liquidity_preservation_need: float = Field(ge=0.0, le=1.0)
    lock_in_irreversibility: float = Field(ge=0.0, le=1.0)
    social_accountability: float = Field(ge=0.0, le=1.0)
    taboo_sanctity: float = Field(ge=0.0, le=1.0)

CATEGORY_REGISTRY: Dict[str, CategoryMentalAccount] = {
    "HEALTH_AND_DIAGNOSTICS": CategoryMentalAccount(
        category_key="HEALTH_AND_DIAGNOSTICS",
        display_name="Healthtech & Medical Diagnostics",
        mental_account_archetype="Survival, Clinical Efficacy & Physical Diagnostic Trust",
        context_directive=(
            "MENTAL ACCOUNT: HEALTH & MEDICAL DIAGNOSTICS.\n"
            "• For minor common ailments (mild fever, seasonal cold, minor rash, routine follow-ups), video consults save travel and clinic waiting time.\n"
            "• However, the inability of a screen to physically palpate, auscultate with a stethoscope, or run immediate in-person swabs creates substantial diagnostic hesitation for many users."
        ),
        sensory_physical_need=0.85,
        human_recourse_need=0.85,
        fee_transparency_need=0.30,
        liquidity_preservation_need=0.10,
        lock_in_irreversibility=0.20,
        social_accountability=0.30,
        taboo_sanctity=0.35,
    ),
    "FINTECH_CREDIT_AND_LENDING": CategoryMentalAccount(
        category_key="FINTECH_CREDIT_AND_LENDING",
        display_name="Fintech: BNPL, Credit & Working Capital",
        mental_account_archetype="Cash-Flow Smoothing, Working Capital & Debt Underwriting",
        context_directive=(
            "MENTAL ACCOUNT: LIQUIDITY, WORKING CAPITAL & NO-COST INSTALLMENTS.\n"
            "• Preserving daily liquid cash in hand vs lump-sum hits is a major financial advantage.\n"
            "• High financial literacy personas welcome genuine 0% no-cost EMI (on UPI/debit/credit) to manage cash flow.\n"
            "• Personas strictly reject hidden processing fees, recurring auto-debit traps, or high interest loans."
        ),
        sensory_physical_need=0.05,
        human_recourse_need=0.20,
        fee_transparency_need=0.95,
        liquidity_preservation_need=0.90,
        lock_in_irreversibility=0.40,
        social_accountability=0.20,
        taboo_sanctity=0.10,
    ),
    "WEALTH_AND_INVESTMENTS": CategoryMentalAccount(
        category_key="WEALTH_AND_INVESTMENTS",
        display_name="Wealthtech: Mutual Funds, SIPs & Equities",
        mental_account_archetype="Long-Term Capital Growth & Fiduciary Platform Trust",
        context_directive=(
            "MENTAL ACCOUNT: WEALTH ACCUMULATION & COMPOUNDING.\n"
            "• Salaried professionals and digital earners actively use direct mutual fund SIP apps to compound wealth without broker commissions.\n"
            "• Traditional merchants and conservative savers prioritize liquid business working capital, guaranteed bank FDs, or physical gold over equity market volatility."
        ),
        sensory_physical_need=0.05,
        human_recourse_need=0.40,
        fee_transparency_need=0.85,
        liquidity_preservation_need=0.40,
        lock_in_irreversibility=0.50,
        social_accountability=0.30,
        taboo_sanctity=0.15,
    ),
    "INSURANCE_AND_PROTECTION": CategoryMentalAccount(
        category_key="INSURANCE_AND_PROTECTION",
        display_name="Insurtech: Health, Life & Term Policies",
        mental_account_archetype="Disaster Protection, Family Fiduciary Trust & Claims Recourse",
        context_directive=(
            "MENTAL ACCOUNT: FAMILY RISK & INSURANCE FIDUCIARY.\n"
            "• Claims settlement certainty, verified company track record, and recourse when tragedy hits are paramount.\n"
            "• Many buyers demand physical agents for claim guarantees, unless the app proves transparent high claim settlement ratios."
        ),
        sensory_physical_need=0.10,
        human_recourse_need=0.85,
        fee_transparency_need=0.80,
        liquidity_preservation_need=0.30,
        lock_in_irreversibility=0.80,
        social_accountability=0.80,
        taboo_sanctity=0.45,
    ),
    "MOBILITY_AND_DURABLES": CategoryMentalAccount(
        category_key="MOBILITY_AND_DURABLES",
        display_name="Mobility & High-Value Durables (EVs, Appliances)",
        mental_account_archetype="Physical Operational Infrastructure & Daily Downtime Risk",
        context_directive=(
            "MENTAL ACCOUNT: OPERATIONAL MOBILITY & HIGH-VALUE DURABLES.\n"
            "• Massive monthly fuel savings (electricity vs expensive petrol) strongly appeal to daily city commuters.\n"
            "• However, charging infrastructure hassle, battery degradation, and roadside downtime risk remain significant considerations."
        ),
        sensory_physical_need=0.70,
        human_recourse_need=0.65,
        fee_transparency_need=0.60,
        liquidity_preservation_need=0.60,
        lock_in_irreversibility=0.75,
        social_accountability=0.45,
        taboo_sanctity=0.10,
    ),
    "DIGITAL_SUBSCRIPTIONS_AND_COMMERCE": CategoryMentalAccount(
        category_key="DIGITAL_SUBSCRIPTIONS_AND_COMMERCE",
        display_name="Digital Entertainment & Subscriptions",
        mental_account_archetype="Everyday Discretionary Leisure, Streaming & Recurring Subscriptions",
        context_directive=(
            "MENTAL ACCOUNT: DISCRETIONARY SUBSCRIPTIONS & STREAMING.\n"
            "• Fast 1-click convenience, transparent monthly pricing, and instant gratification govern decisions.\n"
            "• Sudden price hikes or serial binging trigger immediate churn, plan cancellations, or downgrading to ad-tiers."
        ),
        sensory_physical_need=0.10,
        human_recourse_need=0.20,
        fee_transparency_need=0.75,
        liquidity_preservation_need=0.30,
        lock_in_irreversibility=0.20,
        social_accountability=0.15,
        taboo_sanctity=0.05,
    ),
    "ECOMMERCE_CHECKOUT_AND_RETAIL": CategoryMentalAccount(
        category_key="ECOMMERCE_CHECKOUT_AND_RETAIL",
        display_name="E-Commerce Checkout, Cart & Retail UX",
        mental_account_archetype="Transactional Purchase, Cart Sunk-Cost & Checkout Friction",
        context_directive=(
            "MENTAL ACCOUNT: E-COMMERCE RETAIL & CHECKOUT CONVERSION.\n"
            "• Sunk-Cost Cart Inertia: The shopper has already invested time finding the specific item they want.\n"
            "• Frictions (account creation, unexpected shipping costs, delivery speed, return policies) are evaluated against the desire to receive the item vs the frustration of walking away empty-handed."
        ),
        sensory_physical_need=0.20,
        human_recourse_need=0.30,
        fee_transparency_need=0.85,
        liquidity_preservation_need=0.50,
        lock_in_irreversibility=0.30,
        social_accountability=0.20,
        taboo_sanctity=0.05,
    ),
}

# Aliases for developer convenience
CATEGORY_ALIASES = {
    "health": "HEALTH_AND_DIAGNOSTICS",
    "telemed": "HEALTH_AND_DIAGNOSTICS",
    "telemedicine": "HEALTH_AND_DIAGNOSTICS",
    "doctor": "HEALTH_AND_DIAGNOSTICS",
    "medical": "HEALTH_AND_DIAGNOSTICS",
    "bnpl": "FINTECH_CREDIT_AND_LENDING",
    "credit": "FINTECH_CREDIT_AND_LENDING",
    "emi": "FINTECH_CREDIT_AND_LENDING",
    "lending": "FINTECH_CREDIT_AND_LENDING",
    "loan": "FINTECH_CREDIT_AND_LENDING",
    "fintech": "FINTECH_CREDIT_AND_LENDING",
    "invest": "WEALTH_AND_INVESTMENTS",
    "investment": "WEALTH_AND_INVESTMENTS",
    "sip": "WEALTH_AND_INVESTMENTS",
    "mutual_fund": "WEALTH_AND_INVESTMENTS",
    "mutual_funds": "WEALTH_AND_INVESTMENTS",
    "wealth": "WEALTH_AND_INVESTMENTS",
    "insurance": "INSURANCE_AND_PROTECTION",
    "insurtech": "INSURANCE_AND_PROTECTION",
    "policy": "INSURANCE_AND_PROTECTION",
    "mobility": "MOBILITY_AND_DURABLES",
    "ev": "MOBILITY_AND_DURABLES",
    "scooter": "MOBILITY_AND_DURABLES",
    "durables": "MOBILITY_AND_DURABLES",
    "auto": "MOBILITY_AND_DURABLES",
    "subscription": "DIGITAL_SUBSCRIPTIONS_AND_COMMERCE",
    "streaming": "DIGITAL_SUBSCRIPTIONS_AND_COMMERCE",
    "media": "DIGITAL_SUBSCRIPTIONS_AND_COMMERCE",
    "ecommerce": "ECOMMERCE_CHECKOUT_AND_RETAIL",
    "cart": "ECOMMERCE_CHECKOUT_AND_RETAIL",
    "checkout": "ECOMMERCE_CHECKOUT_AND_RETAIL",
}

def detect_or_resolve_category(
    question_text: str,
    explicit_category: Optional[str] = None,
    api_key: Optional[str] = None
) -> CategoryMentalAccount:
    """
    Resolves the CategoryMentalAccount:
    1. If explicit_category is provided, looks it up in CATEGORY_REGISTRY (or aliases).
    2. Otherwise, performs a fast AI classification to map the question text to one of the 6 categories.
    """
    if explicit_category:
        norm = explicit_category.strip().upper()
        if norm in CATEGORY_REGISTRY:
            return CATEGORY_REGISTRY[norm]
        clean_alias = explicit_category.strip().lower()
        if clean_alias in CATEGORY_ALIASES:
            return CATEGORY_REGISTRY[CATEGORY_ALIASES[clean_alias]]

    # Fast Autonomous AI Classification (Zero Hardcoded Regex)
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY") or load_env_key()

    classification_prompt = f"""
You are an expert behavioral economist. Classify the following product/decision question into EXACTLY ONE of these 6 MECE consumer categories:
1. HEALTH_AND_DIAGNOSTICS (Doctor video consults, medical testing, clinical apps)
2. FINTECH_CREDIT_AND_LENDING (Buy-Now-Pay-Later, 0% No-Cost EMI, credit lines, checkout loans)
3. WEALTH_AND_INVESTMENTS (Mutual funds, SIPs, stock trading apps, gold, long-term savings)
4. INSURANCE_AND_PROTECTION (Term life, health insurance policies, online policy buying)
5. MOBILITY_AND_DURABLES (Electric vehicles, scooters, cars, home appliances, hardware durables)
6. DIGITAL_SUBSCRIPTIONS_AND_COMMERCE (Streaming services, SaaS, e-commerce checkout, digital media)

QUESTION TO CLASSIFY:
"{question_text}"

OUTPUT FORMAT:
Reply ONLY with a JSON object:
{{
  "category_key": "CATEGORY_KEY_HERE",
  "confidence": 0.95
}}
"""
    try:
        res = call_llm_api(api_key, classification_prompt, question_text)
        detected_key = str(res.get("category_key", "")).strip().upper()
        if detected_key in CATEGORY_REGISTRY:
            return CATEGORY_REGISTRY[detected_key]
    except Exception:
        pass

    # Safe default: Digital Subscriptions & Commerce
    return CATEGORY_REGISTRY["DIGITAL_SUBSCRIPTIONS_AND_COMMERCE"]

def classify_question_type(question_text: str) -> str:
    """Detects whether question is ADOPTION (buy/use) or CANCELLATION_CHURN (cancel/drop)."""
    text = question_text.lower()
    if any(k in text for k in ["cancel", "drop your", "abandon your", "unsubscribe", "stop using", "churn"]):
        return "CANCELLATION_CHURN"
    return "ADOPTION"
