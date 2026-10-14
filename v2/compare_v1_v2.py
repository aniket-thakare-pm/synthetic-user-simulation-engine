"""
V1 vs V2 Engine Comparison Runner
Runs a benchmark question through both V1 (Prompt-based McFadden) and V2 (Python Sigmoid + Multi-Pillar Psychometrics)
and prints a side-by-side comparative analysis.
"""
import sys
import os
import time

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
sys.stdout.reconfigure(encoding='utf-8')

from interview_engine import interview_persona_stateless, load_env_key
from indian_sample_personas import INDIAN_SAMPLE_PERSONAS

from v2.interview_engine_v2 import interview_persona_v2
from v2.indian_personas_v2 import INDIAN_PERSONAS_V2

def run_comparison(question_text: str, ground_truth: float = None, question_title: str = "Test Question"):
    print("=" * 90)
    print(f" 🚀 ENGINE COMPARISON: V1 (BASELINE) vs V2 (PYTHON SIGMOID + MULTI-PILLAR)")
    print(f" 📋 Question: {question_title}")
    print(f" 💬 Prompt: \"{question_text}\"")
    if ground_truth is not None:
        print(f" 📊 Empirical Ground Truth: {ground_truth:.1f}%")
    print("=" * 90)

    # --- RUN V1 ---
    print("\n[1/2] Running Engine V1 (Prompt-based McFadden Split)...")
    v1_scores = {}
    v1_weighted = 0.0
    for p in INDIAN_SAMPLE_PERSONAS:
        resp = interview_persona_stateless(p, question_text)
        if resp.churn_or_rejection_percent is not None:
            adopt_pct = 100 - resp.churn_or_rejection_percent
        elif any(k in resp.primary_action_direction for k in ["ADOPT", "ACCEPT", "BUY", "YES", "PROCEED"]) and not any(k in resp.primary_action_direction for k in ["STATUS_QUO", "REJECT", "CANCEL"]):
            adopt_pct = resp.majority_percent
        else:
            adopt_pct = 100 - resp.majority_percent
            
        v1_scores[p.name] = {
            "adopt": adopt_pct,
            "weight": p.population_weight,
            "stance": resp.primary_action_direction,
            "text": resp.response_text[:90]
        }
        v1_weighted += adopt_pct * p.population_weight
        time.sleep(1.0)

    # --- RUN V2 ---
    print("\n[2/2] Running Engine V2 (Decision Primitives + Python Sigmoid Math)...")
    v2_scores = {}
    v2_weighted = 0.0
    for p in INDIAN_PERSONAS_V2:
        resp = interview_persona_v2(p, question_text)
        adopt_pct = resp.adoption_probability_percent
        v2_scores[p.name] = {
            "adopt": adopt_pct,
            "weight": p.population_weight,
            "stance": resp.primary_action_direction,
            "v_new": resp.v_new_utility,
            "v_sq": resp.v_status_quo_utility,
            "friction": resp.switching_friction_score,
            "delta_v": resp.delta_v_calculated,
            "text": resp.response_text[:90]
        }
        v2_weighted += adopt_pct * p.population_weight
        time.sleep(1.0)

    # --- DISPLAY COMPARISON TABLE ---
    print("\n" + "=" * 90)
    print(" 📊 SIDE-BY-SIDE HEAD-TO-HEAD RESULTS")
    print("=" * 90)
    print(f"{'Persona':<18} | {'Weight':<6} | {'V1 Adoption':<12} | {'V2 Adoption':<12} | {'V2 (V_new vs V_sq)':<18} | {'V2 Delta V'}")
    print("-" * 90)
    for p in INDIAN_SAMPLE_PERSONAS:
        s1 = v1_scores[p.name]
        s2 = v2_scores[p.name]
        v_comp = f"{s2['v_new']:.1f} vs {s2['v_sq']:.1f}"
        print(f"{p.name:<18} | {p.population_weight*100:>5.0f}% | {s1['adopt']:>10.1f}% | {s2['adopt']:>10.1f}% | {v_comp:<18} | {s2['delta_v']:>+6.2f}")

    print("-" * 90)
    print(f"🎯 Post-Stratified Market Adoption (V1): {v1_weighted:.1f}%")
    print(f"⚡ Post-Stratified Market Adoption (V2): {v2_weighted:.1f}%")
    if ground_truth is not None:
        print(f"📈 Empirical Ground Truth:              {ground_truth:.1f}%")
        print(f"📐 Prediction Error (V1):                {v1_weighted - ground_truth:+.1f}%")
        print(f"📐 Prediction Error (V2):                {v2_weighted - ground_truth:+.1f}%")
    print("=" * 90)

if __name__ == "__main__":
    test_q = {
        "title": "Online Telemedicine Video Consultations (Q2)",
        "text": "Would you consult a certified doctor over a scheduled video call on a smartphone app instead of physically visiting a local neighborhood clinic for common health issues?",
        "ground_truth": 44.0
    }
    run_comparison(test_q["text"], ground_truth=test_q["ground_truth"], question_title=test_q["title"])
