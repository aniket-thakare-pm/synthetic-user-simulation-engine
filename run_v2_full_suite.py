import sys
import os
import time
import json

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
sys.stdout.reconfigure(encoding='utf-8')

from v2.interview_engine_v2 import interview_persona_v2
from v2.indian_personas_v2 import INDIAN_PERSONAS_V2
from interview_engine import load_env_key

GEMINI_KEY = os.environ.get("GEMINI_API_KEY") or load_env_key()

QUESTIONS = [
    {
        "id": "Q1",
        "title": "Buy-Now-Pay-Later (BNPL) & 0% No-Cost EMI Adoption",
        "text": "When buying consumer electronics or lifestyle goods online (₹3,000 to ₹25,000), do you use or intend to use Buy-Now-Pay-Later (BNPL) or 0% No-Cost EMI checkout options instead of paying the full amount upfront via debit card or UPI?",
        "ground_truth": 62.0,
        "v1_score": 53.5
    },
    {
        "id": "Q2",
        "title": "Online Telemedicine Doctor Consultation Trust",
        "text": "Would you consult a certified doctor over a scheduled video call on a smartphone app instead of physically visiting a local neighborhood clinic for common health issues?",
        "ground_truth": 44.0,
        "v1_score": 84.5
    },
    {
        "id": "Q3",
        "title": "Electric 2-Wheeler (EV Scooter) Adoption Intent",
        "text": "When buying a new two-wheeler for daily commuting, would you switch to an Electric Scooter (Ola/Ather/TVS EV) over a petrol scooter to save on monthly fuel costs?",
        "ground_truth": 54.0,
        "v1_score": 48.5
    },
    {
        "id": "Q4",
        "title": "Online Direct Insurance Purchase (PolicyBazaar)",
        "text": "Would you buy a health or term life insurance policy directly through an online app (like PolicyBazaar) without consulting an offline insurance agent?",
        "ground_truth": 38.0,
        "v1_score": 34.8
    },
    {
        "id": "Q5",
        "title": "Digital Mutual Fund / SIP Investment via Apps",
        "text": "Do you use or intend to use smartphone investment apps (Groww, Zerodha, Paytm Money) to invest in Mutual Funds via monthly SIPs instead of visiting a physical bank or traditional broker?",
        "ground_truth": 47.0,
        "v1_score": 39.5
    }
]

print("=" * 85)
print(" ⚡ RUNNING COMPLETE V2 BENCHMARK SUITE (5 QUESTIONS × 5 PERSONAS)")
print(" 🔬 Framework: Reference-Dependent Choice + Python Sigmoid Resolution")
print("=" * 85)

all_results = []
total_v1_err = 0.0
total_v2_err = 0.0

for q_idx, q in enumerate(QUESTIONS, 1):
    print(f"\n📋 [{q_idx}/5] {q['id']}: {q['title']}")
    print(f"   Empirical Ground Truth: {q['ground_truth']:.1f}% | V1 Baseline: {q['v1_score']:.1f}% (Δ = {q['v1_score'] - q['ground_truth']:+.1f}%)")
    print("-" * 80)
    
    q_weighted_sum = 0.0
    persona_details = []
    
    for p in INDIAN_PERSONAS_V2:
        t0 = time.time()
        resp = interview_persona_v2(p, q["text"], api_key=GEMINI_KEY)
        elapsed = time.time() - t0
        
        adopt_val = resp.adoption_probability_percent
        w_contrib = adopt_val * p.population_weight
        q_weighted_sum += w_contrib
        
        persona_details.append({
            "name": p.name,
            "role": p.demographics.occupation,
            "weight": p.population_weight,
            "stance": resp.primary_action_direction,
            "v_new": resp.v_new_utility,
            "v_sq": resp.v_status_quo_utility,
            "friction": resp.switching_friction_score,
            "delta_v": resp.delta_v_calculated,
            "adoption": adopt_val,
            "reasoning": resp.response_text
        })
        
        v_str = f"V_new:{resp.v_new_utility:.1f} vs V_sq:{resp.v_status_quo_utility:.1f}"
        print(f"  • [{p.name}] W:{p.population_weight*100:.0f}% -> {resp.primary_action_direction} | {v_str} | ΔV:{resp.delta_v_calculated:>+5.2f} => Adopt: {adopt_val:>5.1f}% ({elapsed:.1f}s)")
        print(f"    Reasoning: \"{resp.response_text[:100]}...\"")
        time.sleep(1.2)
        
    v2_error = q_weighted_sum - q['ground_truth']
    v1_error = q['v1_score'] - q['ground_truth']
    total_v2_err += abs(v2_error)
    total_v1_err += abs(v1_error)
    
    print("-" * 80)
    print(f"  🎯 Post-Stratified Market Adoption (V2): {q_weighted_sum:.1f}%")
    print(f"  📊 Empirical Ground Truth:              {q['ground_truth']:.1f}%")
    print(f"  📐 V2 Prediction Error (Δ):             {v2_error:+.1f}% (vs V1 Error: {v1_error:+.1f}%)")
    
    all_results.append({
        "question_id": q["id"],
        "title": q["title"],
        "ground_truth": q["ground_truth"],
        "v1_score": q["v1_score"],
        "v1_error": round(v1_error, 1),
        "v2_score": round(q_weighted_sum, 1),
        "v2_error": round(v2_error, 1),
        "persona_breakdown": persona_details
    })

mae_v1 = total_v1_err / len(QUESTIONS)
mae_v2 = total_v2_err / len(QUESTIONS)

print("\n" + "=" * 85)
print(" 🏁 FINAL 5-QUESTION BENCHMARK ACCURACY SUMMARY: V1 vs V2")
print("=" * 85)
print(f"{'Question':<30} | {'Ground Truth':<12} | {'V1 Score (Δ)':<16} | {'V2 Score (Δ)':<16}")
print("-" * 85)
for res in all_results:
    v1_str = f"{res['v1_score']:.1f}% ({res['v1_error']:+.1f}%)"
    v2_str = f"{res['v2_score']:.1f}% ({res['v2_error']:+.1f}%)"
    print(f"{res['question_id'] + ': ' + res['title'][:25]:<30} | {res['ground_truth']:>10.1f}% | {v1_str:>16} | {v2_str:>16}")

print("-" * 85)
print(f"🎯 Mean Absolute Error (MAE) - V1 Baseline: {mae_v1:.1f}% (Accuracy: {100-mae_v1:.1f}%)")
print(f"⚡ Mean Absolute Error (MAE) - V2 Engine:   {mae_v2:.1f}% (Accuracy: {100-mae_v2:.1f}%)")
print("=" * 85)

# Save results
output_path = os.path.join(PROJECT_ROOT, "india_v2_benchmark_results.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)
print(f"\n✅ Complete V2 benchmark results saved to: {output_path}")
