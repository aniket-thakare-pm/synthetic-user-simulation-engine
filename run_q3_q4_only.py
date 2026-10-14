import sys
import os
import time
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')

from interview_engine import interview_persona_stateless, load_env_key
from indian_sample_personas import INDIAN_SAMPLE_PERSONAS

GEMINI_KEY = os.environ.get("GEMINI_API_KEY") or load_env_key()

questions = [
    {
        "id": "Q3",
        "title": "Electric 2-Wheeler (EV Scooter) Adoption Intent",
        "text": "When buying a new two-wheeler for daily commuting, would you switch to an Electric Scooter (Ola/Ather/TVS EV) over a petrol scooter to save on monthly fuel costs?",
        "ground_truth": 54.0
    },
    {
        "id": "Q4",
        "title": "Online Direct Insurance Purchase (PolicyBazaar)",
        "text": "Would you buy a health or term life insurance policy directly through an online app (like PolicyBazaar) without consulting an offline insurance agent?",
        "ground_truth": 38.0
    }
]

print("=" * 80)
print(" ⚡ RUNNING BENCHMARK QUESTIONS 3 & 4 VIA DIRECT GEMINI API")
print("=" * 80)

results = []
for q in questions:
    print(f"\n📋 QUESTION {q['id']}: {q['title']}")
    print(f"   Ground Truth: {q['ground_truth']}%")
    print("-" * 75)
    
    q_weighted_sum = 0.0
    for p in INDIAN_SAMPLE_PERSONAS:
        t0 = time.time()
        resp = interview_persona_stateless(p, q["text"], api_key=GEMINI_KEY)
        elapsed = time.time() - t0
        
        # Determine adoption vs rejection stance cleanly
        if resp.churn_or_rejection_percent is not None:
            adoption_val = 100 - resp.churn_or_rejection_percent
        elif any(k in action for k in ["ADOPT", "ACCEPT", "BUY", "YES", "PROCEED"]) and not any(k in action for k in ["STATUS_QUO", "REJECT", "CANCEL"]):
            adoption_val = resp.majority_percent
        else:
            adoption_val = 100 - resp.majority_percent
            
        w_contrib = adoption_val * p.population_weight
        q_weighted_sum += w_contrib
        
        print(f"  • [{p.name}] Weight: {p.population_weight*100:.0f}% -> Stance: {action} ({resp.majority_percent}%), Adoption: {adoption_val}% ({elapsed:.1f}s)")
        print(f"    Reasoning: \"{resp.response_text[:110]}...\"")
        time.sleep(2.0)
        
    delta = q_weighted_sum - q['ground_truth']
    print("-" * 75)
    print(f"  🎯 Post-Stratified Weighted Adoption Score (Wi): {q_weighted_sum:.1f}%")
    print(f"  📊 Empirical Ground Truth:                      {q['ground_truth']:.1f}%")
    print(f"  📐 Prediction Error (Δ):                        {delta:+.1f}%")
    print("=" * 80)

