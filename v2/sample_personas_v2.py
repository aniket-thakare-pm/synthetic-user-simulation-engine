from v2.persona_schema_v2 import (
    PersonaV2, Demographics, Psychographics, Capabilities,
    CulturalMindset, SocialProofAndNetwork, CognitiveFriction
)

# 5 MECE US General Consumer Personas (V2 Architecture)
# Calibrated for consumer subscriptions, digital entertainment, and e-commerce.

SAMPLE_PERSONAS_V2 = [
    PersonaV2(
        id="p_v2_01_accountant_sarah",
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
            system_1_habit_strength=4
        ),
        cultural_mindset=CulturalMindset(
            traditionalism_score=5,
            openness_to_experience=4,
            ritual_sanctity_sensitivity=3,
            political_cultural_leaning="Pragmatic Suburban"
        ),
        social_network=SocialProofAndNetwork(
            network_social_proof_threshold=4,
            word_of_mouth_dependence=4
        ),
        cognitive_friction=CognitiveFriction(
            cognitive_bandwidth_scarcity=5,
            household_decision_autonomy=8,
            capital_asset_lock_in=3,
            human_recourse_requirement=4,
            formalization_paper_trail_anxiety=1
        ),
        guardrail_rules=[
            "Reject any product or service requiring mandatory sales calls for pricing.",
            "If total subscription price exceeds $25/month, immediately flag as overpriced and unjustified."
        ]
    ),
    PersonaV2(
        id="p_v2_02_founder_alex",
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
            system_1_habit_strength=8
        ),
        cultural_mindset=CulturalMindset(
            traditionalism_score=2,
            openness_to_experience=9,
            ritual_sanctity_sensitivity=1,
            political_cultural_leaning="Techno-Optimist / Progressive"
        ),
        social_network=SocialProofAndNetwork(
            network_social_proof_threshold=2,
            word_of_mouth_dependence=2
        ),
        cognitive_friction=CognitiveFriction(
            cognitive_bandwidth_scarcity=3,
            household_decision_autonomy=10,
            capital_asset_lock_in=2,
            human_recourse_requirement=1,
            formalization_paper_trail_anxiety=1
        ),
        guardrail_rules=[
            "Rejects products that do not offer instant self-service or fast onboarding.",
            "Willing to pay a premium if it saves time or automates manual effort."
        ]
    ),
    PersonaV2(
        id="p_v2_03_retailer_david",
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
            system_1_habit_strength=9
        ),
        cultural_mindset=CulturalMindset(
            traditionalism_score=8,
            openness_to_experience=2,
            ritual_sanctity_sensitivity=7,
            political_cultural_leaning="Traditionalist / Conservative"
        ),
        social_network=SocialProofAndNetwork(
            network_social_proof_threshold=8,
            word_of_mouth_dependence=8
        ),
        cognitive_friction=CognitiveFriction(
            cognitive_bandwidth_scarcity=7,
            household_decision_autonomy=9,
            capital_asset_lock_in=5,
            human_recourse_requirement=9,
            formalization_paper_trail_anxiety=2
        ),
        guardrail_rules=[
            "You have low tech literacy (2/10). You do NOT read technical terms or privacy fine print.",
            "Rejects options using complex jargon or lack of direct human customer support.",
            "Requires simple 1-step usage and clear, straightforward value."
        ]
    ),
    PersonaV2(
        id="p_v2_04_compliance_elena",
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
            system_1_habit_strength=3
        ),
        cultural_mindset=CulturalMindset(
            traditionalism_score=4,
            openness_to_experience=6,
            ritual_sanctity_sensitivity=4,
            political_cultural_leaning="Pragmatic Independent"
        ),
        social_network=SocialProofAndNetwork(
            network_social_proof_threshold=5,
            word_of_mouth_dependence=5
        ),
        cognitive_friction=CognitiveFriction(
            cognitive_bandwidth_scarcity=4,
            household_decision_autonomy=9,
            capital_asset_lock_in=4,
            human_recourse_requirement=6,
            formalization_paper_trail_anxiety=1
        ),
        guardrail_rules=[
            "Reject options lacking clear security credentials, SOC2 compliance, or data encryption.",
            "Always question unverified claims or missing third-party audit reports."
        ]
    ),
    PersonaV2(
        id="p_v2_05_freelancer_marcus",
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
            system_1_habit_strength=4
        ),
        cultural_mindset=CulturalMindset(
            traditionalism_score=2,
            openness_to_experience=8,
            ritual_sanctity_sensitivity=2,
            political_cultural_leaning="Progressive / Independent"
        ),
        social_network=SocialProofAndNetwork(
            network_social_proof_threshold=4,
            word_of_mouth_dependence=5
        ),
        cognitive_friction=CognitiveFriction(
            cognitive_bandwidth_scarcity=3,
            household_decision_autonomy=10,
            capital_asset_lock_in=2,
            human_recourse_requirement=3,
            formalization_paper_trail_anxiety=1
        ),
        guardrail_rules=[
            "Reject subscriptions that lack a free tier or trial period.",
            "Actively seek promo codes, student pricing, or alternative free open-source tools."
        ]
    )
]
