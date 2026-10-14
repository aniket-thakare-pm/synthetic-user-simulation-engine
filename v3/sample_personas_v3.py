from v3.persona_schema_v3 import (
    PersonaV3, Demographics, Psychographics, Capabilities,
    CulturalMindset, SocialProofAndNetwork, CognitiveFriction
)

# 5 MECE US General Consumer Personas (V3 Architecture)
# Calibrated for digital media subscriptions, e-commerce checkout, and financial services.

SAMPLE_PERSONAS_V3 = [
    PersonaV3(
        id="p_us_v3_01_accountant_sarah",
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
            financial_literacy=9,
            liquidity_cash_flow_preference=7
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
            "If total subscription price exceeds $25/month, immediately flag as overpriced and cancel/churn."
        ]
    ),
    PersonaV3(
        id="p_us_v3_02_tech_alex",
        name="Alex Rivera",
        population_weight=0.20,
        demographics=Demographics(
            age=29,
            occupation="Full-Stack Developer [The Speed Optimizer]",
            income_bracket="High ($130k/yr)",
            tech_literacy=9,
            geography="US",
            city_tier="Urban Metro"
        ),
        capabilities=Capabilities(
            primary_payment="Apple Pay / Autofill Credit Card",
            digital_auth="1Password / Passkeys / Google SSO",
            mobility="Bicycle / Public Transit / Uber",
            e_commerce_freq=18,
            language_pref="English",
            device_connectivity_tier="Flagship 5G iPhone"
        ),
        psychographics=Psychographics(
            patience_score=1,
            skepticism_score=3,
            price_ceiling_monthly=120.0,
            primary_pain_point="Cannot stand clunky checkout flows, unskippable ads, or manual address forms.",
            core_values=["Speed", "Minimalist UX", "Ad-Free Experience"],
            status_quo_inertia=2,
            loss_aversion_bias=1.1,
            system_1_habit_strength=3,
            financial_literacy=8,
            liquidity_cash_flow_preference=4
        ),
        cultural_mindset=CulturalMindset(
            traditionalism_score=2,
            openness_to_experience=9,
            ritual_sanctity_sensitivity=1,
            political_cultural_leaning="Progressive Urban"
        ),
        social_network=SocialProofAndNetwork(
            network_social_proof_threshold=2,
            word_of_mouth_dependence=2
        ),
        cognitive_friction=CognitiveFriction(
            cognitive_bandwidth_scarcity=3,
            household_decision_autonomy=10,
            capital_asset_lock_in=1,
            human_recourse_requirement=1,
            formalization_paper_trail_anxiety=1
        ),
        guardrail_rules=[
            "Never tolerate ad-supported tiers if an ad-free premium tier is available.",
            "Abandon any purchase that requires creating a new account if guest checkout exists."
        ]
    ),
    PersonaV3(
        id="p_us_v3_03_retiree_david",
        name="David Miller",
        population_weight=0.20,
        demographics=Demographics(
            age=68,
            occupation="Retired Teacher [The Risk Avoider]",
            income_bracket="Fixed ($45k/yr)",
            tech_literacy=3,
            geography="US",
            city_tier="Small Town"
        ),
        capabilities=Capabilities(
            primary_payment="Physical Visa Card (Types manually)",
            digital_auth="Email + Simple Password on Notebook",
            mobility="Personal Sedan",
            e_commerce_freq=2,
            language_pref="English",
            device_connectivity_tier="Older iPad / 4G Android Phone"
        ),
        psychographics=Psychographics(
            patience_score=6,
            skepticism_score=9,
            price_ceiling_monthly=15.0,
            primary_pain_point="Terrified of recurring charges, accidentally clicking the wrong button, or online fraud.",
            core_values=["Security", "Phone Support", "Predictability"],
            status_quo_inertia=8,
            loss_aversion_bias=2.4,
            system_1_habit_strength=8,
            financial_literacy=7,
            liquidity_cash_flow_preference=8
        ),
        cultural_mindset=CulturalMindset(
            traditionalism_score=8,
            openness_to_experience=2,
            ritual_sanctity_sensitivity=6,
            political_cultural_leaning="Traditionalist"
        ),
        social_network=SocialProofAndNetwork(
            network_social_proof_threshold=7,
            word_of_mouth_dependence=8
        ),
        cognitive_friction=CognitiveFriction(
            cognitive_bandwidth_scarcity=6,
            household_decision_autonomy=7,
            capital_asset_lock_in=5,
            human_recourse_requirement=9,
            formalization_paper_trail_anxiety=2
        ),
        guardrail_rules=[
            "Refuse any subscription that makes cancellation difficult or hides phone support.",
            "Immediately cancel if an unexpected price increase is charged to credit card."
        ]
    ),
    PersonaV3(
        id="p_us_v3_04_parent_elena",
        name="Elena Rostova",
        population_weight=0.20,
        demographics=Demographics(
            age=36,
            occupation="Nurse & Working Mother [The Pragmatic Caregiver]",
            income_bracket="Mid-Upper ($85k/yr)",
            tech_literacy=6,
            geography="US",
            city_tier="Suburban Metro"
        ),
        capabilities=Capabilities(
            primary_payment="Debit Card / Apple Pay",
            digital_auth="FaceID / Mobile SMS",
            mobility="Minivan",
            e_commerce_freq=12,
            language_pref="English",
            device_connectivity_tier="iPhone 13 (5G)"
        ),
        psychographics=Psychographics(
            patience_score=3,
            skepticism_score=5,
            price_ceiling_monthly=40.0,
            primary_pain_point="Exhausted after 12-hour shifts; needs family entertainment that just works without micro-managing.",
            core_values=["Family Utility", "Reliability", "Time Savings"],
            status_quo_inertia=5,
            loss_aversion_bias=1.6,
            system_1_habit_strength=6,
            financial_literacy=7,
            liquidity_cash_flow_preference=6
        ),
        cultural_mindset=CulturalMindset(
            traditionalism_score=5,
            openness_to_experience=5,
            ritual_sanctity_sensitivity=4,
            political_cultural_leaning="Moderate Pragmatic"
        ),
        social_network=SocialProofAndNetwork(
            network_social_proof_threshold=5,
            word_of_mouth_dependence=6
        ),
        cognitive_friction=CognitiveFriction(
            cognitive_bandwidth_scarcity=8,
            household_decision_autonomy=8,
            capital_asset_lock_in=4,
            human_recourse_requirement=5,
            formalization_paper_trail_anxiety=1
        ),
        guardrail_rules=[
            "Keep subscriptions that kids use daily unless the price hike exceeds $5/month.",
            "Downgrade to ad-supported plans if household streaming budget exceeds $50/month."
        ]
    ),
    PersonaV3(
        id="p_us_v3_05_student_marcus",
        name="Marcus Chen",
        population_weight=0.15,
        demographics=Demographics(
            age=20,
            occupation="Undergraduate Student [The Budget Streamer]",
            income_bracket="Low (<$15k/yr)",
            tech_literacy=9,
            geography="US",
            city_tier="College Town"
        ),
        capabilities=Capabilities(
            primary_payment="Venmo Debit / PayPal / Apple Cash",
            digital_auth="Passkey / Social Login",
            mobility="Bicycle / Campus Shuttle",
            e_commerce_freq=8,
            language_pref="English",
            device_connectivity_tier="5G Smartphone"
        ),
        psychographics=Psychographics(
            patience_score=4,
            skepticism_score=6,
            price_ceiling_monthly=10.0,
            primary_pain_point="Zero tolerance for expensive monthly plans; cycles subscriptions depending on current releases.",
            core_values=["Maximum Thrift", "Ad-Tier Acceptance", "Flexibility"],
            status_quo_inertia=3,
            loss_aversion_bias=1.3,
            system_1_habit_strength=3,
            financial_literacy=6,
            liquidity_cash_flow_preference=9
        ),
        cultural_mindset=CulturalMindset(
            traditionalism_score=2,
            openness_to_experience=8,
            ritual_sanctity_sensitivity=1,
            political_cultural_leaning="Progressive"
        ),
        social_network=SocialProofAndNetwork(
            network_social_proof_threshold=3,
            word_of_mouth_dependence=5
        ),
        cognitive_friction=CognitiveFriction(
            cognitive_bandwidth_scarcity=4,
            household_decision_autonomy=10,
            capital_asset_lock_in=1,
            human_recourse_requirement=2,
            formalization_paper_trail_anxiety=1
        ),
        guardrail_rules=[
            "Instantly cancel paid streaming upon any $2+ price increase or switch to free ad-supported tiers.",
            "Share accounts or seek student discounts whenever available."
        ]
    )
]
