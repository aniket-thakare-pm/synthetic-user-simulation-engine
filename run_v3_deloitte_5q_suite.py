import sys
import os
import time
import json

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
sys.stdout.reconfigure(encoding='utf-8')

from v3.engine_v3 import interview_persona_v3
from v3.sample_personas_v3 import SAMPLE_PERSONAS_V3
from interview_engine import load_env_key

GEMINI_KEY = os.environ.get("GEMINI_API_KEY") or load_env_key()

QUESTIONS = [
    {
        "id": "Q1",
        "title": "$5 Monthly Price Hike Churn",
        "category": "DIGITAL_SUBSCRIPTIONS_AND_COMMERCE",
        "text": "Would you cancel your favorite video streaming service if the monthly subscription price increased by $5 per month?",
        "ground_truth": 61.0,
        "v1_score": 61.3
    },
    {
        "id": "Q2",
        "title": "Show Hopping / Serial Churn Behavior",
        "category": "DIGITAL_SUBSCRIPTIONS_AND_COMMERCE",
        "text": "Do you subscribe to a streaming service just to watch a specific movie or show, and then cancel as soon as you finish watching it?",
        "ground_truth": 47.0,
        "v1_score": 48.0
    },
    {
        "id": "Q3",
        "title": "Canceled Paid Subscription in Last 6 Months",
        "category": "DIGITAL_SUBSCRIPTIONS_AND_COMMERCE",
        "text": "In the past six months, have you canceled or decided not to renew at least one paid video streaming subscription?",
        "ground_truth": 54.0,
        "v1_score": 59.5
    },
    {
        "id": "Q4",
        "title": "Ad-Supported Tier Switch (Half Price)",
        "category": "DIGITAL_SUBSCRIPTIONS_AND_COMMERCE",
        "text": "If your favorite paid streaming video service offered a plan with commercial breaks at half the monthly price, would you switch to that ad-supported plan to save money?",
        "ground_truth": 52.0,
        "v1_score": 54.2
    },
    {
        "id": "Q5",
        "title": "Single Show Binge & Immediate Cancel",
        "category": "DIGITAL_SUBSCRIPTIONS_AND_COMMERCE",
        "text": "Do you frequently sign up for a video streaming service specifically to watch a single season of a show, and cancel the subscription as soon as you finish watching?",
        "ground_truth": 47.0,
        "v1_score": 48.0
    }
]

print("=" * 95)
print(" 🎬 RUNNING FULL 5-QUESTION DELOITTE STUDY ON ENGINE V3")
print(" 🔬 Framework: Category-Aware Mental Accounting Choice Architecture")
print(" 👥 Panel: 5 MECE US General Consumer Personas (Deloitte N=2,005 Empirical Ground Truth)")
print("=" * 95)

all_results = []
total_err_v1 = 0.0
total_err_v3 = 0.0

for q_idx, q in enumerate(QUESTIONS, 1):
    print(f"\n📋 [{q_idx}/5] {q['id']}: {q['title']}")
    print(f"   Ground Truth: {q['ground_truth']:.1f}% | V1 Baseline: {q['v1_score']:.1f}%")
    print("-" * 90)
    
    q_weighted_sum = 0.0
    persona_outputs = []
    
    for p in SAMPLE_PERSONAS_V3:
        t0 = time.time()
        res = interview_persona_v3(p, q["text"], category=q["category"], api_key=GEMINI_KEY)
        elapsed = time.time() - t0
        
        score = res["target_metric_score"]
        w_contrib = score * p.population_weight
        q_weighted_sum += w_contrib
        
        v_str = f"V_new:{res['v_obj_new']:.1f} vs V_sq:{res['v_obj_sq']:.1f} | F_eff:{res['effective_friction']:>4.2f} (ΔV:{res['delta_v']:>+5.2f})"
        print(f"  • [{p.name}] W:{p.population_weight*100:>2.0f}% -> {res['decision_stance']:<3} | {v_str} => Score: {score:>5.1f}% ({elapsed:.1f}s)")
        print(f"    Reasoning: \"{res['response_text'][:90]}...\"")
        persona_outputs.append(res)
        time.sleep(1.2)
        
    gt = q["ground_truth"]
    err_v1 = q["v1_score"] - gt
    err_v3 = q_weighted_sum - gt
    
    total_err_v1 += abs(err_v1)
    total_err_v3 += abs(err_v3)
    
    print("-" * 90)
    print(f"  🎯 Post-Stratified Score (V3): {q_weighted_sum:.1f}%")
    print(f"  📊 Empirical Ground Truth:     {gt:.1f}%")
    print(f"  📐 V3 Prediction Error (Δ):    {err_v3:+.1f}% (vs V1 Error: {err_v1:+.1f}%)")
    
    all_results.append({
        "id": q["id"],
        "title": q["title"],
        "category": q["category"],
        "ground_truth": gt,
        "v1_score": q["v1_score"],
        "v1_error": round(err_v1, 1),
        "v3_score": round(q_weighted_sum, 1),
        "v3_error": round(err_v3, 1),
        "persona_breakdown": persona_outputs
    })

n = len(QUESTIONS)
mae_v1 = total_err_v1 / n
mae_v3 = total_err_v3 / n

print("\n" + "=" * 95)
print(" 🏁 FINAL 5-QUESTION DELOITTE BENCHMARK COMPARISON: V1 vs V3")
print("=" * 95)
print(f"{'Question':<38} | {'GT':<6} | {'V1 Score (Δ)':<18} | {'V3 Score (Δ)':<18}")
print("-" * 95)
for r in all_results:
    v1_str = f"{r['v1_score']:.1f}% ({r['v1_error']:+.1f}%)"
    v3_str = f"{r['v3_score']:.1f}% ({r['v3_error']:+.1f}%)"
    print(f"{r['id'] + ': ' + r['title'][:32]:<38} | {r['ground_truth']:>4.1f}% | {v1_str:>18} | {v3_str:>18}")

print("-" * 95)
print(f"🎯 V1 Baseline MAE: {mae_v1:.1f}% (Accuracy: {100-mae_v1:.1f}%)")
print(f"🏆 V3 Engine MAE:   {mae_v3:.1f}% (Accuracy: {100-mae_v3:.1f}%)")
print("=" * 95)

output_file = os.path.join(PROJECT_ROOT, "deloitte_5q_v3_results.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)
print(f"\n✅ Complete Deloitte 5Q results saved to: {output_file}")
