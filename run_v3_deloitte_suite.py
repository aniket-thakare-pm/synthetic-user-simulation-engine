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
        "name": "Deloitte Q1: $5 Monthly Price Hike Cancellation",
        "category": "DIGITAL_SUBSCRIPTIONS_AND_COMMERCE",
        "text": "Would you cancel your favorite video streaming service if the monthly subscription price increased by $5 per month?",
        "ground_truth": 61.0,
        "v1_score": 61.3,
        "v2_1_score": 63.6
    },
    {
        "id": "Q2",
        "name": "Deloitte Q2: Show Hopping / Serial Churn Behavior",
        "category": "DIGITAL_SUBSCRIPTIONS_AND_COMMERCE",
        "text": "Do you subscribe to a streaming service just to watch a specific movie or show, and then cancel as soon as you finish watching it?",
        "ground_truth": 47.0,
        "v1_score": 48.0,
        "v2_1_score": 48.5
    }
]

print("=" * 90)
print(" 🎬 RUNNING DELOITTE DIGITAL MEDIA TRENDS BENCHMARK ON ENGINE V3")
print(" 🔬 Framework: Category-Aware Mental Accounting Choice Architecture")
print(" 👥 Panel: 5 MECE US General Consumer Personas (N=2,005 Empirical Ground Truth)")
print("=" * 90)

all_results = []
total_err_v3 = 0.0

for q_idx, q in enumerate(QUESTIONS, 1):
    print(f"\n📋 TEST {q_idx}: {q['name']}")
    print(f"   Ground Truth: {q['ground_truth']:.1f}% | V1: {q['v1_score']:.1f}% | V2.1: {q['v2_1_score']:.1f}%")
    print("-" * 80)
    
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
        print(f"  • [{p.name}] W:{p.population_weight*100:>2.0f}% -> {res['decision_stance']:<3} | {v_str} => Churn: {score:>5.1f}% ({elapsed:.1f}s)")
        print(f"    Reasoning: \"{res['response_text'][:90]}...\"")
        persona_outputs.append(res)
        time.sleep(1.2)
        
    gt = q["ground_truth"]
    err_v3 = q_weighted_sum - gt
    total_err_v3 += abs(err_v3)
    
    print("-" * 80)
    print(f"  🎯 Post-Stratified Churn Rate (V3): {q_weighted_sum:.1f}%")
    print(f"  📊 Empirical Human Ground Truth:   {gt:.1f}%")
    print(f"  📐 V3 Prediction Error (Δ):        {err_v3:+.1f}%")
    
    all_results.append({
        "id": q["id"],
        "name": q["name"],
        "ground_truth": gt,
        "v1_score": q["v1_score"],
        "v2_1_score": q["v2_1_score"],
        "v3_score": round(q_weighted_sum, 1),
        "v3_error": round(err_v3, 1),
        "persona_breakdown": persona_outputs
    })

mae_v3 = total_err_v3 / len(QUESTIONS)
print("\n" + "=" * 90)
print(f"🏁 DELOITTE BENCHMARK MAE (V3): {mae_v3:.1f}% (Accuracy: {100-mae_v3:.1f}%)")
print("=" * 90)

output_file = os.path.join(PROJECT_ROOT, "deloitte_v3_benchmark_results.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)
