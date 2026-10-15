"""
run_v4_2_tipping_stress_test.py
Aggressive Stress Test for Engine V4.2 on an Untouched Behavioral Domain:
Pew Research Center National Survey: "Tipping Culture in America & Point-of-Sale iPad Screens"
(N=11,945 US Adults, November 2023)
"""

import sys
import os
import time
import json

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
sys.stdout.reconfigure(encoding='utf-8')

from v4_2.engine_v4_2 import interview_persona_v4_2
from v4.market_router_v4 import resolve_market_and_personas
from interview_engine import load_env_key

GEMINI_KEY = os.environ.get("GEMINI_API_KEY") or load_env_key()

TIPPING_QUESTIONS = [
    {
        "id": "Q1",
        "title": "Sit-Down Restaurant Dining Table Service Tipping",
        "category": "EVERYDAY_CONSUMABLES_AND_GROCERY",
        "text": "When you eat a meal at a casual sit-down restaurant where a server takes your order and brings food to your table, do you always or often leave a standard tip of at least 15% to 20%?",
        "action_a": "Always or often leave a tip of at least 15% to 20% for table service",
        "baseline_b": "Rarely or never leave a tip for table service",
        "pew_ground_truth": 92.0  # Pew: 81% always + 11% often = 92%
    },
    {
        "id": "Q2",
        "title": "Fast-Casual / Walk-Up Counter Pickup Tipping",
        "category": "EVERYDAY_CONSUMABLES_AND_GROCERY",
        "text": "When you buy food at a fast-casual or counter-service restaurant where you order at a register and pick up your own food at the counter, do you regularly choose to leave a tip when prompted on the register screen?",
        "action_a": "Regularly leave a tip on the counter terminal screen for counter pickup",
        "baseline_b": "Press 'No Tip' or skip tipping when picking up your own food at the counter",
        "pew_ground_truth": 12.0  # Pew: 7% always + 5% often = 12%
    },
    {
        "id": "Q3",
        "title": "Coffee Shop Counter iPad Swivel Screen Tipping",
        "category": "EVERYDAY_CONSUMABLES_AND_GROCERY",
        "text": "When you buy a brewed coffee or espresso beverage at a coffee shop counter, the barista swivels the digital tablet around showing preset tip options ($1, $2, 18%, 20%). Do you leave a tip on the screen?",
        "action_a": "Leave a tip on the digital tablet screen for your coffee order",
        "baseline_b": "Select 'No Tip' or bypass the tip prompt screen",
        "pew_ground_truth": 25.0  # Pew: 12% always + 13% often = 25%
    },
    {
        "id": "Q4",
        "title": "Mobile App Food Delivery Driver Tipping",
        "category": "EVERYDAY_CONSUMABLES_AND_GROCERY",
        "text": "When ordering a meal delivered to your home through a mobile app like DoorDash or UberEats, do you regularly add a tip for the delivery driver bringing the food to your door?",
        "action_a": "Always or often add a tip for the food delivery driver in the app",
        "baseline_b": "Skip adding a tip or tip rarely for app food delivery",
        "pew_ground_truth": 76.0  # Pew: 59% always + 17% often = 76%
    },
    {
        "id": "Q5",
        "title": "Mandatory Automatic Restaurant Service Charges",
        "category": "EVERYDAY_CONSUMABLES_AND_GROCERY",
        "text": "A restaurant automatically adds a mandatory 18% to 20% 'service fee' or 'wellness surcharge' to your final bill instead of traditional voluntary tipping. Do you oppose or support this practice?",
        "action_a": "Strongly oppose mandatory automatic service fees added to restaurant bills",
        "baseline_b": "Support or accept mandatory automatic service fees instead of tipping",
        "pew_ground_truth": 72.0  # Pew: 72% oppose automatic service charges
    }
]

def run_tipping_stress_test():
    print("=" * 85)
    print("ENGINE V4.2 STRESS TEST: PEW RESEARCH NATIONAL TIPPING SURVEY (N=11,945)")
    print("Testing Extreme Dynamic Range (12% to 92%) on an Untouched Behavioral Domain")
    print("=" * 85)

    total_error = 0.0
    suite_results = []

    for q in TIPPING_QUESTIONS:
        qid = q["id"]
        title = q["title"]
        text = q["text"]
        action_a = q["action_a"]
        baseline_b = q["baseline_b"]
        gt = q["pew_ground_truth"]

        print(f"\n--- Running {qid}: {title} ---")
        market, personas = resolve_market_and_personas(text)

        weighted_score = 0.0
        total_weight = 0.0
        persona_responses = []

        for p in personas:
            res = interview_persona_v4_2(
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
            print(f"  [{p.name}]: Stance={res['decision_stance']}, Shift={res['persona_shift']:+.2f}, Archetype={res['empirical_archetype']} -> Score={score:.1f}%")
            time.sleep(0.4)

        v4_2_prediction = round(weighted_score / total_weight, 1) if total_weight > 0 else 50.0
        error = round(abs(v4_2_prediction - gt), 1)
        total_error += error

        archetype_used = persona_responses[0]["empirical_archetype"]
        base_rate = persona_responses[0]["empirical_base_rate"]

        print(f"==> Archetype Routed: {archetype_used} (Prior: {base_rate}%)")
        print(f"==> Predicted Score: {v4_2_prediction}% | Pew Ground Truth: {gt}% | Error: {error}%")

        suite_results.append({
            "question_id": qid,
            "title": title,
            "pew_ground_truth": gt,
            "v4_2_prediction": v4_2_prediction,
            "error": error,
            "archetype_matched": archetype_used,
            "base_rate_used": base_rate,
            "persona_responses": persona_responses
        })

    mae = round(total_error / len(TIPPING_QUESTIONS), 2)
    accuracy = round(100.0 - mae, 2)

    print("\n" + "=" * 85)
    print("STRESS TEST BENCHMARK SUMMARY")
    print(f"Mean Absolute Error (MAE): {mae}%")
    print(f"Prediction Accuracy: {accuracy}%")
    print("=" * 85)

    out_file = os.path.join(PROJECT_ROOT, "pew_tipping_5q_v4_2_results.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({
            "engine": "Engine V4.2 (Hybrid Architecture)",
            "benchmark": "Pew Research Center Tipping Culture in America (N=11,945)",
            "mae": mae,
            "accuracy": accuracy,
            "results": suite_results
        }, f, indent=2)

    print(f"Results written to: {out_file}")

if __name__ == "__main__":
    run_tipping_stress_test()
