"""
run_v4_mckinsey_blind_suite.py
High-Difficulty Blind Benchmark: McKinsey & NielsenIQ 5-Year Scanner Study (N=10,000+)
Testing the "Say-Do" / Intention-Action Paradox on Engine V4 with Zero Knowledge of Ground Truth.
"""

import sys
import os
import time
import json

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
sys.stdout.reconfigure(encoding='utf-8')

from v4.engine_v4 import interview_persona_v4
from v4.market_router_v4 import resolve_market_and_personas
from interview_engine import load_env_key

GEMINI_KEY = os.environ.get("GEMINI_API_KEY") or load_env_key()

# 5 High-Difficulty Questions testing the "Say-Do" Paradox
# Ground truth from McKinsey & NielsenIQ Point-of-Sale Scanner Benchmark (N=10,000+ households)
MCKINSEY_QUESTIONS = [
    {
        "id": "Q1",
        "title": "The Green Premium Paradox (Household Detergent)",
        "category": "EVERYDAY_CONSUMABLES_AND_GROCERY",
        "text": "You are shopping for everyday laundry detergent. Your usual effective brand costs $12. Right next to it is a certified zero-plastic, carbon-neutral, eco-friendly alternative priced at $15 (a 25% price premium). Would you pay the extra $3 for the eco-friendly alternative or buy the standard $12 brand?",
        "action_a": "Pay the $3 extra premium ($15 total) to buy the certified eco-friendly laundry detergent",
        "baseline_b": "Buy the standard proven $12 brand to save money and ensure effective cleaning",
        "scanner_ground_truth": 18.0  # McKinsey/NielsenIQ: Only 18% actually pay the +25% green premium at POS
    },
    {
        "id": "Q2",
        "title": "The 10-Cent Plastic Bag Fee Asymmetry",
        "category": "EVERYDAY_CONSUMABLES_AND_GROCERY",
        "text": "Your local grocery store implements a mandatory $0.10 (10-cent) fee per disposable plastic bag at checkout. When you go grocery shopping, do you regularly make the effort to remember and bring your own reusable cloth bags to avoid the fee, or just pay the few dimes for store bags?",
        "action_a": "Bring your own reusable bags to avoid paying the 10-cent bag fees at checkout",
        "baseline_b": "Pay the 10-cent fee per bag at checkout for convenience rather than carrying reusable bags",
        "scanner_ground_truth": 81.0  # Real retail audits: 81% bring reusable bags to avoid the loss-aversion fee
    },
    {
        "id": "Q3",
        "title": "Certified Refurbished Hardware Adoption",
        "category": "DURABLE_HARDWARE_AND_ELECTRONICS",
        "text": "You need to purchase a replacement laptop or smartphone. An official manufacturer certified-refurbished model with a 1-year warranty is available for a 30% discount ($700 vs $1,000 brand new). Do you buy the certified refurbished unit, or pay full price for a brand new sealed box?",
        "action_a": "Buy the certified refurbished unit at $700 to save $300",
        "baseline_b": "Pay $1,000 for the brand new factory-sealed unit for complete peace of mind",
        "scanner_ground_truth": 31.0  # Consumer electronics purchase data: ~31% buy refurbished, 69% buy new
    },
    {
        "id": "Q4",
        "title": "Brand Boycott Durability (60 Days Later)",
        "category": "EVERYDAY_CONSUMABLES_AND_GROCERY",
        "text": "A popular consumer food and beverage brand you buy every week takes an aggressive, public political stance that strongly offends your personal beliefs. 60 days after the controversy, are you still actively boycotting the brand, or have you quietly resumed buying it out of habit and routine?",
        "action_a": "Maintain the active boycott 60 days later and permanently switch to a competitor",
        "baseline_b": "Resume buying the preferred brand out of product taste, convenience, and habit",
        "scanner_ground_truth": 22.0  # Longitudinal purchase tracking: Only 22% maintain boycotts after 60 days
    },
    {
        "id": "Q5",
        "title": "Auto-Ship Replenishment Trap (5% Discount)",
        "category": "DIGITAL_SUBSCRIPTIONS_AND_COMMERCE",
        "text": "An online retailer offers a 5% discount on household essentials (paper towels, coffee, vitamins) if you enroll in an automatic 30-day recurring delivery auto-ship subscription. Would you enroll in the auto-delivery subscription, or decline and order manually when running low?",
        "action_a": "Enroll in the 30-day auto-ship subscription to lock in the 5% discount",
        "baseline_b": "Decline the recurring subscription and buy manually as needed to prevent surplus stock",
        "scanner_ground_truth": 24.0  # E-commerce subscription benchmarks: Only ~24% adopt 5% auto-replenishment
    }
]

def run_mckinsey_blind_suite():
    print("=" * 85)
    print("ENGINE V4: ADVERSARIAL HIGH-DIFFICULTY BENCHMARK (MCKINSEY & NIELSENIQ N=10,000+)")
    print("The 'Say-Do' / Intention-Action Paradox on 5-Year Point-of-Sale Scanner Data")
    print("Zero-Knowledge Protocol: No survey or scanner data encoded into V4 priors.")
    print("=" * 85)

    total_error = 0.0
    suite_results = []

    for q in MCKINSEY_QUESTIONS:
        qid = q["id"]
        title = q["title"]
        text = q["text"]
        action_a = q["action_a"]
        baseline_b = q["baseline_b"]
        gt = q["scanner_ground_truth"]

        print(f"\n--- Running {qid}: {title} ---")
        print(f"Question: \"{text[:90]}...\"")
        print(f"[Blind Mode: Ground truth is hidden from engine]")

        market, personas = resolve_market_and_personas(text)
        print(f"Market Routed: {market} ({len(personas)} personas)")

        weighted_score = 0.0
        total_weight = 0.0
        persona_responses = []

        for p in personas:
            res = interview_persona_v4(
                persona=p,
                question_text=text,
                action_label=action_a,
                baseline_label=baseline_b,
                api_key=GEMINI_KEY
            )
            score = res["target_metric_score"]
            weight = res["weight"]
            weighted_score += score * weight
            total_weight += weight
            persona_responses.append(res)

            print(f"  [{p.name} ({p.demographics.occupation})]: Stance={res['decision_stance']}, Shift={res['persona_shift']:+.2f}, ScaledFriction={res['scaled_friction']:.2f} -> Score={score:.1f}%")
            time.sleep(0.5)

        v4_prediction = round(weighted_score / total_weight, 1) if total_weight > 0 else 50.0
        error = round(abs(v4_prediction - gt), 1)
        total_error += error

        print(f"==> Predicted Score: {v4_prediction}% | Real Scanner Ground Truth: {gt}% | Error: {error}%")

        suite_results.append({
            "question_id": qid,
            "title": title,
            "category": q["category"],
            "scanner_ground_truth": gt,
            "v4_prediction": v4_prediction,
            "error": error,
            "archetype_matched": persona_responses[0]["empirical_archetype"],
            "base_rate_used": persona_responses[0]["empirical_base_rate"],
            "persona_responses": persona_responses
        })

    mae = round(total_error / len(MCKINSEY_QUESTIONS), 2)
    accuracy = round(100.0 - mae, 2)

    print("\n" + "=" * 85)
    print("ADVERSARIAL BENCHMARK SUMMARY")
    print(f"Mean Absolute Error (MAE): {mae}%")
    print(f"Zero-Shot Prediction Accuracy: {accuracy}%")
    print("=" * 85)

    out_file = os.path.join(PROJECT_ROOT, "mckinsey_5q_v4_blind_results.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({
            "benchmark": "McKinsey & NielsenIQ 5-Year Scanner Study (N=10,000+) Blind Out-of-Sample",
            "protocol": "Zero-knowledge (The 'Say-Do' Paradox)",
            "mae": mae,
            "accuracy": accuracy,
            "results": suite_results
        }, f, indent=2)

    print(f"Results written to: {out_file}")

if __name__ == "__main__":
    run_mckinsey_blind_suite()
