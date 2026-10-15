"""
run_v4_baymard_suite.py
Runs the 5-Question Baymard Institute E-Commerce Benchmark (N=4,384) on Engine V4
(Empirical-Bayesian Discrete Choice Architecture).
"""

import sys
import os
import time
import json

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
sys.stdout.reconfigure(encoding='utf-8')

from v4.engine_v4 import interview_persona_v4
from v3.sample_personas_v3 import SAMPLE_PERSONAS_V3
from interview_engine import load_env_key

GEMINI_KEY = os.environ.get("GEMINI_API_KEY") or load_env_key()

QUESTIONS = [
    {
        "id": "Q1",
        "title": "Unexpected Extra Costs (Shipping/Taxes/Fees)",
        "category": "ECOMMERCE_CHECKOUT_AND_RETAIL",
        "text": "When shopping online, would you abandon your shopping cart if extra costs like shipping, taxes, or fees are too high or disclosed only at checkout?",
        "action_a": "Abandon your shopping cart and leave empty-handed without buying",
        "baseline_b": "Pay the extra shipping/fees and complete the order to get the item",
        "ground_truth": 48.0,
        "v1_score": 15.0,
        "v3_1_score": 54.4
    },
    {
        "id": "Q2",
        "title": "Mandatory Account Creation Friction",
        "category": "ECOMMERCE_CHECKOUT_AND_RETAIL",
        "text": "When shopping online, would you abandon your order if the store forces you to create an account before completing checkout?",
        "action_a": "Abandon your order and leave empty-handed without buying",
        "baseline_b": "Create the account and complete the purchase to receive the item",
        "ground_truth": 25.0,
        "v1_score": 15.0,
        "v3_1_score": 28.2
    },
    {
        "id": "Q3",
        "title": "Slow / Unclear Delivery Speeds",
        "category": "ECOMMERCE_CHECKOUT_AND_RETAIL",
        "text": "When shopping online, would you abandon your order if estimated delivery speed is too slow or delivery time is not clearly displayed before payment?",
        "action_a": "Abandon your order and look elsewhere / leave without buying",
        "baseline_b": "Accept the slower/unclear shipping and complete checkout to get the item",
        "ground_truth": 23.0,
        "v1_score": 18.5,
        "v3_1_score": 53.5
    },
    {
        "id": "Q4",
        "title": "Customer Reviews & Star Ratings Reliance",
        "category": "ECOMMERCE_CHECKOUT_AND_RETAIL",
        "text": "When considering a purchase on an e-commerce platform, do you actively check customer reviews and star ratings before deciding to buy?",
        "action_a": "Actively check customer reviews and star ratings before buying",
        "baseline_b": "Buy directly based on images/product description without checking reviews",
        "ground_truth": 75.0,
        "v1_score": 80.0,
        "v3_1_score": 58.4
    },
    {
        "id": "Q5",
        "title": "Strict / Friction Return Policy",
        "category": "ECOMMERCE_CHECKOUT_AND_RETAIL",
        "text": "When shopping online, would you abandon your order if the return policy is strict, short (e.g. under 14 days), or requires you to pay return shipping?",
        "action_a": "Abandon your order and do not buy from this store",
        "baseline_b": "Accept the strict return policy risk and complete the purchase",
        "ground_truth": 18.0,
        "v1_score": 15.0,
        "v3_1_score": 47.3
    }
]

print("=" * 95)
print(" 🛒 RUNNING 5-QUESTION BAYMARD INSTITUTE STUDY ON ENGINE V4 (EB-DCA)")
print("=" * 95)

results = []
total_abs_error_v4 = 0.0

for idx, q in enumerate(QUESTIONS):
    print(f"\n📋 [{idx+1}/5] {q['id']}: {q['title']}")
    print(f"   Ground Truth: {q['ground_truth']}% | V1: {q['v1_score']}% | V3.1: {q['v3_1_score']}%")
    print("-" * 90)

    post_stratified_score = 0.0
    persona_details = []

    for p in SAMPLE_PERSONAS_V3:
        t0 = time.time()
        try:
            resp = interview_persona_v4(
                persona=p,
                question_text=q["text"],
                action_label=q["action_a"],
                baseline_label=q["baseline_b"],
                category=q["category"],
                api_key=GEMINI_KEY
            )
            elapsed = time.time() - t0
            score = resp["target_metric_score"]
            weight = p.population_weight
            post_stratified_score += score * weight

            persona_details.append(resp)
            print(f"  • [{p.name}] W:{int(weight*100)}% -> {resp['decision_stance']} | Shift:{resp['persona_shift']:+.1f} | ScaledF:{resp['scaled_friction']} (ΔV:{resp['delta_v']:+.2f}) => Score: {score:5.1f}% ({elapsed:.1f}s)")
            print(f"    Reasoning: \"{resp['response_text'][:95]}...\"")
        except Exception as e:
            print(f"  ❌ Error for {p.name}: {e}")

    post_stratified_score = round(post_stratified_score, 1)
    error_v4 = round(post_stratified_score - q["ground_truth"], 1)
    abs_error_v4 = abs(error_v4)
    total_abs_error_v4 += abs_error_v4

    print("-" * 90)
    print(f"  🎯 Post-Stratified Rate (V4):   {post_stratified_score}%")
    print(f"  📊 Empirical Ground Truth:      {q['ground_truth']}%")
    print(f"  📐 V4 Prediction Error (Δ):     {error_v4:+.1f}% (vs V3.1: {q['v3_1_score'] - q['ground_truth']:+.1f}%)")

    results.append({
        "question_id": q["id"],
        "title": q["title"],
        "ground_truth": q["ground_truth"],
        "v1_score": q["v1_score"],
        "v3_1_score": q["v3_1_score"],
        "v4_score": post_stratified_score,
        "v4_error": error_v4,
        "persona_responses": persona_details
    })

mae_v4 = round(total_abs_error_v4 / len(QUESTIONS), 1)
acc_v4 = round(100.0 - mae_v4, 1)

print("\n" + "=" * 95)
print(" 🏁 FINAL 5-QUESTION BAYMARD BENCHMARK COMPARISON: V1 vs V3.1 vs V4")
print("=" * 95)
print(f"{'Question':<38} | {'GT':<6} | {'V1 (Δ)':<16} | {'V3.1 (Δ)':<16} | {'V4 (Δ)':<16}")
print("-" * 95)
for r in results:
    v1_err = round(r["v1_score"] - r["ground_truth"], 1)
    v3_err = round(r["v3_1_score"] - r["ground_truth"], 1)
    v4_err = r["v4_error"]
    print(f"{r['question_id'] + ': ' + r['title'][:34]:<38} | {r['ground_truth']:>5.1f}% | {r['v1_score']:>5.1f}% ({v1_err:>+5.1f}%) | {r['v3_1_score']:>5.1f}% ({v3_err:>+5.1f}%) | {r['v4_score']:>5.1f}% ({v4_err:>+5.1f}%)")
print("-" * 95)
print(f"🏆 V4 Engine MAE: {mae_v4}% (Accuracy: {acc_v4}%)")
print("=" * 95)

out_file = os.path.join(PROJECT_ROOT, "baymard_5q_v4_results.json")
with open(out_file, "w", encoding="utf-8") as f:
    json.dump({"benchmark": "Baymard 5Q V4", "mae": mae_v4, "accuracy": acc_v4, "results": results}, f, indent=2)
print(f"\n✅ Results saved to: {out_file}")
