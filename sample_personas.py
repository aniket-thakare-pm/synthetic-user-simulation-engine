from persona_schema import Persona, Demographics, Psychographics

# 5 MECE Behavioral Mindset Personas (Domain-Agnostic with Empirical Behavioral Parameters)
SAMPLE_PERSONAS = [
    Persona(
        id="p_01_accountant_sarah",
        name="Sarah Jenkins",
        population_weight=0.25,
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
            primary_pain_point="Hates hidden costs, sudden price hikes, and unannounced subscription fees.",
            core_values=["Clarity", "Budget Control", "Price Transparency"],
            status_quo_inertia=4,
            loss_aversion_bias=1.8,
            system_1_habit_strength=4
        ),
        guardrail_rules=[
            "Reject any product or service requiring mandatory sales calls for pricing.",
            "If total subscription price exceeds $25/month, immediately flag as overpriced and unjustified."
        ]
    ),
    Persona(
        id="p_02_founder_alex",
        name="Alex Chen",
        population_weight=0.35,
        demographics=Demographics(
            age=29,
            occupation="Startup Founder [The Pragmatic Optimizer]",
            income_bracket="High",
            tech_literacy=9
        ),
        psychographics=Psychographics(
            patience_score=7,
            skepticism_score=6,
            price_ceiling_monthly=99.0,
            primary_pain_point="Wastes time on manual tasks, waiting in lines, or friction-heavy onboarding.",
            core_values=["Speed", "Time Efficiency", "Automation"],
            status_quo_inertia=8,
            loss_aversion_bias=2.5,
            system_1_habit_strength=8
        ),
        guardrail_rules=[
            "Rejects products that do not offer instant self-service or fast onboarding.",
            "Willing to pay a premium if it saves time or automates manual effort."
        ]
    ),
    Persona(
        id="p_03_retailer_david",
        name="David Miller",
        population_weight=0.25,
        demographics=Demographics(
            age=58,
            occupation="Local Retail Store Owner [The Friction-Sensitive Novice]",
            income_bracket="Mid-Low",
            tech_literacy=2
        ),
        psychographics=Psychographics(
            patience_score=2,
            skepticism_score=9,
            price_ceiling_monthly=15.0,
            primary_pain_point="Confused by complex jargon, multi-step instructions, and lack of human support.",
            core_values=["Simplicity", "Human Support", "Trust"],
            status_quo_inertia=9,
            loss_aversion_bias=2.5,
            system_1_habit_strength=9
        ),
        guardrail_rules=[
            "You have low tech literacy (2/10). You do NOT read technical terms or privacy fine print.",
            "Rejects options using complex jargon or lack of direct human customer support.",
            "Requires simple 1-step usage and clear, straightforward value."
        ]
    ),
    Persona(
        id="p_04_compliance_elena",
        name="Elena Rostova",
        population_weight=0.05,
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
            primary_pain_point="Fears unvetted risks, poor quality controls, and lack of safety/compliance audits.",
            core_values=["Security", "Quality Control", "Auditability"],
            status_quo_inertia=5,
            loss_aversion_bias=2.0,
            system_1_habit_strength=3
        ),
        guardrail_rules=[
            "Actively looks for flaws, hidden risks, or unverified claims in any pitch.",
            "Demands rigorous quality verification and clear risk management."
        ]
    ),
    Persona(
        id="p_05_freelancer_marcus",
        name="Marcus Vance",
        population_weight=0.10,
        demographics=Demographics(
            age=23,
            occupation="Freelance Designer [The Bargain Explorer]",
            income_bracket="Low",
            tech_literacy=8
        ),
        psychographics=Psychographics(
            patience_score=4,
            skepticism_score=5,
            price_ceiling_monthly=0.0,
            primary_pain_point="Cannot afford paid subscriptions; demands zero-cost tiers or free trials.",
            core_values=["Freemium", "Instant Value", "Zero Commitment"],
            status_quo_inertia=3,
            loss_aversion_bias=1.5,
            system_1_habit_strength=3
        ),
        guardrail_rules=[
            "Rejects options requiring an upfront credit card for free trials.",
            "Strictly demands a zero-cost option or generous free tier."
        ]
    )
]
