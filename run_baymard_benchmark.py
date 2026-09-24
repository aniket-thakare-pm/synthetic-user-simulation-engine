import sys
import os
import time
import json
from dataclasses import asdict

sys.path.insert(0, r"c:\Users\aatha\Desktop\PM\synthetic_user_engine")
sys.stdout.reconfigure(encoding='utf-8')

from interview_engine import interview_persona_stateless, load_env_key
from sample_personas import SAMPLE_PERSONAS

def run_benchmark():
    print("=" * 80)
    print(" 🛒 E-COMMERCE CHECKOUT UX BENCHMARK STUDY (BAYMARD INSTITUTE, N = 4,384)")
    print("=" * 80)

    api_key = load_env_key()
    if not api_key:
        print("❌ Error: OPENROUTER_API_KEY not found in .env or environment.")
        return

    # 5 Baymard Benchmark Questions with Empirical Ground Truths
    questions = [
        {
            "id": "Q1",
            "title": "Unexpected Extra Costs (Shipping/Taxes/Fees)",
            "text": "When shopping online, would you abandon your shopping cart if extra costs like shipping, taxes, or fees are too high or disclosed only at checkout?",
            "ground_truth": 48.0,
            "baymard_cohort_weights": [0.35, 0.30, 0.20, 0.10, 0.05]
        },
        {
            "id": "Q2",
            "title": "Mandatory Account Creation",
            "text": "When shopping online, would you abandon your order if the store forces you to create an account before completing checkout?",
            "ground_truth": 25.0,
            "baymard_cohort_weights": [0.25, 0.25, 0.25, 0.15, 0.10]
        },
        {
            "id": "Q3",
            "title": "Slow / Unclear Delivery Speeds",
            "text": "When shopping online, would you abandon your order if estimated delivery speed is too slow or delivery time is not clearly displayed before payment?",
            "ground_truth": 23.0,
            "baymard_cohort_weights": [0.20, 0.25, 0.30, 0.15, 0.10]
        },
        {
            "id": "Q4",
            "title": "Customer Reviews & Star Ratings Reliance",
            "text": "When considering a purchase on an e-commerce platform, do you actively check customer reviews and star ratings before deciding to buy?",
            "ground_truth": 75.0,  # High reliance percentage among US online shoppers
            "baymard_cohort_weights": [0.25, 0.25, 0.20, 0.15, 0.15]
        },
        {
            "id": "Q5",
            "title": "Strict / Friction Return Policy",
            "text": "When shopping online, would you abandon your order if the return policy is strict, short (e.g. under 14 days), or requires you to pay return shipping?",
            "ground_truth": 18.0,
            "baymard_cohort_weights": [0.25, 0.25, 0.20, 0.15, 0.15]
        }
    ]

    print(f"\nMECE Persona Panel Size: N = {len(SAMPLE_PERSONAS)}")
    for p in SAMPLE_PERSONAS:
        print(f"  • {p.name:<18} | Role: {p.demographics.occupation:<35} | Population Weight: {p.population_weight*100:.0f}%")

    all_benchmark_results = []
    total_abs_error = 0.0

    for q_idx, q in enumerate(questions, 1):
        print("\n" + "=" * 80)
        print(f" 📋 QUESTION {q_idx}/5: {q['title']}")
        print(f"    Text: \"{q['text']}\"")
        print(f"    Baymard Ground Truth Benchmark: {q['ground_truth']:.1f}%")
        print("=" * 80)

        q_responses = []
        gen_weighted_sum = 0.0
        baymard_weighted_sum = 0.0

        for p_idx, persona in enumerate(SAMPLE_PERSONAS):
            print(f"   [Interviewing {p_idx+1}/5] {persona.name} ({persona.demographics.occupation})...", end="", flush=True)
            
            t0 = time.time()
            try:
                resp = interview_persona_stateless(persona, q["text"], api_key=api_key)
                elapsed = time.time() - t0
                
                churn_val = resp.churn_or_rejection_percent
                if q["id"] == "Q4":
                    # Q4 is adoption/reliance, so positive action (KEEP/ACCEPT) indicates review checking
                    if any(k in resp.primary_action_direction for k in ["KEEP", "ACCEPT", "ADOPT", "RETAIN", "CHECK"]):
                        val = resp.majority_percent
                    else:
                        val = 100 - resp.majority_percent
                else:
                    val = churn_val

                gen_weight = persona.population_weight
                baymard_weight = q["baymard_cohort_weights"][p_idx]

                gen_weighted_sum += val * gen_weight
                baymard_weighted_sum += val * baymard_weight

                q_responses.append({
                    "persona_name": persona.name,
                    "role": persona.demographics.occupation,
                    "action": resp.primary_action_direction,
                    "value": val,
                    "gen_weight": gen_weight,
                    "baymard_weight": baymard_weight,
                    "reasoning": resp.response_text,
                    "latency": elapsed
                })
                print(f" Done ({elapsed:.1f}s) -> Stance: {resp.primary_action_direction}, Impact: {val}%")
            except Exception as e:
                print(f" ❌ ERROR: {e}")
                time.sleep(1)

        error_gen = abs(gen_weighted_sum - q["ground_truth"])
        error_baymard = abs(baymard_weighted_sum - q["ground_truth"])
        total_abs_error += error_gen

        result_summary = {
            "question_id": q["id"],
            "title": q["title"],
            "ground_truth": q["ground_truth"],
            "gen_weighted_score": round(gen_weighted_sum, 1),
            "baymard_weighted_score": round(baymard_weighted_sum, 1),
            "abs_error_gen": round(error_gen, 1),
            "abs_error_baymard": round(error_baymard, 1),
            "persona_breakdown": q_responses
        }
        all_benchmark_results.append(result_summary)

        print("-" * 80)
        print(f" 📊 RESULTS FOR {q['id']} ({q['title']}):")
        print(f"    • Empirical Baymard Ground Truth:  {q['ground_truth']:.1f}%")
        print(f"    • General Weighted Score (W_gen): {gen_weighted_sum:.1f}% (Δ = {gen_weighted_sum - q['ground_truth']:+.1f}%)")
        print(f"    • Baymard Cohort Score (W_cohort):{baymard_weighted_sum:.1f}% (Δ = {baymard_weighted_sum - q['ground_truth']:+.1f}%)")
        print("-" * 80)

    mae = total_abs_error / len(questions)

    print("\n" + "=" * 80)
    print(" 🏁 FINAL E-COMMERCE CHECKOUT UX BENCHMARK SUMMARY")
    print("=" * 80)
    print(f"{'QID':<5} | {'Topic':<35} | {'Ground Truth':<12} | {'Simulated (W_gen)':<18} | {'Error (Δ)':<10}")
    print("-" * 85)
    for res in all_benchmark_results:
        delta_str = f"{res['gen_weighted_score'] - res['ground_truth']:+.1f}%"
        print(f"{res['question_id']:<5} | {res['title']:<35} | {res['ground_truth']:>10.1f}% | {res['gen_weighted_score']:>16.1f}% | {delta_str:>9}")
    print("-" * 85)
    print(f"🎯 MEAN ABSOLUTE ERROR (MAE): {mae:.2f}% across all 5 benchmark questions")
    print("=" * 80)

    # Save benchmark results to JSON file
    out_file = r"c:\Users\aatha\Desktop\PM\synthetic_user_engine\baymard_benchmark_results.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(all_benchmark_results, f, indent=2)
    print(f"\n💾 Full benchmark results saved to '{out_file}'")

if __name__ == "__main__":
    run_benchmark()
