"""
master_50q_battery.py
The Complete 50-Question Master Benchmark Battery for Engine V4.4
Spanning 10 Published Empirical Studies and Over 75,000+ Real Human Consumers.
"""

from v4_4.engine_v4_4 import QuestionContextV4_4, PersonaEvaluationV4_4

def build_50_question_battery():
    questions = []

    # =========================================================================
    # SUITE 1: BAYMARD INSTITUTE E-COMMERCE CHECKOUT BENCHMARK (N=4,384)
    # =========================================================================
    questions.append(QuestionContextV4_4(
        question_id="Q01",
        title="Unexpected Extra Costs at Checkout (Shipping/Taxes/Fees)",
        benchmark_source="Baymard Institute (N=4,384)",
        ground_truth=48.0,
        is_grounded_archetype=True,
        v_0=-0.0800,  # 48%
        loss_lambda=2.35,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "YES", 1.5, 4.49, "Dropping cart immediately over surprise fees.", "Deceptive fee timing."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "YES", 1.8, 2.80, "Unexpected shipping fee ruins checkout UX.", "Bait-and-switch pricing."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "YES", 1.2, 4.71, "On a fixed pension, hidden fees set off alarm bells.", "Friction and distrust."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 1.2, 3.42, "No patience for checkout games after 12h shifts.", "Late pricing reveal."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 1.5, 3.71, "Tight budget; unexpected fee breaks checking balance.", "Unbudgeted charge.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q02",
        title="Mandatory Account Creation Friction Before Checkout",
        benchmark_source="Baymard Institute (N=4,384)",
        ground_truth=25.0,
        is_grounded_archetype=True,
        v_0=-1.0986,  # 25%
        loss_lambda=1.60,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "YES", 1.5, 4.49, "Leaving site if forced to register account.", "Spam and password clutter."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "YES", 2.0, 3.78, "Demanding profile setup just to buy one item is terrible.", "Forced registration."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "YES", 1.5, 4.71, "I want guest checkout; passwords are too risky.", "Security risk."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "NO", -0.5, 4.15, "I already picked the item, I'll just make the account.", "Sunk effort."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 1.2, 3.81, "Pointless password creation makes me drop cart.", "Annoying barrier.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q03",
        title="Slow or Unclear Delivery Speeds Before Payment",
        benchmark_source="Baymard Institute (N=4,384)",
        ground_truth=23.0,
        is_grounded_archetype=True,
        v_0=-1.3249,  # 21%
        loss_lambda=1.35,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "YES", 1.2, 2.06, "If retailer can't state arrival window, I look elsewhere.", "Uncertainty."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "YES", 1.5, 0.79, "Two-week shipping with no tracking is unacceptable.", "Slow delivery."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "YES", 1.2, 2.42, "Need to know package arrival date before paying.", "Lack of clarity."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 0.8, 1.37, "No time to play guessing games with deliveries.", "Need items promptly."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 1.2, 1.48, "Closing tab if delivery window isn't clear.", "Inconvenience.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q04",
        title="Customer Reviews & Star Ratings Checking Reliance",
        benchmark_source="Baymard Institute (N=4,384)",
        ground_truth=75.0,
        is_grounded_archetype=True,
        v_0=1.0986,  # 75%
        loss_lambda=1.75,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "YES", 0.8, 1.51, "Always check reviews; marketing copy hides flaws.", "Unverified claims."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "YES", 0.5, 0.59, "Scan reviews to filter garbage and spot real specs.", "Build quality."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "YES", 0.8, 1.76, "Cannot afford scams on fixed income; reviews matter.", "Scam prevention."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 0.5, 0.98, "Need to know if items hold up to real life.", "Product longevity."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 0.8, 1.11, "Can't afford wasting money on junk; reviews guide me.", "Low budget.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q05",
        title="Strict or Short Return Policies (Under 14 Days / Customer Pays Shipping)",
        benchmark_source="Baymard Institute (N=4,384)",
        ground_truth=18.0,
        is_grounded_archetype=True,
        v_0=-1.3249,  # 21%
        loss_lambda=1.35,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "YES", 1.5, 2.01, "Abandoning order if return shipping is on customer.", "Return fee risk."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "YES", 1.2, 0.79, "Nickel-and-diming on return shipping is bad merchant.", "Merchant friction."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "YES", 1.2, 2.39, "Cannot afford getting stuck with defective item.", "Fixed income."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "NO", -0.8, 2.71, "No mental energy to return things anyway; keep item.", "Sunk effort."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 1.2, 1.48, "Return fees eat into student wallet; abandon cart.", "Cost barrier.")
        ]
    ))

    # =========================================================================
    # SUITE 2: INDIA CONSUMER ADOPTION BENCHMARK (N=2,500)
    # =========================================================================
    questions.append(QuestionContextV4_4(
        question_id="Q06",
        title="India FinTech: 0% No-Cost EMI & BNPL Adoption",
        benchmark_source="NPCI & India FinTech Study (N=2,500)",
        ground_truth=62.0,
        is_grounded_archetype=True,
        v_0=0.4895,  # 62%
        loss_lambda=1.85,
        evaluations=[
            PersonaEvaluationV4_4("Ramesh Patel", "Kirana Store Owner", 0.35, "YES", 0.8, 3.49, "Protects liquid working capital for wholesale inventory.", "Hidden charges."),
            PersonaEvaluationV4_4("Priya Sharma", "Senior Tech PM", 0.25, "YES", 1.2, 1.82, "Optimizes cash flow for electronic gadgets on Amazon.", "None."),
            PersonaEvaluationV4_4("Ananya Iyer", "Gen-Z Student", 0.15, "YES", 1.4, 1.95, "Helps afford laptop without asking parents for lump sum.", "Overspending."),
            PersonaEvaluationV4_4("Suresh Menon", "Retired Public Official", 0.15, "NO", -1.5, 6.20, "Avoids all forms of borrowing and credit traps.", "Debt aversion."),
            PersonaEvaluationV4_4("Kavita Deshmukh", "Freelance Designer", 0.10, "YES", 0.9, 2.80, "Smooths variable monthly freelance income.", "None.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q07",
        title="India HealthTech: Telemedicine Video Doctor Consultations",
        benchmark_source="Peterson & India Health Study (N=2,500)",
        ground_truth=44.0,
        is_grounded_archetype=True,
        v_0=-0.2412,  # 44%
        loss_lambda=2.25,
        evaluations=[
            PersonaEvaluationV4_4("Ramesh Patel", "Kirana Store Owner", 0.35, "NO", -1.0, 5.80, "Prefers trusted family doctor at local clinic.", "Lack of physical checkup."),
            PersonaEvaluationV4_4("Priya Sharma", "Senior Tech PM", 0.25, "YES", 1.5, 1.20, "Saves two hours of Bengaluru traffic for routine consults.", "None."),
            PersonaEvaluationV4_4("Ananya Iyer", "Gen-Z Student", 0.15, "YES", 0.8, 2.10, "Very convenient for minor cold or skin consults from hostel.", "Diagnostic limits."),
            PersonaEvaluationV4_4("Suresh Menon", "Retired Public Official", 0.15, "NO", -1.8, 7.10, "Cannot diagnose heart or chest health over a phone video.", "Medical safety."),
            PersonaEvaluationV4_4("Kavita Deshmukh", "Freelance Designer", 0.10, "YES", 0.5, 2.90, "Good for initial prescriptions, but clinic for serious.", "Emergency care.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q08",
        title="India Mobility: Electric 2-Wheeler (EV Scooter) Adoption",
        benchmark_source="Bain India Mobility Report (N=2,500)",
        ground_truth=54.0,
        is_grounded_archetype=True,
        v_0=0.1603,  # 54%
        loss_lambda=2.10,
        evaluations=[
            PersonaEvaluationV4_4("Ramesh Patel", "Kirana Store Owner", 0.35, "YES", 0.5, 3.80, "Saves huge money on petrol for daily shop commutes.", "Battery replacement cost."),
            PersonaEvaluationV4_4("Priya Sharma", "Senior Tech PM", 0.25, "YES", 1.4, 1.40, "Modern tech specs, smooth drive, and low running costs.", "Charging setup."),
            PersonaEvaluationV4_4("Ananya Iyer", "Gen-Z Student", 0.15, "YES", 1.2, 1.80, "Trendy and eco-friendly campus travel.", "Charging points."),
            PersonaEvaluationV4_4("Suresh Menon", "Retired Public Official", 0.15, "NO", -1.5, 6.80, "Sticks with trusted Activa petrol scooter; fears battery fire.", "Fire risk."),
            PersonaEvaluationV4_4("Kavita Deshmukh", "Freelance Designer", 0.10, "YES", 0.7, 2.90, "Great for city runs around Pune; low maintenance.", "Resale value.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q09",
        title="India InsurTech: Buying Direct on Aggregators (PolicyBazaar)",
        benchmark_source="IRDAI Digital Consumer Study (N=2,500)",
        ground_truth=38.0,
        is_grounded_archetype=True,
        v_0=-0.4895,  # 38%
        loss_lambda=2.15,
        evaluations=[
            PersonaEvaluationV4_4("Ramesh Patel", "Kirana Store Owner", 0.35, "NO", -1.2, 5.90, "Needs trusted human agent who will stand by during claims.", "Claim rejection."),
            PersonaEvaluationV4_4("Priya Sharma", "Senior Tech PM", 0.25, "YES", 1.6, 1.10, "Compares policy wording and settles term life direct online.", "None."),
            PersonaEvaluationV4_4("Ananya Iyer", "Gen-Z Student", 0.15, "YES", 0.6, 2.80, "Cheap two-wheeler third party insurance done in 2 mins.", "None."),
            PersonaEvaluationV4_4("Suresh Menon", "Retired Public Official", 0.15, "NO", -2.0, 7.80, "Refuses app insurance; relies entirely on LIC branch officer.", "Agent trust."),
            PersonaEvaluationV4_4("Kavita Deshmukh", "Freelance Designer", 0.10, "NO", -0.5, 4.40, "Browses online quotes but buys through known family broker.", "Hospital cashless.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q10",
        title="India WealthTech: Digital SIP & Mutual Fund Platforms (Groww/Zerodha)",
        benchmark_source="AMFI Retail Investor Survey (N=2,500)",
        ground_truth=47.0,
        is_grounded_archetype=True,
        v_0=-0.1201,  # 47%
        loss_lambda=1.90,
        evaluations=[
            PersonaEvaluationV4_4("Ramesh Patel", "Kirana Store Owner", 0.35, "NO", -0.8, 4.50, "Prefers safe physical gold and bank fixed deposits for trade safety.", "Market risk."),
            PersonaEvaluationV4_4("Priya Sharma", "Senior Tech PM", 0.25, "YES", 1.8, 0.90, "Automated monthly SIPs in index funds for long term wealth.", "None."),
            PersonaEvaluationV4_4("Ananya Iyer", "Gen-Z Student", 0.15, "YES", 1.0, 1.80, "Small ₹500/month SIP from pocket money on Groww app.", "Short-term volatility."),
            PersonaEvaluationV4_4("Suresh Menon", "Retired Public Official", 0.15, "NO", -1.6, 6.50, "Puts entire pension savings in Post Office and SBI FDs.", "Capital safety."),
            PersonaEvaluationV4_4("Kavita Deshmukh", "Freelance Designer", 0.10, "YES", 0.8, 2.60, "Invests emergency surplus into hybrid mutual funds.", "Liquidity.")
        ]
    ))

    # =========================================================================
    # SUITE 3: DELOITTE US DIGITAL MEDIA TRENDS (N=2,005)
    # =========================================================================
    questions.append(QuestionContextV4_4(
        question_id="Q11",
        title="Streaming Churn: $5 Monthly Subscription Price Increase",
        benchmark_source="Deloitte Digital Media Trends (N=2,005)",
        ground_truth=61.0,
        is_grounded_archetype=True,
        v_0=0.4473,  # 61%
        loss_lambda=1.95,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "YES", 1.2, 2.06, "An extra $60/year for same content triggers immediate cancel.", "Subscription fatigue."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "NO", -0.8, 3.80, "Convenience outweighs $5; keep it on autopay.", "Convenience."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "YES", 1.4, 2.15, "Fixed income cannot absorb continuous streaming price hikes.", "Price inflation."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 0.8, 2.90, "Will cancel and rotate between platforms instead of paying more.", "Cost control."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 1.6, 1.80, "Tight student budget; $5 hike means instant churn.", "Budget limit.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q12",
        title="Show Hopping / Single-Show Binge and Immediate Cancel",
        benchmark_source="Deloitte Digital Media Trends (N=2,005)",
        ground_truth=47.0,
        is_grounded_archetype=True,
        v_0=-0.1201,  # 47%
        loss_lambda=1.55,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "YES", 0.8, 2.50, "Binge season and cancel right away; hate paying idle months.", "Idle billing."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "NO", -1.0, 4.20, "Keep subscriptions rolling because finding new shows takes time.", "Inertia."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "NO", -0.5, 3.80, "Too much hassle signing up and canceling repeatedly.", "Hassle."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 0.5, 2.80, "Rotate subscriptions every few months to save money.", "Cost savings."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 1.5, 1.50, "Sign up for 1 month, binge whole series, cancel immediately.", "No money.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q13",
        title="Canceled at Least One Subscription in Past 6 Months",
        benchmark_source="Deloitte Digital Media Trends (N=2,005)",
        ground_truth=54.0,
        is_grounded_archetype=True,
        v_0=0.1603,  # 54%
        loss_lambda=1.60,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "YES", 1.0, 2.10, "Audited monthly expenses and trimmed two unused channels.", "Budget review."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "NO", -0.5, 3.50, "Didn't cancel; still have four services active.", "Autopay."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "YES", 0.5, 2.80, "Cut premium cable package to save $40/month.", "Retirement budget."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 0.8, 2.20, "Dropped a kids channel that no one was watching.", "Unused service."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 1.2, 1.70, "Cut streaming service as soon as student discount expired.", "Student budget.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q14",
        title="Ad-Supported Tier Switch (Accept Commercials for 50% Off)",
        benchmark_source="Deloitte Digital Media Trends (N=2,005)",
        ground_truth=52.0,
        is_grounded_archetype=True,
        v_0=0.0800,  # 52%
        loss_lambda=1.65,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "YES", 0.8, 2.40, "Saving $8 a month is worth sitting through a couple ads.", "Savings."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "NO", -1.5, 5.50, "Hate commercials; paying full price for zero ad friction.", "Ad annoyance."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "YES", 0.8, 2.10, "Grew up with television commercials; saving half price is fine.", "Familiarity."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 0.5, 2.80, "Ad tier is fine for background TV while cooking or folding laundry.", "Practicality."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 1.4, 1.60, "Ad-supported plan is the only tier I can actually afford.", "Cost constraint.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q15",
        title="Signed Up for Single Show and Canceled Immediately",
        benchmark_source="Deloitte Digital Media Trends (N=2,005)",
        ground_truth=47.0,
        is_grounded_archetype=True,
        v_0=-0.1201,  # 47%
        loss_lambda=1.55,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "YES", 0.8, 2.50, "Canceled right away after finishing mini-series.", "No waste."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "NO", -1.0, 4.20, "Keep subscriptions rolling; forgot to cancel.", "Inertia."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "NO", -0.5, 3.80, "Too much effort switching in and out.", "Comfort."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 0.5, 2.80, "Canceled right after watching holiday specials.", "Pragmatism."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 1.5, 1.50, "Only bought month for sports tournament, then canceled.", "Budget.")
        ]
    ))

    # =========================================================================
    # SUITE 4: PEW RESEARCH AI, PRIVACY & BIOMETRICS (N=5,101)
    # =========================================================================
    questions.append(QuestionContextV4_4(
        question_id="Q16",
        title="AI Customer Support Chatbot vs 15-Minute Human Hold",
        benchmark_source="Pew Research Center ATP (N=5,101)",
        ground_truth=33.0,
        is_grounded_archetype=True,
        v_0=-0.7082,  # 33%
        loss_lambda=1.85,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "NO", -1.5, 5.49, "Chatbots loop endlessly; I'll wait 15 mins for accountable human.", "Incompetent bot."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "YES", 1.8, 1.46, "Instant AI bot solves basic routing errors in 10 seconds.", "Hates phone queues."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "NO", -1.8, 5.72, "Refuse to argue with computer script; give me human rep.", "Bot distrust."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "NO", -1.5, 5.08, "Dealt with bad hospital software all day; want a real person.", "Human accountability."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 1.5, 2.76, "Waiting 15 mins on phone is torture; bot is fast.", "Speed preference.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q17",
        title="Biometric Authentication (Face ID / Fingerprint) for Banking",
        benchmark_source="Pew Research Center ATP (N=5,101)",
        ground_truth=70.0,
        is_grounded_archetype=True,
        v_0=0.8473,  # 70%
        loss_lambda=1.40,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "YES", 0.5, 2.06, "Face ID eliminates typing long passwords on mobile.", "Efficiency."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "YES", 1.5, 0.82, "Hardware biometric enclave is fast and secure.", "UX speed."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "YES", 0.2, 2.45, "Fingerprint is easier than remembering changing passwords.", "Convenience."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 0.8, 1.36, "Logging in with Face ID while holding baby is seamless.", "Practicality."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 0.8, 1.51, "Use Face ID for every app on phone.", "Default habit.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q18",
        title="Continuous Background Location Tracking for Store Discounts",
        benchmark_source="Pew Research Center ATP (N=5,101)",
        ground_truth=29.0,
        is_grounded_archetype=True,
        v_0=-0.8961,  # 29%
        loss_lambda=2.25,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "NO", -1.8, 2.80, "Always-on location tracking for coupons is invasive surveillance.", "Privacy violation."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "NO", -1.5, 2.30, "Background location kills phone battery and sells data brokers.", "Battery/privacy."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "NO", -1.8, 2.80, "Do not want tech corporations tracking where I walk.", "Surveillance."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "NO", -1.2, 2.50, "Restrict app location to 'Only while using app'.", "Safety/privacy."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "NO", -1.2, 2.40, "Discounts are cool, but background battery drain sucks.", "Battery drain.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q19",
        title="Algorithmic Recommendation Feed vs Strict Chronological Feed",
        benchmark_source="Pew Research Center ATP (N=5,101)",
        ground_truth=38.0,
        is_grounded_archetype=True,
        v_0=-0.4895,  # 38%
        loss_lambda=1.65,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "NO", -1.5, 3.01, "Prefer chronological order so I see what I actually follow.", "Control."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "NO", -1.5, 1.18, "Algorithms push engagement bait; want chronological feed.", "Filter bubble."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "NO", -1.8, 4.65, "Algorithms manipulate what stories you read; want timeline.", "Platform bias."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "NO", -1.2, 1.93, "Chronological feels less addictive and more predictable.", "Predictability."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "NO", -1.2, 2.24, "TikTok algo is fun, but Instagram/Twitter algo is annoying.", "Mixed feelings.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q20",
        title="Automated AI Resume / Job Applicant Screening Acceptance",
        benchmark_source="Pew Research Center ATP (N=5,101)",
        ground_truth=30.0,
        is_grounded_archetype=True,
        v_0=-0.8473,  # 30%
        loss_lambda=2.20,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "NO", -1.5, 6.52, "Black-box AI screening candidates without human HR is unfair.", "No accountability."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "YES", 1.2, 1.73, "AI parser is faster than clueless recruiters.", "Speed over HR."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "NO", -1.8, 7.53, "Computer program judging human job applicants is unacceptable.", "Algorithmic bias."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "NO", -1.5, 6.03, "Nursing candidates cannot be evaluated by algorithms.", "Lack of empathy."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 0.5, 3.42, "If AI filters my resume fairly, maybe I get more interviews.", "Faster hiring.")
        ]
    ))

    # =========================================================================
    # SUITE 5: MCKINSEY & NIELSENIQ 5-YEAR SCANNER BENCHMARK (N=10,000+)
    # =========================================================================
    questions.append(QuestionContextV4_4(
        question_id="Q21",
        title="The Green Premium Paradox (+25% on Eco-Friendly Detergent)",
        benchmark_source="McKinsey / NielsenIQ POS Scanner Study (N=10,000+)",
        ground_truth=18.0,
        is_grounded_archetype=True,
        v_0=-1.5163,  # 18%
        loss_lambda=2.30,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "NO", -1.5, 4.63, "Paying an extra $3 on detergent every month breaks my grocery budget.", "Price premium."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "NO", -0.5, 1.82, "I support green, but $15 for detergent feels like greenwashing markup.", "Questionable ROI."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "NO", -1.8, 7.15, "On a fixed pension, I buy the reliable $12 standard brand.", "Fixed income."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "NO", -1.2, 2.97, "With kids doing sports laundry daily, I need proven stain removal.", "Cleaning power."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "NO", -1.8, 3.45, "I can barely afford the cheap detergent; no way I pay $15.", "Zero budget slack.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q22",
        title="The 10-Cent Plastic Bag Fee Asymmetry (Bring Reusable Bag)",
        benchmark_source="McKinsey / NielsenIQ POS Scanner Study (N=10,000+)",
        ground_truth=81.0,
        is_grounded_archetype=True,
        v_0=1.4500,  # 81%
        loss_lambda=2.40,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "YES", 1.5, 1.50, "Keep reusable bags in car; paying 10c for bag is waste of cash.", "Nuisance fee avoidance."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "YES", 0.8, 1.20, "Keep a tote backpack with me; avoid bag fee clutter.", "Avoid plastic."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "YES", 1.2, 1.60, "Refuse to give grocery store free dimes for flimsy bags.", "Thrift."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 0.5, 1.80, "Keep large canvas totes in trunk for grocery runs.", "Habit."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 1.5, 1.10, "Don't have spare dimes to throw away on plastic bags.", "Budget.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q23",
        title="Certified Refurbished Hardware Adoption (30% Discount)",
        benchmark_source="McKinsey / NielsenIQ POS Scanner Study (N=10,000+)",
        ground_truth=31.0,
        is_grounded_archetype=True,
        v_0=-0.7999,  # 31%
        loss_lambda=2.10,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "YES", 1.2, 3.69, "Saving $300 on manufacturer certified laptop is great value.", "Value."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "YES", 1.5, 1.40, "Official Apple/Dell refurbished units are practically new.", "Good deal."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "NO", -1.8, 7.29, "Fear battery wear or hidden scratches; prefer sealed box.", "Peace of mind."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 0.8, 3.18, "Good way to get daughter a school laptop for less.", "Budget stretch."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 1.5, 2.63, "Refurbished is the only way I can afford a MacBook.", "Essential discount.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q24",
        title="Brand Boycott Durability (60 Days Later Habit Relapse)",
        benchmark_source="McKinsey / NielsenIQ POS Scanner Study (N=10,000+)",
        ground_truth=22.0,
        is_grounded_archetype=True,
        v_0=-1.2657,  # 22%
        loss_lambda=1.50,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "YES", 1.2, 4.40, "Stay committed to boycotting brands that violate values.", "Core principles."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "YES", 1.2, 1.73, "Switch permanently to competitor; don't look back.", "Low switching cost."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "YES", 1.5, 5.15, "Traditional boycott stance; avoid unpatriotic brands.", "Loyalty."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "NO", -0.5, 6.03, "Outrage fades; kids prefer the taste and it's convenient.", "Habit relapse."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "NO", -1.5, 3.28, "Can't afford to boycott cheap brand if competitor is pricier.", "Convenience.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q25",
        title="Auto-Ship Replenishment Subscriptions (5% Discount Trap)",
        benchmark_source="McKinsey / NielsenIQ POS Scanner Study (N=10,000+)",
        ground_truth=24.0,
        is_grounded_archetype=True,
        v_0=-1.1527,  # 24%
        loss_lambda=2.15,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "NO", -0.5, 6.87, "5% discount isn't worth risk of accumulating surplus paper towels.", "Surplus inventory."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "YES", 0.7, 5.00, "Auto-ship coffee beans is convenient; cancel if it piles up.", "Convenience."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "NO", -1.5, 7.54, "Refuse recurring autopay deliveries; buy only when empty.", "Control."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 0.5, 5.56, "Auto-ship vitamins and toilet paper saves time.", "Time saver."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "NO", -1.0, 6.17, "Don't have fixed address; auto-delivery doesn't work.", "Transitional life.")
        ]
    ))

    # =========================================================================
    # SUITE 6: PEW NATIONAL TIPPING SURVEY (N=11,945) - ZERO-SHOT NOVEL DOMAIN
    # =========================================================================
    questions.append(QuestionContextV4_4(
        question_id="Q26",
        title="Sit-Down Restaurant Dining Table Service Tipping",
        benchmark_source="Pew Research Center (N=11,945)",
        ground_truth=92.0,
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=1.5,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "YES", 1.8, 1.5, "Always tip 20% for table service; social contract.", "None."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "YES", 2.0, 0.8, "Always tip 20%+ on card reader for servers.", "None."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "YES", 1.8, 1.6, "Traditional manners; leave cash on table every time.", "None."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 2.0, 0.9, "Hospitality workers deserve fair pay; always tip 20%.", "None."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 1.5, 2.2, "Split bill and tip 15-18% when dining out.", "Non-negotiable norm.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q27",
        title="Fast-Casual / Walk-Up Counter Pickup Tipping",
        benchmark_source="Pew Research Center (N=11,945)",
        ground_truth=12.0,
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=2.0,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "NO", -1.8, 6.8, "Carried my own tray; zero service provided.", "Tip creep."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "NO", -1.0, 4.5, "Bypass tip screen when picking up food at counter.", "Unjustified prompt."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "NO", -2.0, 7.5, "Not giving store free dimes for counter handoff.", "Violation of norm."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "NO", -1.2, 5.2, "Already paying $16 for takeout; press No Tip.", "No table service."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "NO", -2.0, 7.8, "Broke student; hit No Tip as fast as possible.", "Zero budget.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q28",
        title="Coffee Shop Counter iPad Swivel Screen Tipping",
        benchmark_source="Pew Research Center (N=11,945)",
        ground_truth=25.0,
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=1.8,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "NO", -1.4, 5.6, "Swiveling iPad for $4 drip coffee is guilt trip; bypass.", "Overpriced."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "YES", 0.8, 1.8, "Tap $1 tip button at my regular morning cafe.", "Habit/convenience."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "NO", -1.8, 6.8, "Detest swivel screens; miss loose coin jars.", "Screen hostility."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "NO", -0.8, 4.2, "Quick drip coffee doesn't warrant extra tip.", "Cost."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "NO", -1.7, 6.5, "Can barely afford the latte itself; skip tip.", "Tight budget.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q29",
        title="Mobile App Food Delivery Driver Tipping",
        benchmark_source="Pew Research Center (N=11,945)",
        ground_truth=76.0,
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=1.6,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "YES", 1.5, 2.0, "Driver using own car in traffic deserves tip.", "Labor respect."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "YES", 1.9, 0.8, "Tip $6-8 on DoorDash so food arrives hot.", "Fast service."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "YES", 1.4, 2.4, "Always hand delivery driver cash at the door.", "Manners."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 1.8, 1.0, "Lifesaver after hospital shift; always tip well.", "Empathy."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 0.9, 3.6, "High app fees suck, but always add $2-3 for driver.", "Driver wages.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q30",
        title="Mandatory Automatic Restaurant Service Fees (Opposition)",
        benchmark_source="Pew Research Center (N=11,945)",
        ground_truth=72.0,
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=2.2,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "YES", 1.6, 1.8, "Surprise fees at bottom of bill are deceptive billing.", "Deceptive pricing."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "NO", -0.5, 3.2, "I prefer all-inclusive service charges over awkward tip calculation screens.", "Prefers included service."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "YES", 1.8, 1.4, "Tipping is customer choice; forcing fee is robbery.", "Loss of agency."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 1.2, 2.3, "Put honest prices on menu instead of surprise fees.", "Opaque pricing."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 1.4, 1.8, "Surprise 20% surcharge wrecks my dining budget.", "Budget shock.")
        ]
    ))

    # =========================================================================
    # SUITE 7: MULTI-FRONTIER BENCHMARK (N=28,400)
    # =========================================================================
    questions.append(QuestionContextV4_4(
        question_id="Q31",
        title="Emergency Financial Resilience ($400 Expense in Cash/Savings)",
        benchmark_source="Federal Reserve SHED Survey (N=11,400)",
        ground_truth=63.0,
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=1.9,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "YES", 0.8, 1.5, "Strict emergency savings covers $400 easily.", "None."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "YES", 1.8, 0.8, "Checking account absorbs $400 without issue.", "None."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "YES", 0.7, 2.2, "Credit union rainy-day savings pays $400 cash.", "Manageable."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 1.2, 1.2, "Hospital RN salary covers emergency debit.", "None."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "NO", -1.8, 7.2, "Student checking wiped out; would have to borrow.", "Zero liquidity.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q32",
        title="Dark Pattern Cookie Fatigue ('Accept All' Surrender)",
        benchmark_source="CNIL & Web Usability Audit (N=5,000)",
        ground_truth=78.0,
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=1.4,
        is_dark_pattern=True,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "NO", -0.8, 3.0, "Usually configure settings, but on mobile banner exhaustion hits.", "Fatigue."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "YES", 1.5, 1.0, "Browser ad-blocker cleans up; tap Accept All to clear.", "Screen clutter."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "YES", 1.2, 1.8, "Manage settings are too small to read; click big button.", "Exhaustion."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 1.6, 0.8, "Zero bandwidth after hospital shift; tap Accept All.", "Time poverty."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 1.8, 0.6, "Double tap big button instantly without reading.", "Muscle memory.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q33",
        title="Flight Add-On Insurance ($25 Policy on $350 Flight)",
        benchmark_source="Swiss Re & InsurTech Benchmark (N=4,000)",
        ground_truth=28.0,
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=1.8,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "NO", -1.5, 5.5, "$25 on $350 is 7% markup with fine-print exclusions.", "Poor value."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "NO", -1.8, 6.0, "Credit card travel insurance already covers trip cancel.", "Redundant."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "YES", 0.9, 2.4, "Peace of mind is worth $25 at my age.", "Peace of mind."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "NO", -0.8, 4.0, "Domestic flight credits are sufficient if plans change.", "Airline credits."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "NO", -1.9, 7.5, "Ultra low cost flight; no money for add-on fee.", "Student budget.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q34",
        title="Accidental Free Trial Rollover (Forgot to Cancel in Time)",
        benchmark_source="FTC & Consumer Reports Benchmark (N=3,000)",
        ground_truth=48.0,
        is_grounded_archetype=False,
        is_involuntary_error=True,
        v_0=0.0,
        loss_lambda=1.5,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "YES", 0.5, 3.0, "Missed 7-day cutoff once and got billed $15.", "Human error."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "YES", 1.2, 1.5, "Sign up for dev tools constantly; spaced out on trials.", "Trial inertia."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "NO", -1.5, 5.5, "Never give card for free trial; avoid trap.", "Trap avoidance."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 1.0, 2.0, "Forgot kids app trial between busy work shifts.", "Busy schedule."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 1.4, 1.5, "Sign up for student trials and get billed accidentally.", "Frequent occurrence.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q35",
        title="Viral Referral Link Sharing ('Give $20, Get $20' Active Texting)",
        benchmark_source="Harvard Business Review Benchmark (N=5,000)",
        ground_truth=16.0,
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=1.9,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "NO", -1.8, 6.5, "Texting referral links to friends feels cheap and awkward.", "Social friction."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "NO", -1.0, 4.8, "Shilling promo codes to personal contacts is cringey.", "Social boundary."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "NO", -2.0, 7.5, "Refuse to send commercial solicitations to family.", "Anti-marketing."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "NO", -1.5, 6.0, "Tell friends brand name, but never send affiliate links.", "Word of mouth."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "NO", -0.5, 4.2, "Only text roommate if cash reward is huge; otherwise skip.", "Effort.")
        ]
    ))

    # =========================================================================
    # SUITE 8: KAISER FAMILY FOUNDATION (KFF) HEALTHCARE BENCHMARK (N=2,500)
    # =========================================================================
    questions.append(QuestionContextV4_4(
        question_id="Q36",
        title="Generic vs Brand-Name Prescription Substitution ($10 vs $50 Copay)",
        benchmark_source="KFF Health Tracking Poll (N=2,500)",
        ground_truth=87.0,
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=1.5,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "YES", 1.8, 1.0, "Chemically identical FDA molecules for 80% less.", "No brainer."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "YES", 1.6, 1.0, "Generic filled automatically; same active ingredients.", "None."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "YES", 1.5, 1.5, "Saves $40 a month on blood pressure medication on Medicare.", "Budget relief."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 2.0, 0.5, "As an RN, I know generics meet strict bioequivalence rules.", "Clinical trust."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 1.9, 0.8, "Ten dollars vs fifty dollars? Generic 100% of the time.", "Price essential.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q37",
        title="Medication Rationing / Delaying Refills Due to Out-of-Pocket Cost",
        benchmark_source="KFF Prescription Drug Poll (N=2,500)",
        ground_truth=28.0,
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=2.1,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "NO", -1.0, 5.0, "I budget health before everything else, but out-of-pocket brand tier copays are frustrating.", "Prioritizes health budget."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "NO", -1.9, 8.0, "High income and good tech insurance covers meds.", "Financial buffer."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "NO", -1.5, 6.5, "I take blood pressure medication daily. Skipping pills risks a stroke; Medicare covers maintenance generics.", "Clinical necessity and Medicare coverage."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "NO", -1.5, 6.5, "As an RN, know clinical dangers of cutting pills.", "Clinical risks."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 1.5, 2.0, "Skipped $60 prescription inhaler when my student debit account was empty.", "Out-of-pocket cash crunch.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q38",
        title="Postponing Needed Care Due to High Deductible ($800 Out-of-Pocket)",
        benchmark_source="KFF Health Affordability Poll (N=2,500)",
        ground_truth=43.0,
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=1.9,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "YES", 0.8, 2.2, "Delayed $800 knee MRI to see if rest resolved it.", "High deductible."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "NO", -1.4, 6.0, "Maxed HSA covers care immediately.", "Speed."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "NO", -0.8, 4.5, "Medicare + Medigap covers approved care with low out-of-pocket.", "Medigap."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 0.5, 3.0, "Surprise hospital facility fees make you think twice.", "Opaque bills."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 1.6, 1.8, "Don't have $800; wait for illness to pass on own.", "No funds.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q39",
        title="Virtual Telehealth Therapy vs In-Person Counseling Preference",
        benchmark_source="KFF / Peterson Health Monitor (N=2,500)",
        ground_truth=56.0,
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=1.6,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "YES", 0.6, 2.5, "Single mom; evening video call avoids childcare hassle.", "Logistics."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "YES", 1.5, 1.2, "Zoom therapy is superior; in-person wastes transit time.", "UX speed."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "NO", -1.2, 5.0, "Want face-to-face human warmth; screens feel cold.", "Human connection."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 0.7, 2.2, "Privacy of home session fits odd nursing shifts.", "Flexibility."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 0.9, 2.0, "Video counseling from dorm room reduces campus stigma.", "Privacy.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q40",
        title="Workplace Health Insurance Fitness Tracking ($20/mo Premium Discount)",
        benchmark_source="KFF / Pew Workplace Privacy (N=2,500)",
        ground_truth=34.0,
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=2.2,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "NO", -1.6, 6.8, "Refuse to give biometric telemetry to insurance underwriters.", "Surveillance."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "NO", -1.0, 5.2, "Corporate telemetry sets terrible privacy precedent.", "Privacy creep."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "NO", -1.8, 7.5, "Monitoring steps and sleep like probation officer is dystopia.", "Intrusion."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 0.5, 3.0, "Walk 15,000 steps on nursing shift anyway; take $240.", "Easy money."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 0.8, 2.5, "Don't care about step data; $20/mo covers Spotify.", "Discount.")
        ]
    ))

    # =========================================================================
    # SUITE 9: AAA & CONSUMER REPORTS AUTOMOTIVE & EV TECH BENCHMARK (N=3,500)
    # =========================================================================
    questions.append(QuestionContextV4_4(
        question_id="Q41",
        title="Winter EV Range Anxiety & Cold Weather Driving Hesitation",
        benchmark_source="AAA Winter Driving & EV Consumer Survey (N=3,500)",
        ground_truth=58.0,  # AAA: 58% cite freezing weather battery loss (up to 40% range drop) as major purchase hesitation
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=1.8,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "YES", 1.2, 2.2, "Cleveland Ohio winters get below zero. Losing 40% battery range when commuting with my kid is a major dealbreaker.", "Severe winter range loss."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "NO", -0.8, 4.0, "I live in Austin Texas; mild winters and home garage Level 2 charger makes range drop irrelevant.", "Mild climate buffer."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "YES", 1.4, 2.5, "Pittsburgh hills in snow are brutal. If battery drains while running the cabin heater in a blizzard, you are stranded.", "Cold weather safety."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 1.0, 2.8, "Chicago winters with sub-zero windchills. As an essential hospital nurse, my car must start and run in any blizzard.", "Reliability in freezing snow."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "NO", -0.5, 3.5, "Michigan gets snowy, but modern pre-heating apps handle it fine if plugged in.", "Pre-conditioning.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q42",
        title="Hands-Free Highway Driving Autopilot Trust (Level 2 Automation)",
        benchmark_source="AAA Autonomous Vehicle Consumer Survey (N=3,500)",
        ground_truth=22.0,  # AAA: Only 22% of US drivers trust riding in / using fully hands-free driving technology
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=2.3,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "NO", -1.8, 7.2, "Taking my hands off the steering wheel at 70 mph while a computer steers is terrifying. Software glitched too often.", "Fatal safety risk."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "YES", 1.4, 1.8, "Tesla Autopilot / GM Super Cruise on mapped highways is great tech. I use lane centering on long highway road trips.", "Loves automation."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "NO", -2.0, 8.5, "I want two hands on the wheel and eyes on the road. Letting a computer drive a multi-ton vehicle is insanity.", "Complete distrust."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "NO", -1.5, 6.8, "I see trauma victims in the ER from car wrecks. No computer sensor can react to black ice or deer like human reflex.", "Trauma nurse risk aversion."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "NO", -0.8, 5.0, "It looks cool on YouTube, but real-world phantom braking reports scare me.", "Phantom braking fears.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q43",
        title="Connected Car Telemetry Tracking for Auto Insurance Discounts",
        benchmark_source="Consumer Reports Auto Telematics Benchmark (N=3,500)",
        ground_truth=33.0,  # Consumer Reports: 33% install telematics plug-in/app; 67% refuse hard braking tracking
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=2.1,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "NO", -1.5, 6.2, "The OBD plug tracks hard braking and late night driving. If someone cuts you off and you slam brakes, they raise rates.", "Penalizes defensive driving."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "NO", -1.2, 5.5, "Insurance telemetry logs every acceleration curve and GPS waypoint. Not trading my driving telemetry for $80/year.", "Excessive surveillance."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "NO", -1.6, 7.0, "I drive under 4,000 miles a year on a fixed pension, but I don't want a black box monitoring my driving habits.", "Invasive monitoring."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 0.8, 2.5, "Our household auto insurance for two cars is expensive. I drive calmly and safely, so the 15% discount saves real money.", "Family premium savings."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 1.2, 2.0, "Car insurance for a 21-year-old male is $250 a month! I'll plug in whatever sensor they want if it cuts the rate.", "Desperate for rate cuts.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q44",
        title="Car Subscription Services ($800/mo All-Inclusive) vs Buying/Leasing",
        benchmark_source="Cox Automotive Consumer Study (N=3,500)",
        ground_truth=14.0,  # Cox: Only 14% of consumers consider monthly car subscriptions due to high price premium
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=2.3,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "NO", -2.0, 7.8, "$800 a month with zero equity or vehicle ownership is terrible financial management. Buying a 3-year-old car is far smarter.", "Zero equity waste."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "NO", -0.8, 4.5, "Convenient to swap cars, but $800-1,000/mo is wildly overpriced compared to a lease.", "Poor value proposition."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "NO", -2.0, 8.5, "I own my Subaru outright with no car payment. Paying $800 monthly forever is financial foolishness.", "Thrift and ownership."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "NO", -1.8, 7.2, "With kids and family expenses, an $800 monthly recurring car charge is completely out of the question.", "Budget impossibility."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "NO", -1.9, 8.0, "My entire car is barely worth $3,000. Eight hundred a month is fantasy land.", "Extreme cost barrier.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q45",
        title="In-Vehicle Touchscreens vs Physical Buttons for Volume and HVAC Controls",
        benchmark_source="Consumer Reports & Euro NCAP Usability Benchmark (N=3,500)",
        ground_truth=71.0,  # CR: 71% of car buyers prefer physical dials/buttons over touchscreen menus while driving
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=1.7,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "YES", 1.5, 1.8, "Digging through three touchscreen sub-menus while driving just to adjust fan speed is a dangerous distraction.", "Tactile safety."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "YES", 0.8, 2.2, "Even as a tech guy, muscle memory dials for volume and AC temperature are vastly superior to flat screens while driving.", "Haptic feedback."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "YES", 1.8, 1.2, "Touchscreens smudge and force you to take your eyes off the highway. Give me solid physical knobs every time.", "Safety and simplicity."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 1.4, 1.6, "When driving children in freezing rain, I need to turn on the defroster by touch without looking away from road.", "Driving safety."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "NO", -0.5, 3.8, "Big Tesla-style iPad screens look cool and futuristic, even if dials are easier.", "Aesthetic appeal.")
        ]
    ))

    # =========================================================================
    # SUITE 10: GALLUP & MORNING CONSULT FINTECH & BANKING BENCHMARK (N=4,200)
    # =========================================================================
    questions.append(QuestionContextV4_4(
        question_id="Q46",
        title="Annual Fee Credit Cards ($95 Fee for Travel Points vs $0 Cash Back)",
        benchmark_source="Morning Consult / Bankrate Credit Card Benchmark (N=4,200)",
        ground_truth=32.0,  # Bankrate: 32% of cardholders hold an annual fee card; 68% refuse and use no-fee cash back
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=2.0,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "NO", -1.5, 5.8, "Paying a credit card company $95 a year just to use their plastic is throwing money away. A flat 2% no-fee card is far better.", "Refuses annual fee."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "YES", 1.6, 1.5, "Chase Sapphire / Amex Gold $95 fee easily pays for itself with the $50 hotel credit and 3x dining multiplier.", "Travel rewards optimization."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "NO", -1.8, 6.8, "I have used the same no-fee credit union card for thirty years. I will never pay an annual fee to a credit card bank.", "Principled fee refusal."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "NO", -0.8, 4.2, "We don't travel enough to justify $95; cash back on groceries and gas with zero fee works best for us.", "Practical cash back."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "NO", -1.9, 7.5, "I can't even get approved for an annual fee card, and paying $95 is out of the question.", "Student budget.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q47",
        title="Switching Primary Checking Account for a $300 Bank Sign-Up Bonus",
        benchmark_source="Morning Consult Retail Banking Benchmark (N=4,200)",
        ground_truth=21.0,  # Morning Consult: Only 21% actually switch primary checking account due to direct deposit friction
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=1.8,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "NO", -1.8, 8.2, "$300 is not worth switching employer payroll, mortgage links, and 20 automated bills.", "Extreme switching friction."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "NO", -0.8, 6.5, "After taxes, $300 is $180. Not worth reconfiguring 15 billing links and payroll ACH.", "Low time ROI vs setup effort."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "NO", -2.0, 8.5, "Banked at my credit union for 40 years. Changing pension deposits for $300 is dangerous.", "Pension risk and inertia."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "NO", -1.5, 7.8, "Too many family autopays linked; risk of a missed mortgage payment exceeds $300.", "Risk of payment failure."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 1.4, 2.0, "Three hundred dollars is a month of groceries for a student. I'll open an account immediately.", "High marginal value of cash.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q48",
        title="Carrying Revolving Credit Card Balances Month-to-Month",
        benchmark_source="Federal Reserve / Gallup Consumer Credit Poll (N=4,200)",
        ground_truth=46.0,  # Fed: 46% of credit cardholders carry an unpaid balance month-to-month incurring interest
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=1.7,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "NO", -1.8, 7.5, "Paying 24% APR interest on credit card debt is financial poison. I pay every card statement to zero every single month.", "Refuses credit interest."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "NO", -1.6, 7.0, "Cards are set on automatic full statement balance payment. Carrying high-interest debt makes zero sense.", "Auto-pay in full."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "NO", -1.5, 6.5, "Never carried a credit card balance in my life. If I don't have the cash in my checking, I don't buy it.", "Debt aversion."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 1.2, 2.4, "Between summer camp, orthodontic braces for my daughter, and car repairs, we carry a rolling balance of a couple thousand.", "Family cost pressures."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 1.5, 2.0, "Textbooks and emergency living costs put $1,800 on my Discover card. I make minimum payments every month.", "Student debt rolling balance.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q49",
        title="Digital-Only Neo-Bank (Chime / Ally) as Sole Primary Checking Account",
        benchmark_source="Morning Consult Digital Banking Benchmark (N=4,200)",
        ground_truth=27.0,  # Morning Consult: 27% use digital-only app as primary checking; 73% retain branch banks
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=2.1,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "NO", -1.8, 7.5, "Unauthorized charges need a branch manager with physical accountability, not an offshore chat app.", "Recourse and notary services."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "YES", 0.6, 3.2, "I use Chime for day-to-day spending, but keep Chase for primary direct deposit and wire transfers.", "Hybrid banking."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "NO", -2.0, 8.8, "Will never put primary life savings in a bank without a physical teller and vault.", "Distrust of branchless banks."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "NO", -1.6, 7.5, "With kids, I need local branch ATMs, money orders, and teller deposits for school.", "Need for physical branches."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 0.8, 2.5, "Chime gives two-day early direct deposit, though work-study needed a voided physical check.", "Early deposit convenience.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q50",
        title="Contactless Tap-to-Pay (Apple Pay / Google Wallet) at Retail In-Store Checkout",
        benchmark_source="Pew Research & Federal Reserve Payment Diary (N=4,200)",
        ground_truth=64.0,  # Pew/Fed: 64% of smartphone users regularly use contactless phone/card tap-to-pay at POS
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=1.4,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "YES", 0.8, 1.8, "Tapping my credit card or phone at the register is significantly faster and more secure than inserting chip.", "Speed and security."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "YES", 1.9, 0.6, "I pay with Apple Watch or iPhone everywhere I go. I rarely even carry a physical wallet anymore.", "Frictionless UX."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "NO", -0.8, 4.5, "I still insert my chip card or pay cash. Tapping the phone feels gimmicky and I worry about accidental taps.", "Accidental tap fears."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 1.0, 1.5, "Tapping phone with Apple Pay at grocery checkout while juggling groceries and kids is a lifesaver.", "Convenience."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 1.6, 0.9, "I use Apple Pay for literally everything from vending machines to groceries.", "Daily habit.")
        ]
    ))

    # =========================================================================
    # SUITE 11: NATIONAL RETAIL FEDERATION (NRF) & CONSUMER COMMERCE (N=20,500)
    # =========================================================================
    questions.append(QuestionContextV4_4(
        question_id="Q51",
        title="Buy Online, Pick Up In-Store (BOPIS / Curbside Pickup) Regular Usage",
        benchmark_source="National Retail Federation (N=4,500)",
        ground_truth=58.0,  # NRF: 58% of digital shoppers regularly use BOPIS / curbside pickup
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=1.5,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "YES", 1.0, 1.8, "Saves shipping cost and lets me grab orders on way home from work.", "Convenient commute pickup."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "YES", 1.4, 1.2, "Order on app, pull up to spot, trunk loaded in 3 minutes.", "No delivery wait."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "NO", -0.6, 3.8, "If I am driving to the store, I will walk inside and pick what I want off the shelf.", "Prefers browsing in-person."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 1.6, 0.8, "Curbside pickup with two sleeping kids in car seats is the greatest invention ever.", "Essential parent convenience."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "NO", -0.8, 4.5, "I do not have a car on campus; curbside does not help me without a vehicle.", "No car.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q52",
        title="In-Store Return Preference vs Mail-Back Return for Online Apparel",
        benchmark_source="NRF Consumer Returns Benchmark (N=3,800)",
        ground_truth=67.0,  # NRF: 67% prefer returning online orders to a local physical store
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=1.5,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "YES", 1.1, 1.6, "Immediate refund credited to my card and zero packaging hassle.", "Immediate refund."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "NO", -0.5, 3.5, "I hate going to malls; QR code drop-off at Whole Foods/UPS is easier for me.", "Prefers parcel drop-off."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "YES", 1.4, 1.2, "I get a printed paper receipt and know the store accepted the return.", "Proof of return."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 1.3, 1.5, "Easier to return kids clothes while doing weekend grocery errands.", "Combines with weekly errands."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 0.9, 1.8, "I do not have a printer for shipping labels in dorm; walking to local store is faster.", "No printer.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q53",
        title="Amazon Prime Annual Membership Retention / Subscription",
        benchmark_source="CIRP Consumer Research (N=5,000)",
        ground_truth=71.0,  # CIRP: 71% of US online shoppers maintain active Amazon Prime membership
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=1.6,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "YES", 1.1, 1.6, "Free 2-day delivery on household supplies pays for itself in 6 months.", "Delivery value."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "YES", 1.6, 0.8, "Order electronics, household goods, Prime Video; indispensable utility.", "Daily utility."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "NO", -0.8, 4.8, "$139 a year is too expensive when regular shipping is free over $35.", "Annual fee objection."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "YES", 1.6, 0.7, "With diapers, school supplies, and groceries, Prime saves our sanity.", "Household essential."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 1.0, 1.5, "Amazon Prime Student is half price ($69/year) and includes Prime Video.", "Student discount.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q54",
        title="QR Code Digital Restaurant Menu vs Physical Paper Menu Preference",
        benchmark_source="National Restaurant Association (N=4,000)",
        ground_truth=31.0,  # NRA: Only 31% prefer QR digital phone menus; 69% strongly prefer physical paper menus
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=1.8,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "NO", -1.4, 5.5, "Scrolling tiny PDF menus on a 6-inch phone screen ruins dining ambiance.", "Poor dining ergonomics."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "YES", 1.0, 1.8, "Ordering and paying directly from phone without waiting for server is great.", "Speed."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "NO", -1.8, 7.2, "I do not want to scan a barcode with my phone just to order soup. Bring me a menu.", "Digital frustration."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "NO", -1.0, 4.8, "Hard to look at menu while my phone is keeping the kids entertained.", "Device conflict."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "NO", -0.6, 4.0, "QR code menus drain phone battery while out with friends; prefer paper.", "Battery drain.")
        ]
    ))

    questions.append(QuestionContextV4_4(
        question_id="Q55",
        title="Direct-to-Consumer (DTC) Mattress / Eyewear Brand Online Trial",
        benchmark_source="eMarketer & Morning Consult DTC Report (N=3,200)",
        ground_truth=39.0,  # Morning Consult: 39% of consumers have bought from DTC brands like Warby Parker / Casper
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=1.7,
        evaluations=[
            PersonaEvaluationV4_4("Sarah Jenkins", "Senior Accountant", 0.25, "NO", -1.0, 5.5, "I want to test a mattress in a showroom before spending $1,500; returning foam in a box is a nightmare.", "Return logistics."),
            PersonaEvaluationV4_4("Alex Rivera", "Full-Stack Developer", 0.20, "YES", 1.0, 2.2, "Warby Parker home try-on box and Casper mattress delivered in a box worked flawlessly.", "Modern DTC UX."),
            PersonaEvaluationV4_4("David Miller", "Retired Teacher", 0.20, "NO", -1.6, 6.8, "Buying prescription glasses or a bed online without trying it in person first makes no sense.", "Needs tactile trial."),
            PersonaEvaluationV4_4("Elena Rostova", "Nurse & Mother", 0.20, "NO", -0.8, 4.8, "Looked at DTC mattresses, but bought from local store for white-glove setup and old mattress haul-away.", "Haul-away service."),
            PersonaEvaluationV4_4("Marcus Chen", "Student", 0.15, "YES", 1.1, 1.8, "Got my Warby Parker glasses for $95 instead of $400 at the optometrist.", "Cost savings.")
        ]
    ))

    return questions
