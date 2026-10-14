import sys
import os
import time
import json

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
sys.stdout.reconfigure(encoding='utf-8')

from v2.engine_v2_1 import interview_persona_v2_1
from v2.indian_personas_v2 import INDIAN_PERSONAS_V2
from interview_engine import load_env_key

GEMINI_KEY = os.environ.get("GEMINI_API_KEY") or load_env_key()

QUESTIONS = [
    {
        "id": "Q1",
        "title": "Buy-Now-Pay-Later (BNPL) & 0% No-Cost EMI Adoption",
        "text": "When buying consumer electronics or lifestyle goods online (₹3,000 to ₹25,000), do you use or intend to use Buy-Now-Pay-Later (BNPL) or 0% No-Cost EMI checkout options instead of paying the full amount upfront via debit card or UPI?",
        "ground_truth": 62.0,
        "v1_score": 53.5,
        "v2_0_score": 5.0
    },
    {
        "id": "Q2",
        "title": "Online Telemedicine Video Consultations Trust",
        "text": "Would you consult a certified doctor over a scheduled video call on a smartphone app instead of physically visiting a local neighborhood clinic for common health issues?",
        "ground_truth": 44.0,
        "v1_score": 84.5,
        "v2_0_score": 27.5
    },
    {
        "id": "Q3",
        "title": "Electric 2-Wheeler (EV Scooter) Adoption Intent",
        "text": "When buying a new two-wheeler for daily commuting, would you switch to an Electric Scooter (Ola/Ather/TVS EV) over a petrol scooter to save on monthly fuel costs?",
        "ground_truth": 54.0,
        "v1_score": 48.5,
        "v2_0_score": 23.5
    },
    {
        "id": "Q4",
        "title": "Online Direct Insurance Purchase (PolicyBazaar)",
        "text": "Would you buy a health or term life insurance policy directly through an online app (like PolicyBazaar) without consulting an offline insurance agent?",
        "ground_truth": 38.0,
        "v1_score": 34.8,
        "v2_0_score": 6.1
    },
    {
        "id": "Q5",
        "title": "Digital Mutual Fund / SIP Investment via Apps",
        "text": "Do you use or intend to use smartphone investment apps (Groww, Zerodha, Paytm Money) to invest in Mutual Funds via monthly SIPs instead of visiting a physical bank or traditional broker?",
        "ground_truth": 47.0,
        "v1_score": 39.5,
        "v2_0_score": 45.4
    }
]

print("=" * 90)
print(" 🚀 RUNNING FULL 5-QUESTION BENCHMARK SUITE ON ENGINE V2.1")
print(" 🔬 Framework: Objective Functional Ratings + Kenneth Train (2009) Subtraction + k=0.32")
print(" 👥 Panel: 5 MECE Indian Personas (BCG-FICCI & PwC Empirical Benchmark N=2,500)")
print("=" * 90)

all_results = []
total_err_v1 = 0.0
total_err_v2_0 = 0.0
total_err_v2_1 = 0.0

for q_idx, q in enumerate(QUESTIONS, 1):
    print(f"\n📋 [{q_idx}/5] {q['id']}: {q['title']}")
    print(f"   Ground Truth: {q['ground_truth']:.1f}% | V1: {q['v1_score']:.1f}% | V2.0 (Double-Penalty): {q['v2_0_score']:.1f}%")
    print("-" * 80)
    
    q_weighted_sum = 0.0
    persona_outputs = []
    
    for p in INDIAN_PERSONAS_V2:
        t0 = time.time()
        res = interview_persona_v2_1(p, q["text"], api_key=GEMINI_KEY)
        elapsed = time.time() - t0
        
        score = res["target_metric_score"]
        w_contrib = score * p.population_weight
        q_weighted_sum += w_contrib
        
        v_str = f"V_new:{res['v_obj_new']:.1f} vs V_sq:{res['v_obj_sq']:.1f} | FricPen:{res['friction_penalty']:>4.2f} (ΔV:{res['delta_v']:>+5.2f})"
        print(f"  • [{p.name}] W:{p.population_weight*100:>2.0f}% -> {res['decision_stance']:<3} | {v_str} => Adoption: {score:>5.1f}% ({elapsed:.1f}s)")
        print(f"    Reasoning: \"{res['response_text'][:95]}...\"")
        persona_outputs.append(res)
        time.sleep(1.2)
        
    gt = q["ground_truth"]
    err_v1 = q["v1_score"] - gt
    err_v2_0 = q["v2_0_score"] - gt
    err_v2_1 = q_weighted_sum - gt
    
    total_err_v1 += abs(err_v1)
    total_err_v2_0 += abs(err_v2_0)
    total_err_v2_1 += abs(err_v2_1)
    
    print("-" * 80)
    print(f"  🎯 Post-Stratified Market Adoption (V2.1): {q_weighted_sum:.1f}%")
    print(f"  📊 Empirical Ground Truth:                 {gt:.1f}%")
    print(f"  📐 V2.1 Prediction Error (Δ):              {err_v2_1:+.1f}% (vs V1: {err_v1:+.1f}%, vs V2.0: {err_v2_0:+.1f}%)")
    
    all_results.append({
        "id": q["id"],
        "title": q["title"],
        "ground_truth": gt,
        "v1_score": q["v1_score"],
        "v1_error": round(err_v1, 1),
        "v2_0_score": q["v2_0_score"],
        "v2_0_error": round(err_v2_0, 1),
        "v2_1_score": round(q_weighted_sum, 1),
        "v2_1_error": round(err_v2_1, 1),
        "persona_breakdown": persona_outputs
    })

n = len(QUESTIONS)
mae_v1 = total_err_v1 / n
mae_v2_0 = total_err_v2_0 / n
mae_v2_1 = total_err_v2_1 / n

print("\n" + "=" * 90)
print(" 🏁 FINAL 5-QUESTION BENCHMARK COMPARISON: V1 vs V2.0 vs V2.1")
print("=" * 90)
print(f"{'Question':<30} | {'GT':<6} | {'V1 (Δ)':<14} | {'V2.0 (Δ)':<14} | {'V2.1 (Δ)':<14}")
print("-" * 90)
for r in all_results:
    v1_str = f"{r['v1_score']:.1f}% ({r['v1_error']:+.1f}%)"
    v2_0_str = f"{r['v2_0_score']:.1f}% ({r['v2_0_error']:+.1f}%)"
    v2_1_str = f"{r['v2_1_score']:.1f}% ({r['v2_1_error']:+.1f}%)"
    print(f"{r['id'] + ': ' + r['title'][:25]:<30} | {r['ground_truth']:>4.1f}% | {v1_str:>14} | {v2_0_str:>14} | {v2_1_str:>14}")

print("-" * 90)
print(f"🎯 V1 Baseline MAE:                 {mae_v1:.1f}% (Accuracy: {100-mae_v1:.1f}%)")
print(f"⚠️ V2.0 (Double-Penalty) MAE:       {mae_v2_0:.1f}% (Accuracy: {100-mae_v2_0:.1f}%)")
print(f"🚀 V2.1 (Calibrated Train 2009) MAE: {mae_v2_1:.1f}% (Accuracy: {100-mae_v2_1:.1f}%)")
print("=" * 90)

output_file = os.path.join(PROJECT_ROOT, "india_v2_1_benchmark_results.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)
print(f"\n✅ Complete V2.1 benchmark results saved to: {output_file}")
