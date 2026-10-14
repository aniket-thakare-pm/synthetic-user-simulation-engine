import sys
import os
import time
import json

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
sys.stdout.reconfigure(encoding='utf-8')

from v3.engine_v3_1 import interview_persona_v3_1
from v3.indian_personas_v3 import INDIAN_PERSONAS_V3
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
        "v1_score": 53.5
    },
    {
        "id": "Q2",
        "title": "Online Telemedicine Video Consultations Trust",
        "category": "HEALTH_AND_DIAGNOSTICS",
        "text": "Would you consult a certified doctor over a scheduled video call on a smartphone app instead of physically visiting a local neighborhood clinic for common health issues?",
        "action_a": "Consult a certified doctor over scheduled video call on a smartphone app",
        "baseline_b": "Physically visit a local neighborhood clinic for common health issues",
        "ground_truth": 44.0,
        "v1_score": 84.5
    },
    {
        "id": "Q3",
        "title": "Electric 2-Wheeler (EV Scooter) Adoption Intent",
        "category": "MOBILITY_AND_DURABLES",
        "text": "When buying a new two-wheeler for daily commuting, would you switch to an Electric Scooter (Ola/Ather/TVS EV) over a petrol scooter to save on monthly fuel costs?",
        "action_a": "Switch to an Electric Scooter (Ola/Ather/TVS EV) for daily commuting",
        "baseline_b": "Keep or buy a traditional petrol scooter (Honda Activa) for daily commuting",
        "ground_truth": 54.0,
        "v1_score": 48.5
    },
    {
        "id": "Q4",
        "title": "Online Direct Insurance Purchase (PolicyBazaar)",
        "category": "INSURANCE_AND_PROTECTION",
        "text": "Would you buy a health or term life insurance policy directly through an online app (like PolicyBazaar) without consulting an offline insurance agent?",
        "action_a": "Buy health or term life insurance directly through an online app (PolicyBazaar)",
        "baseline_b": "Consult and buy through a traditional offline insurance agent",
        "ground_truth": 38.0,
        "v1_score": 34.8
    },
    {
        "id": "Q5",
        "title": "Digital Mutual Fund / SIP Investment via Apps",
        "category": "WEALTH_AND_INVESTMENTS",
        "text": "Do you use or intend to use smartphone investment apps (Groww, Zerodha, Paytm Money) to invest in Mutual Funds via monthly SIPs instead of visiting a physical bank or traditional broker?",
        "action_a": "Use smartphone investment apps (Groww/Zerodha) to invest in Mutual Funds via monthly SIPs",
        "baseline_b": "Visit a physical bank branch or invest through a traditional offline broker",
        "ground_truth": 47.0,
        "v1_score": 39.5
    }
]

print("=" * 100)
print(" 🚀 RUNNING FULL 5-QUESTION BENCHMARK SUITE ON ENGINE V3.1")
print(" 🔬 Framework: Clean Discrete Choice Architecture (Thaler-Train Model, Explicit Action A vs Baseline B)")
print(" 👥 Panel: 5 MECE Indian Personas (BCG-FICCI & PwC Empirical Benchmark N=2,500)")
print("=" * 100)

all_results = []
total_err_v1 = 0.0
total_err_v3_1 = 0.0

for q_idx, q in enumerate(QUESTIONS, 1):
    print(f"\n📋 [{q_idx}/5] {q['id']}: {q['title']}")
    print(f"   Category: {q['category']}")
    print(f"   Ground Truth: {q['ground_truth']:.1f}% | V1 Baseline: {q['v1_score']:.1f}%")
    print(f"   Action A:   \"{q['action_a']}\"")
    print(f"   Baseline B: \"{q['baseline_b']}\"")
    print("-" * 95)
    
    q_weighted_sum = 0.0
    persona_outputs = []
    
    for p in INDIAN_PERSONAS_V3:
        t0 = time.time()
        res = interview_persona_v3_1(
            p, q["text"],
            action_label=q["action_a"],
            baseline_label=q["baseline_b"],
            category=q["category"],
            api_key=GEMINI_KEY
        )
        elapsed = time.time() - t0
        
        score = res["target_metric_score"]
        w_contrib = score * p.population_weight
        q_weighted_sum += w_contrib
        
        v_str = f"V_A:{res['v_action_a']:.1f} vs V_B:{res['v_baseline_b']:.1f} | F_eff:{res['effective_friction']:>4.2f} (ΔV:{res['delta_v']:>+5.2f})"
        print(f"  • [{p.name}] W:{p.population_weight*100:>2.0f}% -> {res['decision_stance']:<3} | {v_str} => Adoption: {score:>5.1f}% ({elapsed:.1f}s)")
        print(f"    Reasoning: \"{res['response_text'][:95]}...\"")
        persona_outputs.append(res)
        time.sleep(1.2)
        
    gt = q["ground_truth"]
    err_v1 = q["v1_score"] - gt
    err_v3_1 = q_weighted_sum - gt
    
    total_err_v1 += abs(err_v1)
    total_err_v3_1 += abs(err_v3_1)
    
    print("-" * 95)
    print(f"  🎯 Post-Stratified Market Adoption (V3.1): {q_weighted_sum:.1f}%")
    print(f"  📊 Empirical Ground Truth:                 {gt:.1f}%")
    print(f"  📐 V3.1 Prediction Error (Δ):              {err_v3_1:+.1f}% (vs V1 Error: {err_v1:+.1f}%)")
    
    all_results.append({
        "id": q["id"],
        "title": q["title"],
        "category": q["category"],
        "ground_truth": gt,
        "v1_score": q["v1_score"],
        "v1_error": round(err_v1, 1),
        "v3_1_score": round(q_weighted_sum, 1),
        "v3_1_error": round(err_v3_1, 1),
        "persona_breakdown": persona_outputs
    })

n = len(QUESTIONS)
mae_v1 = total_err_v1 / n
mae_v3_1 = total_err_v3_1 / n

print("\n" + "=" * 100)
print(" 🏁 FINAL 5-QUESTION BENCHMARK COMPARISON: V1 vs V3.1")
print("=" * 100)
print(f"{'Question':<30} | {'GT':<6} | {'V1 Score (Δ)':<18} | {'V3.1 Score (Δ)':<18}")
print("-" * 100)
for r in all_results:
    v1_str = f"{r['v1_score']:.1f}% ({r['v1_error']:+.1f}%)"
    v3_1_str = f"{r['v3_1_score']:.1f}% ({r['v3_1_error']:+.1f}%)"
    print(f"{r['id'] + ': ' + r['title'][:25]:<30} | {r['ground_truth']:>4.1f}% | {v1_str:>18} | {v3_1_str:>18}")

print("-" * 100)
print(f"🎯 V1 Baseline MAE: {mae_v1:.1f}% (Accuracy: {100-mae_v1:.1f}%)")
print(f"🏆 V3.1 Engine MAE: {mae_v3_1:.1f}% (Accuracy: {100-mae_v3_1:.1f}%)")
print("=" * 100)

output_file = os.path.join(PROJECT_ROOT, "india_v3_1_benchmark_results.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)
print(f"\n✅ Complete V3.1 India benchmark results saved to: {output_file}")
