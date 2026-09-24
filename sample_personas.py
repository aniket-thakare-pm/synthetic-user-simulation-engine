from persona_schema import Persona, Demographics, Psychographics, Capabilities

# 5 MECE Behavioral Mindset Personas (Global / US General Panel)
SAMPLE_PERSONAS = [
    Persona(
        id="p_01_accountant_sarah",
        name="Sarah Jenkins",
        population_weight=0.25,
        demographics=Demographics(
            age=42,
            occupation="Senior Accountant [The Value Auditor]",
            income_bracket="Mid ($65k/yr)",
            tech_literacy=4,
            geography="US",
            city_tier="Suburban"
        ),
        capabilities=Capabilities(
            primary_payment="Credit Card / Apple Pay",
            digital_auth="Email + Password / Guest Checkout",
            mobility="Personal SUV / Car",
            e_commerce_freq=6,
            language_pref="English",
            device_connectivity_tier="Mid-range 5G Smartphone"
        ),
        psychographics=Psychographics(
            patience_score=3,
            skepticism_score=8,
            price_ceiling_monthly=25.0,
            primary_pain_point="Hates hidden costs, sudden price hikes, and unannounced subscription fees.",
            core_values=["Clarity", "Budget Control", "Price Transparency"],
            status_quo_inertia=4,
            loss_aversion_bias=1.8,
            system_1_habit_strength=4,
            privacy_data_sensitivity=8,
            financial_literacy=9
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
            income_bracket="High ($140k/yr)",
            tech_literacy=9,
            geography="US",
            city_tier="Urban Metro (SF)"
        ),
        capabilities=Capabilities(
            primary_payment="Corporate Credit Card / Apple Pay",
            digital_auth="Google SSO / 1-Click Passkey",
            mobility="Rideshare (Uber) & Metro",
            e_commerce_freq=14,
            language_pref="English",
            device_connectivity_tier="Flagship 5G (iPhone 15 Pro)"
        ),
        psychographics=Psychographics(
            patience_score=7,
            skepticism_score=6,
            price_ceiling_monthly=99.0,
            primary_pain_point="Wastes time on manual tasks, waiting in lines, or friction-heavy onboarding.",
            core_values=["Speed", "Time Efficiency", "Automation"],
            status_quo_inertia=8,
            loss_aversion_bias=2.5,
            system_1_habit_strength=8,
            privacy_data_sensitivity=5,
            financial_literacy=8
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
            income_bracket="Mid-Low ($45k/yr)",
            tech_literacy=2,
            geography="US",
            city_tier="Small Town / Rural"
        ),
        capabilities=Capabilities(
            primary_payment="Debit Card / Guest Checkout",
            digital_auth="Phone Number / Simple Password",
            mobility="Personal Pickup Truck",
            e_commerce_freq=3,
            language_pref="English",
            device_connectivity_tier="Budget 4G Smartphone"
        ),
        psychographics=Psychographics(
            patience_score=2,
            skepticism_score=9,
            price_ceiling_monthly=15.0,
            primary_pain_point="Confused by complex jargon, multi-step instructions, and lack of human support.",
            core_values=["Simplicity", "Human Support", "Trust"],
            status_quo_inertia=9,
            loss_aversion_bias=2.5,
            system_1_habit_strength=9,
            privacy_data_sensitivity=9,
            financial_literacy=5
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
            income_bracket="Enterprise ($180k/yr)",
            tech_literacy=7,
            geography="US",
            city_tier="Suburban Metro"
        ),
        capabilities=Capabilities(
            primary_payment="Corporate Card / Wire Transfer",
            digital_auth="Okta SSO / Hardware Token 2FA",
            mobility="Personal Luxury Sedan",
            e_commerce_freq=8,
            language_pref="English",
            device_connectivity_tier="Flagship 5G Smartphone"
        ),
        psychographics=Psychographics(
            patience_score=6,
            skepticism_score=9,
            price_ceiling_monthly=500.0,
            primary_pain_point="Fears unvetted risks, poor quality controls, and lack of safety/compliance audits.",
            core_values=["Security", "Quality Control", "Auditability"],
            status_quo_inertia=5,
            loss_aversion_bias=2.0,
            system_1_habit_strength=3,
            privacy_data_sensitivity=10,
            financial_literacy=9
        ),
        guardrail_rules=[
            "Reject options lacking clear security credentials, SOC2 compliance, or data encryption.",
            "Always question unverified claims or missing third-party audit reports."
        ]
    ),
    Persona(
        id="p_05_freelancer_marcus",
        name="Marcus Vance",
        population_weight=0.10,
        demographics=Demographics(
            age=24,
            occupation="Freelance Designer [The Bargain Explorer]",
            income_bracket="Low ($32k/yr)",
            tech_literacy=8,
            geography="US",
            city_tier="Urban Metro"
        ),
        capabilities=Capabilities(
            primary_payment="PayPal / Apple Pay",
            digital_auth="Google / Apple SSO",
            mobility="Bicycle & Rideshare",
            e_commerce_freq=10,
            language_pref="English",
            device_connectivity_tier="Upper Mid-range 5G Smartphone"
        ),
        psychographics=Psychographics(
            patience_score=5,
            skepticism_score=4,
            price_ceiling_monthly=12.0,
            primary_pain_point="Strict budget limitations; active deal-seeker unwilling to pay full price.",
            core_values=["Affordability", "Discounts", "Flexibility"],
            status_quo_inertia=3,
            loss_aversion_bias=1.5,
            system_1_habit_strength=4,
            privacy_data_sensitivity=4,
            financial_literacy=6
        ),
        guardrail_rules=[
            "Reject subscriptions that lack a free tier or trial period.",
            "Actively seek promo codes, student pricing, or alternative free open-source tools."
        ]
    )
]
