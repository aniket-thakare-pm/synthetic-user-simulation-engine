import sys
import os
import time
import json

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
sys.stdout.reconfigure(encoding='utf-8')

from v2.interview_engine_v2 import interview_persona_v2
from v2.sample_personas_v2 import SAMPLE_PERSONAS_V2
from interview_engine import load_env_key

GEMINI_KEY = os.environ.get("GEMINI_API_KEY") or load_env_key()

QUESTIONS = [
    {
        "id": "Q1",
        "name": "Deloitte Q1: $5 Monthly Price Hike Cancellation",
        "text": "Would you cancel your favorite video streaming service if the monthly subscription price increased by $5 per month, and why?",
        "ground_truth": 61.0,
        "v1_score": 61.3
    },
    {
        "id": "Q2",
        "name": "Deloitte Q2: Show Hopping / Serial Churn Behavior",
        "text": "Do you subscribe to a streaming service just to watch a specific movie or show, and then cancel as soon as you finish watching it?",
        "ground_truth": 47.0,
        "v1_score": 48.0
    }
]

print("=" * 85)
print(" 🎬 RUNNING DELOITTE DIGITAL MEDIA TRENDS BENCHMARK ON V2 ENGINE")
print(" 🔬 Framework: Reference-Dependent Choice + Python Sigmoid Resolution")
print("=" * 85)

results = []

for q_idx, q in enumerate(QUESTIONS, 1):
    print(f"\n📋 TEST {q_idx}: {q['name']}")
    print(f"   Question: \"{q['text']}\"")
    print(f"   Empirical Human Benchmark: {q['ground_truth']:.1f}% | V1 Baseline: {q['v1_score']:.1f}%")
    print("-" * 80)
    
    q_weighted_churn = 0.0
    persona_outputs = []
    
    for p in SAMPLE_PERSONAS_V2:
        t0 = time.time()
        resp = interview_persona_v2(p, q["text"], api_key=GEMINI_KEY)
        elapsed = time.time() - t0
        
        # In a cancellation/churn question:
        # If persona says YES to cancel / rejects hike -> Churn = resp.rejection_probability_percent
        # If persona says NO to cancel / accepts hike -> Churn = resp.adoption_probability_percent
        # Let's check their text & direction:
        is_canceling = any(k in resp.response_text.lower() for k in ["cancel", "drop", "unsubscribe", "leave", "quit", "cut"]) and not any(k in resp.response_text.lower() for k in ["keep", "stay", "continue", "absorb", "pay the extra"])
        
        if "RETAIN_STATUS_QUO" in resp.primary_action_direction or is_canceling:
            churn_val = resp.rejection_probability_percent
            action_label = "CANCEL"
        else:
            churn_val = resp.adoption_probability_percent
            action_label = "KEEP"
            
        w_contrib = churn_val * p.population_weight
        q_weighted_churn += w_contrib
        
        v_str = f"V_new:{resp.v_new_utility:.1f} vs V_sq:{resp.v_status_quo_utility:.1f} (ΔV:{resp.delta_v_calculated:>+5.2f})"
        print(f"  • [{p.name}] W:{p.population_weight*100:>2.0f}% -> {action_label} | {v_str} => Churn: {churn_val:>5.1f}% ({elapsed:.1f}s)")
        print(f"    Reasoning: \"{resp.response_text[:95]}...\"")
        time.sleep(1.2)
        
    v2_error = q_weighted_churn - q['ground_truth']
    v1_error = q['v1_score'] - q['ground_truth']
    
    print("-" * 80)
    print(f"  🎯 Post-Stratified Churn Rate (V2): {q_weighted_churn:.1f}%")
    print(f"  📊 Empirical Human Ground Truth:   {q['ground_truth']:.1f}%")
    print(f"  📐 V2 Prediction Error (Δ):        {v2_error:+.1f}% (vs V1 Error: {v1_error:+.1f}%)")
    
    results.append({
        "id": q["id"],
        "name": q["name"],
        "ground_truth": q["ground_truth"],
        "v1_score": q["v1_score"],
        "v1_error": round(v1_error, 1),
        "v2_score": round(q_weighted_churn, 1),
        "v2_error": round(v2_error, 1)
    })

print("\n" + "=" * 85)
print(" 🏁 FINAL DELOITTE BENCHMARK COMPARISON: V1 vs V2")
print("=" * 85)
print(f"{'Test':<35} | {'Ground Truth':<12} | {'V1 Score (Δ)':<16} | {'V2 Score (Δ)':<16}")
print("-" * 85)
for r in results:
    v1_str = f"{r['v1_score']:.1f}% ({r['v1_error']:+.1f}%)"
    v2_str = f"{r['v2_score']:.1f}% ({r['v2_error']:+.1f}%)"
    print(f"{r['name'][:35]:<35} | {r['ground_truth']:>10.1f}% | {v1_str:>16} | {v2_str:>16}")
print("=" * 85)
