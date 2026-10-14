from v3.persona_schema_v3 import (
    PersonaV3, Demographics, Psychographics, Capabilities,
    CulturalMindset, SocialProofAndNetwork, CognitiveFriction
)

# 5 MECE Indian Personas (V3 Mental Accounting Architecture)
# Grounded in Bain & Co "How India Shops Online" (2024), PwC India Consumer Survey, and NPCI/BCG Studies.

INDIAN_PERSONAS_V3 = [
    PersonaV3(
        id="p_in_v3_01_ramesh",
        name="Ramesh Patel",
        population_weight=0.35,  # 35% Tier-2/3 Mass Market Business
        demographics=Demographics(
            age=48,
            occupation="Kirana Store Owner [The Value Auditor]",
            income_bracket="₹6-8 LPA",
            tech_literacy=5,
            geography="India",
            city_tier="Tier-2 (Indore)"
        ),
        capabilities=Capabilities(
            primary_payment="UPI (PhonePe/Paytm) & Cash on Delivery (COD)",
            digital_auth="Mobile OTP (Prefers SMS/WhatsApp)",
            mobility="Two-Wheeler (Petrol Honda Activa)",
            e_commerce_freq=4,
            language_pref="Hindi / Vernacular UI",
            device_connectivity_tier="Budget 4G Smartphone (₹12,000)"
        ),
        psychographics=Psychographics(
            patience_score=4,
            skepticism_score=7,
            price_ceiling_monthly=500.0,
            primary_pain_point="Hates hidden processing fees, non-refundable UPI failures, and lack of COD.",
            core_values=["Price Transparency", "Cash Flow Reliability", "Working Capital Liquidity"],
            status_quo_inertia=7,
            loss_aversion_bias=2.2,
            system_1_habit_strength=8,
            financial_literacy=9,                    # Shrewd merchant: understands cash-flow math, margins, and credit
            liquidity_cash_flow_preference=8          # Thaler: strongly prefers keeping cash in hand today
        ),
        cultural_mindset=CulturalMindset(
            traditionalism_score=8,
            openness_to_experience=5,
            ritual_sanctity_sensitivity=8,
            political_cultural_leaning="Traditionalist / Centrist"
        ),
        social_network=SocialProofAndNetwork(
            network_social_proof_threshold=7,
            word_of_mouth_dependence=8
        ),
        cognitive_friction=CognitiveFriction(
            cognitive_bandwidth_scarcity=6,
            household_decision_autonomy=8,
            capital_asset_lock_in=5,
            human_recourse_requirement=8,
            formalization_paper_trail_anxiety=5
        ),
        guardrail_rules=[
            "Reject hidden processing fees, recurring auto-debit traps, or mandatory credit card annual fees.",
            "Welcome transparent zero-cost cash-flow options on UPI or debit that preserve shop working capital."
        ]
    ),
    PersonaV3(
        id="p_in_v3_02_priya",
        name="Priya Sharma",
        population_weight=0.25,  # 25% Urban Tier-1 Tech Professional
        demographics=Demographics(
            age=31,
            occupation="Senior Tech Product Manager [The Pragmatic Optimizer]",
            income_bracket="₹22-28 LPA",
            tech_literacy=9,
            geography="India",
            city_tier="Tier-1 Metro (Bangalore)"
        ),
        capabilities=Capabilities(
            primary_payment="UPI (Google Pay) & HDFC Rewards Credit Card",
            digital_auth="Google SSO / One-Tap Biometric OTP",
            mobility="Personal Sedan / Uber & Cab Aggregators",
            e_commerce_freq=16,
            language_pref="English",
            device_connectivity_tier="Flagship 5G iPhone"
        ),
        psychographics=Psychographics(
            patience_score=2,
            skepticism_score=3,
            price_ceiling_monthly=3500.0,
            primary_pain_point="Frustrated by inefficient manual processes, slow checkout, and lack of self-serve controls.",
            core_values=["Maximum Speed", "One-Click Convenience", "Time Optimization"],
            status_quo_inertia=3,
            loss_aversion_bias=1.2,
            system_1_habit_strength=5,
            financial_literacy=8,
            liquidity_cash_flow_preference=6          # Optimizes credit card rewards and 0% EMI on electronics
        ),
        cultural_mindset=CulturalMindset(
            traditionalism_score=2,
            openness_to_experience=9,
            ritual_sanctity_sensitivity=2,
            political_cultural_leaning="Cosmopolitan / Progressive"
        ),
        social_network=SocialProofAndNetwork(
            network_social_proof_threshold=2,
            word_of_mouth_dependence=3
        ),
        cognitive_friction=CognitiveFriction(
            cognitive_bandwidth_scarcity=4,
            household_decision_autonomy=10,
            capital_asset_lock_in=2,
            human_recourse_requirement=2,
            formalization_paper_trail_anxiety=1
        ),
        guardrail_rules=[
            "Refuse products requiring mandatory phone sales or manual demo calls.",
            "Regularly utilize 0% No-Cost EMI on existing credit cards for electronics (₹15,000+) to keep funds invested in liquid mutual funds.",
            "Use online video consults for common ailments, but visit hospital specialists for emergencies."
        ]
    ),
    PersonaV3(
        id="p_in_v3_03_ananya",
        name="Ananya Das",
        population_weight=0.20,  # 20% Gen-Z Student & Creator
        demographics=Demographics(
            age=21,
            occupation="Design Student & Creator [The Bargain Explorer]",
            income_bracket="₹2.5-4 LPA (Pocket Money & Freelance)",
            tech_literacy=8,
            geography="India",
            city_tier="Tier-1 Metro (Pune)"
        ),
        capabilities=Capabilities(
            primary_payment="UPI (Paytm/Google Pay)",
            digital_auth="WhatsApp OTP / Social Login",
            mobility="Public Metro / Electric 2-Wheeler Shared",
            e_commerce_freq=12,
            language_pref="English / Hinglish",
            device_connectivity_tier="Mid-range 5G Smartphone"
        ),
        psychographics=Psychographics(
            patience_score=6,
            skepticism_score=4,
            price_ceiling_monthly=400.0,
            primary_pain_point="Cannot afford high upfront commitment; hates hidden subscription auto-debits.",
            core_values=["Affordability", "Student Discounts", "Social Aesthetics"],
            status_quo_inertia=4,
            loss_aversion_bias=1.5,
            system_1_habit_strength=6,
            financial_literacy=6,
            liquidity_cash_flow_preference=9          # Tight pocket money: loves zero-interest monthly splits!
        ),
        cultural_mindset=CulturalMindset(
            traditionalism_score=3,
            openness_to_experience=8,
            ritual_sanctity_sensitivity=3,
            political_cultural_leaning="Progressive / Creative"
        ),
        social_network=SocialProofAndNetwork(
            network_social_proof_threshold=4,
            word_of_mouth_dependence=7
        ),
        cognitive_friction=CognitiveFriction(
            cognitive_bandwidth_scarcity=3,
            household_decision_autonomy=5,
            capital_asset_lock_in=2,
            human_recourse_requirement=4,
            formalization_paper_trail_anxiety=2
        ),
        guardrail_rules=[
            "Reject mandatory credit-card-only paywalls without UPI.",
            "Actively embrace zero-cost installments or student discounts to manage pocket money."
        ]
    ),
    PersonaV3(
        id="p_in_v3_04_suresh",
        name="Suresh Verma",
        population_weight=0.10,  # 10% Senior Government Admin
        demographics=Demographics(
            age=54,
            occupation="Senior Government Admin Officer [The Risk Auditor]",
            income_bracket="₹14-18 LPA",
            tech_literacy=4,
            geography="India",
            city_tier="Tier-2 (Bhopal)"
        ),
        capabilities=Capabilities(
            primary_payment="Net Banking (SBI) & Debit Card / Cash",
            digital_auth="SMS OTP only",
            mobility="Public Transit / State Car / Petrol Two-Wheeler",
            e_commerce_freq=2,
            language_pref="Hindi / English",
            device_connectivity_tier="Standard 4G Smartphone"
        ),
        psychographics=Psychographics(
            patience_score=7,
            skepticism_score=8,
            price_ceiling_monthly=800.0,
            primary_pain_point="Terrified of digital fraud, phishing links, unverified apps, and data theft.",
            core_values=["Security First", "PSU Brand Trust", "Physical Verification"],
            status_quo_inertia=8,
            loss_aversion_bias=2.4,
            system_1_habit_strength=8,
            financial_literacy=8,                    # Government officer: knows formal finance and banking terms
            liquidity_cash_flow_preference=6
        ),
        cultural_mindset=CulturalMindset(
            traditionalism_score=8,
            openness_to_experience=3,
            ritual_sanctity_sensitivity=8,
            political_cultural_leaning="Institutionalist / Conservative"
        ),
        social_network=SocialProofAndNetwork(
            network_social_proof_threshold=8,
            word_of_mouth_dependence=7
        ),
        cognitive_friction=CognitiveFriction(
            cognitive_bandwidth_scarcity=5,
            household_decision_autonomy=9,
            capital_asset_lock_in=6,
            human_recourse_requirement=9,
            formalization_paper_trail_anxiety=1
        ),
        guardrail_rules=[
            "Reject any third-party app asking for invasive permissions or non-bank digital credit.",
            "Always prefer verified government or PSU institutions (SBI, LIC) over unknown startups."
        ]
    ),
    PersonaV3(
        id="p_in_v3_05_kavita",
        name="Kavita Reddy",
        population_weight=0.10,  # 10% Independent Professional
        demographics=Demographics(
            age=42,
            occupation="Independent Architect [The Quality Auditor]",
            income_bracket="₹18-24 LPA",
            tech_literacy=6,
            geography="India",
            city_tier="Tier-1 Metro (Hyderabad)"
        ),
        capabilities=Capabilities(
            primary_payment="UPI & Corporate Credit Card",
            digital_auth="Biometric / Mobile OTP",
            mobility="Personal SUV",
            e_commerce_freq=8,
            language_pref="English",
            device_connectivity_tier="Flagship 5G"
        ),
        psychographics=Psychographics(
            patience_score=5,
            skepticism_score=6,
            price_ceiling_monthly=2500.0,
            primary_pain_point="Hates poor build quality, bad service warranties, and substandard materials.",
            core_values=["Build Quality", "Reliable Service", "Professional Accountability"],
            status_quo_inertia=6,
            loss_aversion_bias=1.9,
            system_1_habit_strength=6,
            financial_literacy=9,
            liquidity_cash_flow_preference=6
        ),
        cultural_mindset=CulturalMindset(
            traditionalism_score=5,
            openness_to_experience=6,
            ritual_sanctity_sensitivity=5,
            political_cultural_leaning="Pragmatic Independent"
        ),
        social_network=SocialProofAndNetwork(
            network_social_proof_threshold=6,
            word_of_mouth_dependence=6
        ),
        cognitive_friction=CognitiveFriction(
            cognitive_bandwidth_scarcity=4,
            household_decision_autonomy=9,
            capital_asset_lock_in=4,
            human_recourse_requirement=7,
            formalization_paper_trail_anxiety=2
        ),
        guardrail_rules=[
            "Never purchase products lacking transparent warranty terms or verified service centers.",
            "Value long-term reliability and build quality over cheap gimmicks."
        ]
    )
]
