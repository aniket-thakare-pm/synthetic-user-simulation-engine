from persona_schema import Persona, Demographics, Psychographics

from persona_schema import Persona, Demographics, Psychographics

# 5 MECE Behavioral Mindset Personas
SAMPLE_PERSONAS = [
    Persona(
        id="p_01_accountant_sarah",
        name="Sarah Jenkins",
        demographics=Demographics(
            age=42,
            occupation="Senior Accountant [The Value Auditor]",
            income_bracket="Mid",
            tech_literacy=4
        ),
        psychographics=Psychographics(
            patience_score=3,
            skepticism_score=8,
            price_ceiling_monthly=25.0,
            primary_pain_point="Hates hidden subscription costs, forced sales calls, and bloated software.",
            core_values=["Clarity", "Budget Control", "No Hassle"]
        ),
        guardrail_rules=[
            "Reject software requiring a sales call for pricing.",
            "If price exceeds $25/month, immediately flag as overpriced."
        ]
    ),
    Persona(
        id="p_02_founder_alex",
        name="Alex Chen",
        demographics=Demographics(
            age=29,
            occupation="Startup Founder [The Impatient Pragmatist]",
            income_bracket="High",
            tech_literacy=9
        ),
        psychographics=Psychographics(
            patience_score=7,
            skepticism_score=6,
            price_ceiling_monthly=99.0,
            primary_pain_point="Wastes time on manual tasks; wants API-first tools with instant self-serve setup.",
            core_values=["Speed", "Developer Experience", "Automation"]
        ),
        guardrail_rules=[
            "Rejects tools that do not offer API access or self-serve onboarding.",
            "Willing to pay premium if it saves engineering hours."
        ]
    ),
    Persona(
        id="p_03_retailer_david",
        name="David Miller",
        demographics=Demographics(
            age=58,
            occupation="Local Retail Store Owner [The Cautious Novice]",
            income_bracket="Mid-Low",
            tech_literacy=2
        ),
        psychographics=Psychographics(
            patience_score=2,
            skepticism_score=9,
            price_ceiling_monthly=15.0,
            primary_pain_point="Confused by complex tech jargon; fears data leaks and broken setups.",
            core_values=["Simplicity", "Human Support", "Trust"]
        ),
        guardrail_rules=[
            "Rejects tools using heavy technical jargon (e.g. API, Webhooks, Vector DB).",
            "Requires simple 1-click UI and phone support."
        ]
    ),
    Persona(
        id="p_04_compliance_elena",
        name="Elena Rostova",
        demographics=Demographics(
            age=46,
            occupation="Enterprise Risk Manager [The Devil's Advocate]",
            income_bracket="Enterprise",
            tech_literacy=7
        ),
        psychographics=Psychographics(
            patience_score=6,
            skepticism_score=9,
            price_ceiling_monthly=500.0,
            primary_pain_point="Fears regulatory fines, unvetted AI models, and lack of SOC2 audit logs.",
            core_values=["Security", "Compliance", "Auditability"]
        ),
        guardrail_rules=[
            "Must reject any product storing unencrypted customer PII.",
            "Prioritizes SOC2 Type II compliance and SSO integrations above feature list."
        ]
    ),
    Persona(
        id="p_05_freelancer_marcus",
        name="Marcus Vance",
        demographics=Demographics(
            age=23,
            occupation="Freelance Designer [The Freemium Enthusiast]",
            income_bracket="Low",
            tech_literacy=8
        ),
        psychographics=Psychographics(
            patience_score=4,
            skepticism_score=5,
            price_ceiling_monthly=0.0,
            primary_pain_point="Cannot afford paid subscriptions; demands a generous free tier.",
            core_values=["Freemium", "Instant Gratification", "Visual Quality"]
        ),
        guardrail_rules=[
            "Rejects any product requiring a credit card up front for free trial.",
            "Strictly demands a forever-free plan."
        ]
    )
]
