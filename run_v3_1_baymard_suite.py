import sys
import os
import time
import json

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
sys.stdout.reconfigure(encoding='utf-8')

from v3.engine_v3_1 import interview_persona_v3_1
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
        "v1_score": 15.0
    },
    {
        "id": "Q2",
        "title": "Mandatory Account Creation Friction",
        "category": "ECOMMERCE_CHECKOUT_AND_RETAIL",
        "text": "When shopping online, would you abandon your order if the store forces you to create an account before completing checkout?",
        "action_a": "Abandon your order and leave empty-handed without buying",
        "baseline_b": "Create the account and complete the purchase to receive the item",
        "ground_truth": 25.0,
        "v1_score": 15.0
    },
    {
        "id": "Q3",
        "title": "Slow / Unclear Delivery Speeds",
        "category": "ECOMMERCE_CHECKOUT_AND_RETAIL",
        "text": "When shopping online, would you abandon your order if estimated delivery speed is too slow or delivery time is not clearly displayed before payment?",
        "action_a": "Abandon your order and look elsewhere / leave without buying",
        "baseline_b": "Accept the slower/unclear shipping and complete checkout to get the item",
        "ground_truth": 23.0,
        "v1_score": 18.5
    },
    {
        "id": "Q4",
        "title": "Customer Reviews & Star Ratings Reliance",
        "category": "ECOMMERCE_CHECKOUT_AND_RETAIL",
        "text": "When considering a purchase on an e-commerce platform, do you actively check customer reviews and star ratings before deciding to buy?",
        "action_a": "Actively check customer reviews and star ratings before buying",
        "baseline_b": "Buy directly based on images/product description without checking reviews",
        "ground_truth": 75.0,
        "v1_score": 80.0
    },
    {
        "id": "Q5",
        "title": "Strict / Friction Return Policy",
        "category": "ECOMMERCE_CHECKOUT_AND_RETAIL",
        "text": "When shopping online, would you abandon your order if the return policy is strict, short (e.g. under 14 days), or requires you to pay return shipping?",
        "action_a": "Abandon your order and do not buy from this store",
        "baseline_b": "Accept the strict return policy risk and complete the purchase",
        "ground_truth": 18.0,
        "v1_score": 15.0
    }
]

print("=" * 95)
print(" 🛒 RUNNING 5-QUESTION BAYMARD INSTITUTE STUDY ON ENGINE V3.1")
print(" 🔬 Framework: Clean Discrete Choice Architecture (Thaler-Train Model, Zero Inversion Hacks)")
print(" 👥 Panel: 5 MECE US General Consumer Personas (Baymard N=4,384 Empirical Ground Truth)")
print("=" * 95)

all_results = []
total_err_v1 = 0.0
total_err_v3_1 = 0.0

for q_idx, q in enumerate(QUESTIONS, 1):
    print(f"\n📋 [{q_idx}/5] {q['id']}: {q['title']}")
    print(f"   Ground Truth: {q['ground_truth']:.1f}% | V1 Baseline: {q['v1_score']:.1f}%")
    print(f"   Action A:   \"{q['action_a']}\"")
    print(f"   Baseline B: \"{q['baseline_b']}\"")
    print("-" * 90)
    
    q_weighted_sum = 0.0
    persona_outputs = []
    
    for p in SAMPLE_PERSONAS_V3:
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
        print(f"  • [{p.name}] W:{p.population_weight*100:>2.0f}% -> {res['decision_stance']:<3} | {v_str} => Score: {score:>5.1f}% ({elapsed:.1f}s)")
        print(f"    Reasoning: \"{res['response_text'][:90]}...\"")
        persona_outputs.append(res)
        time.sleep(1.2)
        
    gt = q["ground_truth"]
    err_v1 = q["v1_score"] - gt
    err_v3_1 = q_weighted_sum - gt
    
    total_err_v1 += abs(err_v1)
    total_err_v3_1 += abs(err_v3_1)
    
    print("-" * 90)
    print(f"  🎯 Post-Stratified Rate (V3.1): {q_weighted_sum:.1f}%")
    print(f"  📊 Empirical Ground Truth:      {gt:.1f}%")
    print(f"  📐 V3.1 Prediction Error (Δ):   {err_v3_1:+.1f}% (vs V1 Error: {err_v1:+.1f}%)")
    
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

print("\n" + "=" * 95)
print(" 🏁 FINAL 5-QUESTION BAYMARD BENCHMARK COMPARISON: V1 vs V3.1")
print("=" * 95)
print(f"{'Question':<38} | {'GT':<6} | {'V1 Score (Δ)':<18} | {'V3.1 Score (Δ)':<18}")
print("-" * 95)
for r in all_results:
    v1_str = f"{r['v1_score']:.1f}% ({r['v1_error']:+.1f}%)"
    v3_1_str = f"{r['v3_1_score']:.1f}% ({r['v3_1_error']:+.1f}%)"
    print(f"{r['id'] + ': ' + r['title'][:32]:<38} | {r['ground_truth']:>4.1f}% | {v1_str:>18} | {v3_1_str:>18}")

print("-" * 95)
print(f"🎯 V1 Baseline MAE: {mae_v1:.1f}% (Accuracy: {100-mae_v1:.1f}%)")
print(f"🏆 V3.1 Engine MAE: {mae_v3_1:.1f}% (Accuracy: {100-mae_v3_1:.1f}%)")
print("=" * 95)

output_file = os.path.join(PROJECT_ROOT, "baymard_5q_v3_1_results.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)
print(f"\n✅ Complete Baymard 5Q V3.1 results saved to: {output_file}")
