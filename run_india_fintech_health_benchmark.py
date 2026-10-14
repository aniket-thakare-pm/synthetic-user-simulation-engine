import sys
import os
import time
import json
from dataclasses import asdict

sys.path.insert(0, r"c:\Users\aatha\Desktop\PM\synthetic_user_engine")
sys.stdout.reconfigure(encoding='utf-8')

from interview_engine import interview_persona_stateless, load_env_key
from indian_sample_personas import INDIAN_SAMPLE_PERSONAS

def run_india_benchmark():
    print("=" * 85)
    print(" 🇮🇳 INDIA CONSUMER FINTECH, HEALTHTECH & MOBILITY BENCHMARK STUDY")
    print("    (Grounded in BCG-FICCI & PwC India Consumer Financial Behavior Survey, N = 2,500)")
    print("=" * 85)

    api_key = load_env_key()
    if not api_key:
        print("❌ Error: OPENROUTER_API_KEY not found in .env or environment.")
        return

    # 5 Empirical Indian Consumer Questions across Credit, Healthtech, Mobility, Insurtech, Wealthtech
    questions = [
        {
            "id": "Q1",
            "title": "Buy-Now-Pay-Later (BNPL) & 0% No-Cost EMI Adoption",
            "text": "When buying electronics or home appliances online above ₹10,000, would you use Buy-Now-Pay-Later (BNPL) or 0% No-Cost EMI to spread out payments rather than paying 100% upfront?",
            "ground_truth": 62.0,
            "cohort_weights": [0.35, 0.25, 0.20, 0.10, 0.10]
        },
        {
            "id": "Q2",
            "title": "Online Telemedicine Doctor Consultation Trust",
            "text": "Would you use a smartphone app for a virtual video consultation with a doctor for minor health issues (fever, skin rash, cold) instead of traveling to a local clinic?",
            "ground_truth": 44.0,
            "cohort_weights": [0.35, 0.25, 0.20, 0.10, 0.10]
        },
        {
            "id": "Q3",
            "title": "Electric 2-Wheeler (EV Scooter) Adoption Intent",
            "text": "When buying a new two-wheeler for daily commuting, would you switch to an Electric Scooter (Ola/Ather/TVS EV) over a petrol scooter to save on monthly fuel costs?",
            "ground_truth": 54.0,
            "cohort_weights": [0.35, 0.25, 0.20, 0.10, 0.10]
        },
        {
            "id": "Q4",
            "title": "Online Direct Insurance Purchase (PolicyBazaar)",
            "text": "Would you buy a health or term life insurance policy directly through an online app (like PolicyBazaar) without consulting an offline insurance agent?",
            "ground_truth": 38.0,
            "cohort_weights": [0.35, 0.25, 0.20, 0.10, 0.10]
        },
        {
            "id": "Q5",
            "title": "Digital Mutual Fund / SIP Investment via Apps",
            "text": "Do you use or intend to use smartphone investment apps (Groww, Zerodha, Paytm Money) to invest in Mutual Funds via monthly SIPs?",
            "ground_truth": 47.0,
            "cohort_weights": [0.35, 0.25, 0.20, 0.10, 0.10]
        }
    ]

    print(f"\nStratified Indian MECE Persona Panel Size: N = {len(INDIAN_SAMPLE_PERSONAS)}")
    for p in INDIAN_SAMPLE_PERSONAS:
        print(f"  • {p.name:<18} | Role: {p.demographics.occupation:<40} | Weight: {p.population_weight*100:.0f}%")

    all_benchmark_results = []
    total_abs_error = 0.0

    for q_idx, q in enumerate(questions, 1):
        print("\n" + "=" * 85)
        print(f" 📋 QUESTION {q_idx}/5: {q['title']}")
        print(f"    Text: \"{q['text']}\"")
        print(f"    Empirical Ground Truth (India Study): {q['ground_truth']:.1f}%")
        print("=" * 85)

        q_responses = []
        gen_weighted_sum = 0.0

        for p_idx, persona in enumerate(INDIAN_SAMPLE_PERSONAS):
            print(f"   [Interviewing {p_idx+1}/5] {persona.name} ({persona.demographics.occupation})...", end="", flush=True)
            
            t0 = time.time()
            try:
                gem_key = os.environ.get("GEMINI_API_KEY") or api_key
                resp = interview_persona_stateless(persona, q["text"], api_key=gem_key)
                elapsed = time.time() - t0
                
                # Check adoption stance using normalized churn_or_rejection_percent or explicit enums
                if resp.churn_or_rejection_percent is not None:
                    val = 100 - resp.churn_or_rejection_percent
                elif any(k in resp.primary_action_direction for k in ["ADOPT", "ACCEPT", "BUY", "YES", "PROCEED"]) and not any(k in resp.primary_action_direction for k in ["STATUS_QUO", "REJECT", "CANCEL"]):
                    val = resp.majority_percent
                else:
                    val = 100 - resp.majority_percent

                gen_weight = persona.population_weight
                gen_weighted_sum += val * gen_weight

                q_responses.append({
                    "persona_name": persona.name,
                    "role": persona.demographics.occupation,
                    "action": resp.primary_action_direction,
                    "value": val,
                    "weight": gen_weight,
                    "reasoning": resp.response_text,
                    "latency": elapsed
                })
                print(f" Done ({elapsed:.1f}s) -> Stance: {resp.primary_action_direction}, Adoption Rate: {val}%")
            except Exception as e:
                print(f" ❌ ERROR: {e}")
                time.sleep(1)

        error_gen = abs(gen_weighted_sum - q["ground_truth"])
        total_abs_error += error_gen

        result_summary = {
            "question_id": q["id"],
            "title": q["title"],
            "ground_truth": q["ground_truth"],
            "simulated_score": round(gen_weighted_sum, 1),
            "abs_error": round(error_gen, 1),
            "persona_breakdown": q_responses
        }
        all_benchmark_results.append(result_summary)

        print("-" * 85)
        print(f" 📊 RESULTS FOR {q['id']} ({q['title']}):")
        print(f"    • Empirical India Ground Truth: {q['ground_truth']:.1f}%")
        print(f"    • Simulated Score (W_gen):      {gen_weighted_sum:.1f}% (Δ = {gen_weighted_sum - q['ground_truth']:+.1f}%)")
        print("-" * 85)

    mae = total_abs_error / len(questions)

    print("\n" + "=" * 85)
    print(" 🏁 FINAL INDIAN CONSUMER BENCHMARK STUDY SUMMARY")
    print("=" * 85)
    print(f"{'QID':<5} | {'Topic / Domain':<38} | {'Ground Truth':<12} | {'Simulated Score':<16} | {'Error (Δ)':<10}")
    print("-" * 88)
    for res in all_benchmark_results:
        delta_str = f"{res['simulated_score'] - res['ground_truth']:+.1f}%"
        print(f"{res['question_id']:<5} | {res['title']:<38} | {res['ground_truth']:>10.1f}% | {res['simulated_score']:>14.1f}% | {delta_str:>9}")
    print("-" * 88)
    print(f"🎯 MEAN ABSOLUTE ERROR (MAE): {mae:.2f}% across all 5 benchmark questions")
    print("=" * 85)

    # Save benchmark results to JSON file
    out_file = r"c:\Users\aatha\Desktop\PM\synthetic_user_engine\india_fintech_health_benchmark_results.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(all_benchmark_results, f, indent=2)
    print(f"\n💾 Full benchmark results saved to '{out_file}'")

if __name__ == "__main__":
    run_india_benchmark()
