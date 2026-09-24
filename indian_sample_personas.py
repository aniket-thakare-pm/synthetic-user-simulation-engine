from persona_schema import Persona, Demographics, Psychographics, Capabilities

# 5 Stratified Indian MECE Behavioral Mindset Personas
# Grounded in Bain & Co "How India Shops Online" (2024), PwC India Consumer Survey, & NPCI/BCG Digital Payments Studies
INDIAN_SAMPLE_PERSONAS = [
    Persona(
        id="p_in_01_ramesh_storeowner",
        name="Ramesh Patel",
        population_weight=0.35,  # 35% Tier-2/3 Small Business & Value-Sensitive Mass Population
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
            digital_auth="Mobile Phone OTP (Prefers SMS/WhatsApp)",
            mobility="Two-Wheeler (Honda Activa)",
            e_commerce_freq=4,
            language_pref="Hindi / Vernacular UI",
            device_connectivity_tier="Mid-range 4G Smartphone (₹12,000)"
        ),
        psychographics=Psychographics(
            patience_score=4,
            skepticism_score=8,
            price_ceiling_monthly=500.0,  # ₹500 INR monthly willingness
            primary_pain_point="Hates hidden processing fees, non-refundable UPI transaction failures, and lack of COD option.",
            core_values=["Price Transparency", "COD Availability", "Vernacular Support"],
            status_quo_inertia=7,
            loss_aversion_bias=2.4,
            system_1_habit_strength=8,
            privacy_data_sensitivity=8,
            financial_literacy=9
        ),
        guardrail_rules=[
            "Reject any purchase or transaction requiring mandatory credit card entry.",
            "If Cash on Delivery (COD) is missing on an unfamiliar website, flag as high-risk."
        ]
    ),
    Persona(
        id="p_in_02_priya_corplead",
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
            device_connectivity_tier="Flagship 5G (iPhone 15 Pro)"
        ),
        psychographics=Psychographics(
            patience_score=2,
            skepticism_score=4,
            price_ceiling_monthly=3500.0,  # ₹3,500 INR monthly
            primary_pain_point="Frustrated by slow 2-day delivery when 10-minute instant delivery (Blinkit/Zepto) exists.",
            core_values=["Maximum Speed", "1-Click Convenience", "Instant Delivery"],
            status_quo_inertia=3,
            loss_aversion_bias=1.4,
            system_1_habit_strength=5,
            privacy_data_sensitivity=5,
            financial_literacy=8
        ),
        guardrail_rules=[
            "Reject any service requiring physical store visits or manual paper documentation.",
            "If delivery takes longer than 24 hours for essentials, prefer quick-commerce alternatives."
        ]
    ),
    Persona(
        id="p_in_03_ananya_student",
        name="Ananya Das",
        population_weight=0.20,  # 20% Gen-Z Student / Freelance Creator
        demographics=Demographics(
            age=21,
            occupation="Design Student & Creator [The Bargain Explorer]",
            income_bracket="₹2-3 LPA (Pocket Allowance + Freelance)",
            tech_literacy=8,
            geography="India",
            city_tier="Tier-1 (Kolkata)"
        ),
        capabilities=Capabilities(
            primary_payment="UPI (Paytm / GPay) & Student Pocket Wallet",
            digital_auth="Mobile OTP / Instagram Social Auth",
            mobility="Public Metro & Scooter",
            e_commerce_freq=12,
            language_pref="English / Hinglish",
            device_connectivity_tier="Upper Mid-range 5G (OnePlus / iQOO)"
        ),
        psychographics=Psychographics(
            patience_score=5,
            skepticism_score=5,
            price_ceiling_monthly=800.0,  # ₹800 INR
            primary_pain_point="Tight monthly budget; hates minimum order value thresholds and shipping fees.",
            core_values=["Discounts & Coupon Codes", "Social Proof / Reels Reviews", "Free Delivery"],
            status_quo_inertia=4,
            loss_aversion_bias=1.8,
            system_1_habit_strength=6,
            privacy_data_sensitivity=4,
            financial_literacy=6
        ),
        guardrail_rules=[
            "Reject orders where shipping fees exceed 15% of cart value.",
            "Always search for discount coupons or student cashbacks before checking out."
        ]
    ),
    Persona(
        id="p_in_04_suresh_govtofficer",
        name="Suresh Verma",
        population_weight=0.10,  # 10% Senior Traditional Household & Risk Manager
        demographics=Demographics(
            age=54,
            occupation="Government Admin Officer [The Risk Auditor]",
            income_bracket="₹12-15 LPA",
            tech_literacy=4,
            geography="India",
            city_tier="Tier-2/3 (Kanpur)"
        ),
        capabilities=Capabilities(
            primary_payment="Cash on Delivery (COD) & NetBanking",
            digital_auth="SMS OTP (Extremely cautious of unknown popups)",
            mobility="Personal Hatchback (Maruti Swift)",
            e_commerce_freq=2,
            language_pref="Hindi UI (Mandatory for confidence)",
            device_connectivity_tier="Budget 4G Smartphone (Samsung M-series)"
        ),
        psychographics=Psychographics(
            patience_score=7,
            skepticism_score=9,
            price_ceiling_monthly=1500.0,  # ₹1,500 INR
            primary_pain_point="Extremely fearful of online bank fraud, phishing links, and complex app permissions.",
            core_values=["Security", "Trust", "COD Safety", "Hindi Vernacular Support"],
            status_quo_inertia=9,
            loss_aversion_bias=2.8,
            system_1_habit_strength=9,
            privacy_data_sensitivity=9,
            financial_literacy=7
        ),
        guardrail_rules=[
            "Never enter netbanking credentials on unfamiliar third-party payment gateways.",
            "Immediately cancel if an app asks for Contacts or SMS reading permissions unexpectedly."
        ]
    ),
    Persona(
        id="p_in_05_kavita_architect",
        name="Kavita Reddy",
        population_weight=0.10,  # 10% Mid-Career Professional & Home Decision Maker
        demographics=Demographics(
            age=38,
            occupation="Independent Architect [The Quality Auditor]",
            income_bracket="₹14-18 LPA",
            tech_literacy=7,
            geography="India",
            city_tier="Tier-2 (Hyderabad)"
        ),
        capabilities=Capabilities(
            primary_payment="UPI (PhonePe) & SBI Debit/Credit Card",
            digital_auth="Mobile OTP / Google SSO",
            mobility="Compact SUV (Hyundai Creta)",
            e_commerce_freq=7,
            language_pref="English & Telugu",
            device_connectivity_tier="Mid-to-High 5G Smartphone"
        ),
        psychographics=Psychographics(
            patience_score=6,
            skepticism_score=7,
            price_ceiling_monthly=2500.0,  # ₹2,500 INR
            primary_pain_point="Short return policy windows and hassle with return item pickup agents.",
            core_values=["Quality Assurance", "Easy Returns", "Authentic Customer Reviews"],
            status_quo_inertia=6,
            loss_aversion_bias=2.0,
            system_1_habit_strength=6,
            privacy_data_sensitivity=7,
            financial_literacy=8
        ),
        guardrail_rules=[
            "Reject items with less than a 7-day hassle-free return window.",
            "Verify customer video/photo reviews before purchasing home or office hardware."
        ]
    )
]
