import sys
import os
import time
import json

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
sys.stdout.reconfigure(encoding='utf-8')

from v3.engine_v3 import interview_persona_v3
from v3.indian_personas_v3 import INDIAN_PERSONAS_V3
from interview_engine import load_env_key

GEMINI_KEY = os.environ.get("GEMINI_API_KEY") or load_env_key()

QUESTIONS = [
    {
        "id": "Q1",
        "title": "Buy-Now-Pay-Later (BNPL) & 0% No-Cost EMI Adoption",
        "category": "FINTECH_CREDIT_AND_LENDING",
        "text": "When buying consumer electronics or lifestyle goods online (₹3,000 to ₹25,000), do you use or intend to use Buy-Now-Pay-Later (BNPL) or 0% No-Cost EMI checkout options instead of paying the full amount upfront via debit card or UPI?",
        "ground_truth": 62.0,
        "v1_score": 53.5,
        "v2_1_score": 25.3,
        "v2_3_score": 27.6
    },
    {
        "id": "Q2",
        "title": "Online Telemedicine Video Consultations Trust",
        "category": "HEALTH_AND_DIAGNOSTICS",
        "text": "Would you consult a certified doctor over a scheduled video call on a smartphone app instead of physically visiting a local neighborhood clinic for common health issues?",
        "ground_truth": 44.0,
        "v1_score": 84.5,
        "v2_1_score": 40.4,
        "v2_3_score": 39.1
    },
    {
        "id": "Q3",
        "title": "Electric 2-Wheeler (EV Scooter) Adoption Intent",
        "category": "MOBILITY_AND_DURABLES",
        "text": "When buying a new two-wheeler for daily commuting, would you switch to an Electric Scooter (Ola/Ather/TVS EV) over a petrol scooter to save on monthly fuel costs?",
        "ground_truth": 54.0,
        "v1_score": 48.5,
        "v2_1_score": 42.3,
        "v2_3_score": 46.9
    },
    {
        "id": "Q4",
        "title": "Online Direct Insurance Purchase (PolicyBazaar)",
        "category": "INSURANCE_AND_PROTECTION",
        "text": "Would you buy a health or term life insurance policy directly through an online app (like PolicyBazaar) without consulting an offline insurance agent?",
        "ground_truth": 38.0,
        "v1_score": 34.8,
        "v2_1_score": 33.0,
        "v2_3_score": 43.8
    },
    {
        "id": "Q5",
        "title": "Digital Mutual Fund / SIP Investment via Apps",
        "category": "WEALTH_AND_INVESTMENTS",
        "text": "Do you use or intend to use smartphone investment apps (Groww, Zerodha, Paytm Money) to invest in Mutual Funds via monthly SIPs instead of visiting a physical bank or traditional broker?",
        "ground_truth": 47.0,
        "v1_score": 39.5,
        "v2_1_score": 54.0,
        "v2_3_score": 58.4
    }
]

print("=" * 100)
print(" 🚀 RUNNING FULL 5-QUESTION BENCHMARK SUITE ON ENGINE V3")
print(" 🔬 Framework: Category-Aware Mental Accounting Choice Architecture (Thaler-Train Model)")
print(" 👥 Panel: 5 MECE Indian Personas (BCG-FICCI & PwC Empirical Benchmark N=2,500)")
print("=" * 100)

all_results = []
total_err_v1 = 0.0
total_err_v2_1 = 0.0
total_err_v2_3 = 0.0
total_err_v3 = 0.0

for q_idx, q in enumerate(QUESTIONS, 1):
    print(f"\n📋 [{q_idx}/5] {q['id']}: {q['title']}")
    print(f"   Category: {q['category']}")
    print(f"   Ground Truth: {q['ground_truth']:.1f}% | V1: {q['v1_score']:.1f}% | V2.1: {q['v2_1_score']:.1f}% | V2.3: {q['v2_3_score']:.1f}%")
    print("-" * 95)
    
    q_weighted_sum = 0.0
    persona_outputs = []
    
    for p in INDIAN_PERSONAS_V3:
        t0 = time.time()
        res = interview_persona_v3(p, q["text"], category=q["category"], api_key=GEMINI_KEY)
        elapsed = time.time() - t0
        
        score = res["target_metric_score"]
        w_contrib = score * p.population_weight
        q_weighted_sum += w_contrib
        
        v_str = f"V_new:{res['v_obj_new']:.1f} vs V_sq:{res['v_obj_sq']:.1f} | F_eff:{res['effective_friction']:>4.2f} | FricPen:{res['friction_penalty']:>4.2f} (ΔV:{res['delta_v']:>+5.2f})"
        print(f"  • [{p.name}] W:{p.population_weight*100:>2.0f}% -> {res['decision_stance']:<3} | {v_str} => Adoption: {score:>5.1f}% ({elapsed:.1f}s)")
        print(f"    Reasoning: \"{res['response_text'][:95]}...\"")
        persona_outputs.append(res)
        time.sleep(1.2)
        
    gt = q["ground_truth"]
    err_v1 = q["v1_score"] - gt
    err_v2_1 = q["v2_1_score"] - gt
    err_v2_3 = q["v2_3_score"] - gt
    err_v3 = q_weighted_sum - gt
    
    total_err_v1 += abs(err_v1)
    total_err_v2_1 += abs(err_v2_1)
    total_err_v2_3 += abs(err_v2_3)
    total_err_v3 += abs(err_v3)
    
    print("-" * 95)
    print(f"  🎯 Post-Stratified Market Adoption (V3):   {q_weighted_sum:.1f}%")
    print(f"  📊 Empirical Ground Truth:                 {gt:.1f}%")
    print(f"  📐 V3 Prediction Error (Δ):                {err_v3:+.1f}% (vs V2.3: {err_v2_3:+.1f}%, vs V1: {err_v1:+.1f}%)")
    
    all_results.append({
        "id": q["id"],
        "title": q["title"],
        "category": q["category"],
        "ground_truth": gt,
        "v1_score": q["v1_score"],
        "v1_error": round(err_v1, 1),
        "v2_1_score": q["v2_1_score"],
        "v2_1_error": round(err_v2_1, 1),
        "v2_3_score": q["v2_3_score"],
        "v2_3_error": round(err_v2_3, 1),
        "v3_score": round(q_weighted_sum, 1),
        "v3_error": round(err_v3, 1),
        "persona_breakdown": persona_outputs
    })

n = len(QUESTIONS)
mae_v1 = total_err_v1 / n
mae_v2_1 = total_err_v2_1 / n
mae_v2_3 = total_err_v2_3 / n
mae_v3 = total_err_v3 / n

print("\n" + "=" * 100)
print(" 🏁 FINAL 5-QUESTION BENCHMARK COMPARISON: V1 vs V2.1 vs V2.3 vs V3")
print("=" * 100)
print(f"{'Question':<26} | {'GT':<5} | {'V1 (Δ)':<12} | {'V2.1 (Δ)':<12} | {'V2.3 (Δ)':<12} | {'V3 (Δ)':<12}")
print("-" * 100)
for r in all_results:
    v1_str = f"{r['v1_score']:.1f}% ({r['v1_error']:+.1f}%)"
    v2_1_str = f"{r['v2_1_score']:.1f}% ({r['v2_1_error']:+.1f}%)"
    v2_3_str = f"{r['v2_3_score']:.1f}% ({r['v2_3_error']:+.1f}%)"
    v3_str = f"{r['v3_score']:.1f}% ({r['v3_error']:+.1f}%)"
    print(f"{r['id'] + ': ' + r['title'][:21]:<26} | {r['ground_truth']:>4.1f}% | {v1_str:>12} | {v2_1_str:>12} | {v2_3_str:>12} | {v3_str:>12}")

print("-" * 100)
print(f"🎯 V1 Baseline MAE:                         {mae_v1:.1f}% (Accuracy: {100-mae_v1:.1f}%)")
print(f"📈 V2.1 (Train 2009 Subtraction) MAE:       {mae_v2_1:.1f}% (Accuracy: {100-mae_v2_1:.1f}%)")
print(f"🚀 V2.3 (Salience RMS Choice) MAE:          {mae_v2_3:.1f}% (Accuracy: {100-mae_v2_3:.1f}%)")
print(f"🏆 V3 (Category Mental Accounting) MAE:     {mae_v3:.1f}% (Accuracy: {100-mae_v3:.1f}%)")
print("=" * 100)

output_file = os.path.join(PROJECT_ROOT, "india_v3_benchmark_results.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)
print(f"\n✅ Complete V3 benchmark results saved to: {output_file}")
