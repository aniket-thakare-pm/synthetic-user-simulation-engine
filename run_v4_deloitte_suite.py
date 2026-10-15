"""
run_v4_deloitte_suite.py
Runs the 5-Question Deloitte Digital Media Trends Benchmark (N=2,005) on Engine V4
(Empirical-Bayesian Discrete Choice Architecture with Market Router).
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

QUESTIONS = [
    {
        "id": "Q1",
        "title": "$5 Monthly Price Hike Churn",
        "category": "DIGITAL_SUBSCRIPTIONS_AND_COMMERCE",
        "text": "Would you cancel your favorite video streaming service if the monthly subscription price increased by $5 per month?",
        "action_a": "Cancel your streaming subscription to avoid the $5 monthly price increase",
        "baseline_b": "Accept the $5 price increase and keep your subscription and watchlist",
        "ground_truth": 61.0,
        "v1_score": 61.3,
        "v3_1_score": 42.0
    },
    {
        "id": "Q2",
        "title": "Show Hopping / Serial Churn Behavior",
        "category": "DIGITAL_SUBSCRIPTIONS_AND_COMMERCE",
        "text": "Do you subscribe to a streaming service just to watch a specific movie or show, and then cancel as soon as you finish watching it?",
        "action_a": "Subscribe only to watch a specific show and cancel as soon as you finish",
        "baseline_b": "Keep the streaming subscription active continuously month-to-month",
        "ground_truth": 47.0,
        "v1_score": 48.0,
        "v3_1_score": 57.2
    },
    {
        "id": "Q3",
        "title": "Canceled Paid Subscription in Last 6 Months",
        "category": "DIGITAL_SUBSCRIPTIONS_AND_COMMERCE",
        "text": "In the past six months, have you canceled or decided not to renew at least one paid video streaming subscription?",
        "action_a": "Cancel at least one streaming subscription to cut costs or eliminate unused services",
        "baseline_b": "Keep all current streaming subscriptions active without canceling",
        "ground_truth": 54.0,
        "v1_score": 59.5,
        "v3_1_score": 64.0
    },
    {
        "id": "Q4",
        "title": "Ad-Supported Tier Switch (Half Price)",
        "category": "DIGITAL_SUBSCRIPTIONS_AND_COMMERCE",
        "text": "If your favorite paid streaming video service offered a plan with commercial breaks at half the monthly price, would you switch to that ad-supported plan to save money?",
        "action_a": "Switch to the half-price ad-supported plan with commercials to save money",
        "baseline_b": "Keep paying full price for the ad-free premium tier to avoid commercials",
        "ground_truth": 52.0,
        "v1_score": 54.2,
        "v3_1_score": 56.6
    },
    {
        "id": "Q5",
        "title": "Single Show Binge & Immediate Cancel",
        "category": "DIGITAL_SUBSCRIPTIONS_AND_COMMERCE",
        "text": "Have you signed up for a subscription video on-demand service specifically to watch a specific season or program and canceled as soon as you finished watching?",
        "action_a": "Sign up for a single season/show and immediately cancel upon finishing",
        "baseline_b": "Keep the subscription rolling after watching the show",
        "ground_truth": 47.0,
        "v1_score": 48.0,
        "v3_1_score": 69.9
    }
]

print("=" * 95)
print(" 📺 RUNNING 5-QUESTION DELOITTE STUDY ON ENGINE V4 (EB-DCA)")
print("=" * 95)

results = []
total_abs_error_v4 = 0.0

for idx, q in enumerate(QUESTIONS):
    market_code, personas = resolve_market_and_personas(q["text"], explicit_market="US")
    print(f"\n📋 [{idx+1}/5] {q['id']}: {q['title']} (Market: {market_code})")
    print(f"   Ground Truth: {q['ground_truth']}% | V1: {q['v1_score']}% | V3.1: {q['v3_1_score']}%")
    print("-" * 90)

    post_stratified_score = 0.0
    persona_details = []

    for p in personas:
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
print(" 🏁 FINAL 5-QUESTION DELOITTE BENCHMARK COMPARISON: V1 vs V3.1 vs V4")
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

out_file = os.path.join(PROJECT_ROOT, "deloitte_5q_v4_results.json")
with open(out_file, "w", encoding="utf-8") as f:
    json.dump({"benchmark": "Deloitte 5Q V4", "mae": mae_v4, "accuracy": acc_v4, "results": results}, f, indent=2)
print(f"\n✅ Results saved to: {out_file}")
