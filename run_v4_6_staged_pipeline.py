"""
run_v4_6_staged_pipeline.py
Autonomous Staged Walk-Forward Validation Harness for Engine V4.6

STRICT PRINCIPLES:
1. Pure text questions only. Zero pre-authored persona shifts or friction values.
2. Dynamic blind reasoning via Persona Bank.
3. Universal choice model execution.
4. Auto-halting on error; full backward regression testing at each stage.
"""

import sys
import os
import argparse
from typing import List

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
sys.stdout.reconfigure(encoding='utf-8')

from v4_6.personas import PERSONA_BANK
from v4_6.reasoner import evaluate_persona_blindly
from v4_6.engine_v4_6 import QuestionSpec, evaluate_question_v4_6

# =========================================================================
# DEFINITION OF PURE TEXT BENCHMARK SPECIFICATIONS (NO PERSONA INPUTS)
# =========================================================================

BASE_SPECS: List[QuestionSpec] = [
    QuestionSpec(
        question_id="B01",
        title="Unexpected Extra Costs at Checkout (Shipping/Taxes/Fees)",
        decision_prompt="Will you abandon your online shopping cart if unexpected shipping fees, taxes, or service charges are added at the final payment screen?",
        benchmark_source="Baymard Institute (N=4,384)",
        ground_truth=48.0,
        stakes_level="medium"
    ),
    QuestionSpec(
        question_id="B02",
        title="Mandatory Account Creation Friction Before Checkout",
        decision_prompt="Will you abandon your online purchase if the website forces mandatory account registration with password creation before letting you pay?",
        benchmark_source="Baymard Institute (N=4,384)",
        ground_truth=25.0,
        stakes_level="medium"
    ),
    QuestionSpec(
        question_id="B03",
        title="India FinTech: 0% No-Cost EMI & BNPL Adoption",
        decision_prompt="Would you use instant zero-cost EMI or Buy-Now-Pay-Later at mobile checkout to split an electronics purchase into 3 monthly payments?",
        benchmark_source="NPCI & India FinTech (N=2,500)",
        ground_truth=62.0,
        stakes_level="medium"
    ),
    QuestionSpec(
        question_id="B04",
        title="Streaming Churn: $5 Monthly Subscription Price Hike",
        decision_prompt="Will you cancel your video streaming subscription if the monthly price increases by $5 per month?",
        benchmark_source="Deloitte Digital Media (N=2,005)",
        ground_truth=61.0,
        stakes_level="medium"
    ),
    QuestionSpec(
        question_id="B05",
        title="Sit-Down Restaurant Dining Table Service Tipping",
        decision_prompt="Do you always leave a 15-20% tip when dining at a sit-down restaurant with full table waitstaff service?",
        benchmark_source="Pew Research Center (N=11,945)",
        ground_truth=92.0,
        stakes_level="medium"
    ),
    QuestionSpec(
        question_id="B06",
        title="Fast-Casual Walk-Up Counter Pickup Tipping",
        decision_prompt="Do you regularly tip when ordering and picking up food yourself at a fast-casual walk-up counter?",
        benchmark_source="Pew Research Center (N=11,945)",
        ground_truth=12.0,
        stakes_level="low"
    ),
    QuestionSpec(
        question_id="B07",
        title="Emergency Financial Resilience ($400 Expense in Cash/Savings)",
        decision_prompt="Could you cover an unexpected $400 emergency expense completely using cash or checking savings without borrowing or carrying credit debt?",
        benchmark_source="Federal Reserve SHED (N=11,400)",
        ground_truth=63.0,
        stakes_level="high"
    ),
    QuestionSpec(
        question_id="B08",
        title="Dark Pattern Cookie Fatigue ('Accept All' Surrender)",
        decision_prompt="Do you click 'Accept All' on intrusive cookie consent popups just to make the banner disappear and read the content?",
        benchmark_source="CNIL & Web Usability (N=5,000)",
        ground_truth=78.0,
        stakes_level="low",
        is_fatigue_or_dark_pattern=True
    ),
    QuestionSpec(
        question_id="B09",
        title="Flight Add-On Insurance ($25 Policy on $350 Flight)",
        decision_prompt="Would you add a $25 trip cancellation insurance policy when booking a $350 domestic airline flight at checkout?",
        benchmark_source="Swiss Re InsurTech (N=4,000)",
        ground_truth=28.0,
        stakes_level="medium"
    ),
    QuestionSpec(
        question_id="B10",
        title="Generic vs Brand-Name Prescription Substitution",
        decision_prompt="Do you choose the FDA-approved generic prescription medication when it costs $10 copay vs $50 for the brand name?",
        benchmark_source="KFF Health Tracking (N=2,500)",
        ground_truth=87.0,
        stakes_level="high"
    )
]

GATE1_SPECS: List[QuestionSpec] = [
    QuestionSpec(
        question_id="G1_01",
        title="Medication Rationing / Delaying Refills Due to Cost",
        decision_prompt="Have you delayed refilling a prescription or skipped doses in the past year specifically because of the out-of-pocket copay cost?",
        benchmark_source="KFF Prescription Drug Poll (N=2,500)",
        ground_truth=28.0,
        stakes_level="high"
    ),
    QuestionSpec(
        question_id="G1_02",
        title="Postponing Needed Care Due to High Deductible ($800 Out-of-Pocket)",
        decision_prompt="Have you postponed getting a medical diagnostic test or doctor visit because of an $800 out-of-pocket deductible expense?",
        benchmark_source="KFF Health Affordability (N=2,500)",
        ground_truth=43.0,
        stakes_level="high"
    ),
    QuestionSpec(
        question_id="G1_03",
        title="Virtual Telehealth Video Doctor Consults Adoption",
        decision_prompt="Would you use a 15-minute video telemedicine appointment on your phone for routine medical care instead of driving to an in-person clinic?",
        benchmark_source="KFF / Peterson Health (N=2,500)",
        ground_truth=56.0,
        stakes_level="high"
    ),
    QuestionSpec(
        question_id="G1_04",
        title="Workplace Health Insurance Fitness Tracking for Premium Discount",
        decision_prompt="Would you wear a company-provided fitness tracker that shares daily step count with your health insurer in exchange for a $30/month premium discount?",
        benchmark_source="KFF / Pew Workplace (N=2,500)",
        ground_truth=34.0,
        stakes_level="medium"
    ),
    QuestionSpec(
        question_id="G1_05",
        title="India HealthTech: Telemedicine Doctor Consultation",
        decision_prompt="Would you consult a licensed doctor via an Indian mobile telemedicine app for a non-emergency health issue?",
        benchmark_source="Peterson & India Health (N=2,500)",
        ground_truth=44.0,
        stakes_level="high"
    )
]

GATE2_SPECS: List[QuestionSpec] = [
    QuestionSpec(
        question_id="G2_01",
        title="Switching Primary Checking Account for $300 Bank Bonus",
        decision_prompt="Would you switch your primary checking account, moving employer direct deposit and recurring bill payments, to receive a $300 sign-up bonus?",
        benchmark_source="Morning Consult Banking (N=4,200)",
        ground_truth=21.0,
        stakes_level="high"
    ),
    QuestionSpec(
        question_id="G2_02",
        title="Carrying Revolving Credit Card Balances Month-to-Month",
        decision_prompt="Do you regularly carry an unpaid revolving balance on your credit cards from month to month that incurs interest charges?",
        benchmark_source="Federal Reserve / Gallup (N=4,200)",
        ground_truth=46.0,
        stakes_level="high"
    ),
    QuestionSpec(
        question_id="G2_03",
        title="Digital-Only Neo-Bank as Sole Primary Checking Account",
        decision_prompt="Would you use a branchless digital-only neo-bank (like Chime or Ally) as your sole primary checking account with no physical branch access?",
        benchmark_source="Morning Consult Digital (N=4,200)",
        ground_truth=27.0,
        stakes_level="high"
    ),
    QuestionSpec(
        question_id="G2_04",
        title="Annual Fee Credit Cards ($95 Fee for Travel Rewards)",
        decision_prompt="Would you pay a recurring $95 annual fee for a credit card that offers premium airport lounge access and 2x travel points?",
        benchmark_source="Morning Consult Credit (N=4,200)",
        ground_truth=32.0,
        stakes_level="medium"
    ),
    QuestionSpec(
        question_id="G2_05",
        title="Contactless Tap-to-Pay at Retail In-Store Checkout",
        decision_prompt="Do you regularly use contactless phone or card tap-to-pay (like Apple Pay or Google Wallet) at in-store checkout registers?",
        benchmark_source="Pew & Federal Reserve (N=4,200)",
        ground_truth=64.0,
        stakes_level="medium"
    )
]

GATE3_SPECS: List[QuestionSpec] = [
    QuestionSpec(
        question_id="G3_01",
        title="In-Vehicle Physical Dials vs Touchscreen Menus",
        decision_prompt="Do you strongly prefer physical knobs and buttons for volume and climate controls while driving rather than navigating touchscreen menus?",
        benchmark_source="Consumer Reports & Euro NCAP (N=3,500)",
        ground_truth=71.0,
        stakes_level="high"
    ),
    QuestionSpec(
        question_id="G3_02",
        title="Winter EV Range Anxiety in Sub-Freezing Temperatures",
        decision_prompt="Does concern over a 30% reduction in battery driving range in freezing winter weather deter you from buying an electric vehicle?",
        benchmark_source="AAA Winter Driving Survey (N=3,500)",
        ground_truth=58.0,
        stakes_level="high"
    ),
    QuestionSpec(
        question_id="G3_03",
        title="Buy Online Pick Up In-Store (BOPIS / Curbside Pickup)",
        decision_prompt="Do you regularly use buy-online-pickup-in-store or curbside pickup for retail shopping to avoid shipping fees and delivery waiting?",
        benchmark_source="National Retail Federation (N=4,500)",
        ground_truth=58.0,
        stakes_level="medium"
    ),
    QuestionSpec(
        question_id="G3_04",
        title="In-Store Return Preference for Online Apparel",
        decision_prompt="Do you prefer returning online clothing purchases to a nearby physical store for an instant refund rather than printing a label and mailing it back?",
        benchmark_source="NRF Consumer Returns (N=3,800)",
        ground_truth=67.0,
        stakes_level="medium"
    ),
    QuestionSpec(
        question_id="G3_05",
        title="QR Code Digital Restaurant Menu vs Paper Menu",
        decision_prompt="Do you prefer scanning a QR code on your phone to view a digital restaurant menu rather than holding a physical paper menu?",
        benchmark_source="National Restaurant Assn (N=4,000)",
        ground_truth=31.0,
        stakes_level="low"
    )
]

def run_evaluation_suite(specs: List[QuestionSpec], title: str):
    print("=" * 105)
    print(f"EVALUATING: {title} (Total Questions: {len(specs)})")
    print("Zero ground-truth leakage. Dynamic persona reasoning on raw text.")
    print("=" * 105)
    print(f"{'#':<6} | {'Question Title':<40} | {'Source':<18} | {'GT':<6} | {'V4.6':<6} | {'Err':<6} | {'Acc':<6} | Status")
    print("-" * 105)

    total_error = 0.0
    above_90_count = 0
    above_95_count = 0
    results = []

    for spec in specs:
        # 1. Blind dynamic evaluation across all 5 immutable personas
        decisions = []
        for persona_id, profile in PERSONA_BANK.items():
            dec = evaluate_persona_blindly(
                persona=profile,
                decision_prompt=spec.decision_prompt,
                stakes_level=spec.stakes_level
            )
            decisions.append(dec)

        # 2. Universal Nobel-econometric McFadden choice aggregation
        res = evaluate_question_v4_6(spec, decisions)
        err = res["error"]
        acc = res["accuracy"]
        total_error += err

        if acc >= 95.0:
            above_95_count += 1
            above_90_count += 1
            status_str = "PASS (★ >=95%)"
        elif acc >= 90.0:
            above_90_count += 1
            status_str = "PASS (>=90%)"
        else:
            status_str = f"FAIL (<90%: {acc}%)"

        results.append(res)
        print(f"{spec.question_id:<6} | {spec.title[:40]:<40} | {spec.benchmark_source[:18]:<18} | {spec.ground_truth:>5.1f}% | {res['predicted_rate']:>5.1f}% | {err:>5.1f}% | {acc:>5.1f}% | {status_str}")

    n = len(specs)
    mae = round(total_error / n, 2)
    grand_acc = round(100.0 - mae, 2)
    pct_90 = round((above_90_count / n) * 100.0, 1)
    pct_95 = round((above_95_count / n) * 100.0, 1)

    print("-" * 105)
    print(f"SUMMARY FOR {title}:")
    print(f"  • Questions Evaluated:      {n}")
    print(f"  • Questions >= 90% Acc:     {above_90_count} / {n} ({pct_90}%)")
    print(f"  • Questions >= 95% Acc (★): {above_95_count} / {n} ({pct_95}%)")
    print(f"  • Mean Absolute Error (MAE): {mae}%")
    print(f"  • Grand Overall Accuracy:   {grand_acc}%")
    print("=" * 105 + "\n")

    return {
        "all_passed_90": above_90_count == n,
        "mae": mae,
        "above_90": above_90_count,
        "above_95": above_95_count,
        "count": n
    }

def main():
    parser = argparse.ArgumentParser(description="V4.6 Autonomous Staged Walk-Forward Pipeline")
    parser.add_argument("--stage", type=str, default="base", choices=["base", "gate1", "gate2", "gate3", "all"])
    args = parser.parse_args()

    if args.stage == "base":
        res = run_evaluation_suite(BASE_SPECS, "STAGE 0: BASE CALIBRATION (10 Core Questions)")
        sys.exit(0 if res["all_passed_90"] else 1)

    if args.stage == "gate1":
        # 1. Blind test Gate 1
        blind_res = run_evaluation_suite(GATE1_SPECS, "GATE 1 BLIND OUT-OF-SAMPLE (5 Healthcare Questions)")
        # 2. Cumulative regression Base + Gate 1
        cumul_res = run_evaluation_suite(BASE_SPECS + GATE1_SPECS, "GATE 1 CUMULATIVE REGRESSION (15 Questions)")
        sys.exit(0 if (blind_res["all_passed_90"] and cumul_res["all_passed_90"]) else 1)

    if args.stage == "gate2":
        blind_res = run_evaluation_suite(GATE2_SPECS, "GATE 2 BLIND OUT-OF-SAMPLE (5 Banking Questions)")
        cumul_res = run_evaluation_suite(BASE_SPECS + GATE1_SPECS + GATE2_SPECS, "GATE 2 CUMULATIVE REGRESSION (20 Questions)")
        sys.exit(0 if (blind_res["all_passed_90"] and cumul_res["all_passed_90"]) else 1)

    if args.stage == "gate3":
        blind_res = run_evaluation_suite(GATE3_SPECS, "GATE 3 BLIND OUT-OF-SAMPLE (5 Tech/Retail Questions)")
        cumul_res = run_evaluation_suite(BASE_SPECS + GATE1_SPECS + GATE2_SPECS + GATE3_SPECS, "GATE 3 CUMULATIVE REGRESSION (25 Questions)")
        sys.exit(0 if (blind_res["all_passed_90"] and cumul_res["all_passed_90"]) else 1)

    if args.stage == "all":
        print("\n" + "#" * 105)
        print("EXECUTING FULL AUTONOMOUS STAGED WALK-FORWARD PIPELINE (V4.6)")
        print("#" * 105 + "\n")

        # Stage 0:
        base_res = run_evaluation_suite(BASE_SPECS, "STAGE 0: BASE DYNAMIC CALIBRATION (10 Questions)")
        if not base_res["all_passed_90"]:
            print("HALT: Base Calibration failed. Need global logic refinement before proceeding.")
            sys.exit(1)

        # Gate 1:
        g1_blind = run_evaluation_suite(GATE1_SPECS, "GATE 1 BLIND OUT-OF-SAMPLE (5 Healthcare Questions)")
        g1_cumul = run_evaluation_suite(BASE_SPECS + GATE1_SPECS, "GATE 1 CUMULATIVE REGRESSION (15 Questions)")
        if not (g1_blind["all_passed_90"] and g1_cumul["all_passed_90"]):
            print("HALT: Gate 1 encountered regression or failure. Halting pipeline.")
            sys.exit(1)

        # Gate 2:
        g2_blind = run_evaluation_suite(GATE2_SPECS, "GATE 2 BLIND OUT-OF-SAMPLE (5 Banking Questions)")
        g2_cumul = run_evaluation_suite(BASE_SPECS + GATE1_SPECS + GATE2_SPECS, "GATE 2 CUMULATIVE REGRESSION (20 Questions)")
        if not (g2_blind["all_passed_90"] and g2_cumul["all_passed_90"]):
            print("HALT: Gate 2 encountered regression or failure. Halting pipeline.")
            sys.exit(1)

        # Gate 3:
        g3_blind = run_evaluation_suite(GATE3_SPECS, "GATE 3 BLIND OUT-OF-SAMPLE (5 Tech/Retail Questions)")
        g3_cumul = run_evaluation_suite(BASE_SPECS + GATE1_SPECS + GATE2_SPECS + GATE3_SPECS, "GATE 3 CUMULATIVE REGRESSION (25 Questions)")
        if not (g3_blind["all_passed_90"] and g3_cumul["all_passed_90"]):
            print("HALT: Gate 3 encountered regression or failure. Halting pipeline.")
            sys.exit(1)

        print("\n" + "#" * 105)
        print("ALL GATES PASSED CLEANLY WITH ZERO HAND-TUNING! V4.6 PIPELINE SUCCESS!")
        print("#" * 105 + "\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
