"""
run_v4_india_suite.py
Runs the 5-Question India Consumer Adoption Benchmark (N=2,500) on Engine V4
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
        "title": "Buy-Now-Pay-Later (BNPL) & 0% No-Cost EMI Adoption",
        "category": "FINTECH_CREDIT_AND_LENDING",
        "text": "When buying consumer electronics or lifestyle goods online (₹3,000 to ₹25,000), do you use or intend to use Buy-Now-Pay-Later (BNPL) or 0% No-Cost EMI checkout options instead of paying the full amount upfront via debit card or UPI?",
        "action_a": "Use Buy-Now-Pay-Later (BNPL) or 0% No-Cost EMI checkout option",
        "baseline_b": "Pay the full amount upfront via debit card or UPI",
        "ground_truth": 62.0,
        "v1_score": 53.5,
        "v3_1_score": 59.7
    },
    {
        "id": "Q2",
        "title": "Online Telemedicine Video Consultations Trust",
        "category": "HEALTH_AND_DIAGNOSTICS",
        "text": "Would you consult a certified doctor over a scheduled video call on a smartphone app instead of physically visiting a local neighborhood clinic for common health issues?",
        "action_a": "Consult a certified doctor over scheduled video call on a smartphone app",
        "baseline_b": "Physically visit a local neighborhood clinic for common health issues",
        "ground_truth": 44.0,
        "v1_score": 84.5,
        "v3_1_score": 43.2
    },
    {
        "id": "Q3",
        "title": "Electric 2-Wheeler (EV Scooter) Adoption Intent",
        "category": "MOBILITY_AND_DURABLES",
        "text": "When buying a new two-wheeler for daily commuting, would you switch to an Electric Scooter (Ola/Ather/TVS EV) over a petrol scooter to save on monthly fuel costs?",
        "action_a": "Switch to an Electric Scooter (Ola/Ather/TVS EV) for daily commuting",
        "baseline_b": "Keep or buy a traditional petrol scooter (Honda Activa) for daily commuting",
        "ground_truth": 54.0,
        "v1_score": 48.5,
        "v3_1_score": 40.1
    },
    {
        "id": "Q4",
        "title": "Online Direct Insurance Purchase (PolicyBazaar)",
        "category": "INSURANCE_AND_PROTECTION",
        "text": "Would you buy a health or term life insurance policy directly through an online app (like PolicyBazaar) without consulting an offline insurance agent?",
        "action_a": "Buy health or term life insurance directly through an online app (PolicyBazaar)",
        "baseline_b": "Consult and buy through a traditional offline insurance agent",
        "ground_truth": 38.0,
        "v1_score": 34.8,
        "v3_1_score": 43.3
    },
    {
        "id": "Q5",
        "title": "Digital Mutual Fund / SIP Investment via Apps",
        "category": "WEALTH_AND_INVESTMENTS",
        "text": "When investing in financial markets or starting a Mutual Fund SIP, do you use direct smartphone investment apps (Groww/Zerodha) instead of visiting a physical bank branch or using an offline broker?",
        "action_a": "Use smartphone investment apps (Groww/Zerodha) to invest in Mutual Funds via monthly SIPs",
        "baseline_b": "Visit a physical bank branch or invest through a traditional offline broker",
        "ground_truth": 47.0,
        "v1_score": 39.5,
        "v3_1_score": 57.9
    }
]

print("=" * 95)
print(" 🇮🇳 RUNNING 5-QUESTION INDIA CONSUMER STUDY ON ENGINE V4 (EB-DCA)")
print("=" * 95)

results = []
total_abs_error_v4 = 0.0

for idx, q in enumerate(QUESTIONS):
    market_code, personas = resolve_market_and_personas(q["text"], explicit_market="IN")
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
print(" 🏁 FINAL 5-QUESTION INDIA BENCHMARK COMPARISON: V1 vs V3.1 vs V4")
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

out_file = os.path.join(PROJECT_ROOT, "india_5q_v4_results.json")
with open(out_file, "w", encoding="utf-8") as f:
    json.dump({"benchmark": "India 5Q V4", "mae": mae_v4, "accuracy": acc_v4, "results": results}, f, indent=2)
print(f"\n✅ Results saved to: {out_file}")
