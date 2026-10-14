"""
A/B Test Runner: Engine V2.1 (Option A) vs Engine V2.2 (Option B)
Runs any benchmark suite head-to-head and prints a clear comparative scorecard.
"""
import sys
import os
import time
import json

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
sys.stdout.reconfigure(encoding='utf-8')

from v2.engine_v2_1 import interview_persona_v2_1
from v2.engine_v2_2 import interview_persona_v2_2
from v2.sample_personas_v2 import SAMPLE_PERSONAS_V2
from v2.indian_personas_v2 import INDIAN_PERSONAS_V2
from interview_engine import load_env_key

GEMINI_KEY = os.environ.get("GEMINI_API_KEY") or load_env_key()

DELOITTE_QUESTIONS = [
    {
        "id": "Deloitte Q1",
        "title": "$5 Monthly Price Hike Cancellation",
        "text": "Would you cancel your favorite video streaming service if the monthly subscription price increased by $5 per month, and why?",
        "ground_truth": 61.0,
        "v1_score": 61.3,
        "panel": "US"
    },
    {
        "id": "Deloitte Q2",
        "title": "Show Hopping / Serial Churn Behavior",
        "text": "Do you subscribe to a streaming service just to watch a specific movie or show, and then cancel as soon as you finish watching it?",
        "ground_truth": 47.0,
        "v1_score": 48.0,
        "panel": "US"
    }
]

INDIA_QUESTIONS = [
    {
        "id": "India Q1",
        "title": "Buy-Now-Pay-Later (BNPL) Adoption",
        "text": "When buying consumer electronics or lifestyle goods online (₹3,000 to ₹25,000), do you use or intend to use Buy-Now-Pay-Later (BNPL) or 0% No-Cost EMI checkout options instead of paying the full amount upfront via debit card or UPI?",
        "ground_truth": 62.0,
        "v1_score": 53.5,
        "panel": "INDIA"
    },
    {
        "id": "India Q2",
        "title": "Online Telemedicine Video Consultations",
        "text": "Would you consult a certified doctor over a scheduled video call on a smartphone app instead of physically visiting a local neighborhood clinic for common health issues?",
        "ground_truth": 44.0,
        "v1_score": 84.5,
        "panel": "INDIA"
    },
    {
        "id": "India Q3",
        "title": "Electric 2-Wheeler (EV Scooter) Intent",
        "text": "When buying a new two-wheeler for daily commuting, would you switch to an Electric Scooter (Ola/Ather/TVS EV) over a petrol scooter to save on monthly fuel costs?",
        "ground_truth": 54.0,
        "v1_score": 48.5,
        "panel": "INDIA"
    },
    {
        "id": "India Q4",
        "title": "Online Direct Insurance Purchase",
        "text": "Would you buy a health or term life insurance policy directly through an online app (like PolicyBazaar) without consulting an offline insurance agent?",
        "ground_truth": 38.0,
        "v1_score": 34.8,
        "panel": "INDIA"
    },
    {
        "id": "India Q5",
        "title": "Digital Mutual Fund / SIP Apps",
        "text": "Do you use or intend to use smartphone investment apps (Groww, Zerodha, Paytm Money) to invest in Mutual Funds via monthly SIPs instead of visiting a physical bank or traditional broker?",
        "ground_truth": 47.0,
        "v1_score": 39.5,
        "panel": "INDIA"
    }
]

def run_suite(suite_name: str, questions: list):
    print("=" * 90)
    print(f" 🚀 RUNNING A/B TEST: V2.1 (OPTION A) vs V2.2 (OPTION B)")
    print(f" 📚 Suite: {suite_name}")
    print("=" * 90)

    scorecard = []

    for q in questions:
        print(f"\n📋 [{q['id']}]: {q['title']}")
        print(f"   Ground Truth: {q['ground_truth']:.1f}% | V1 Baseline: {q['v1_score']:.1f}%")
        print("-" * 80)

        panel = INDIAN_PERSONAS_V2 if q["panel"] == "INDIA" else SAMPLE_PERSONAS_V2

        # 1. Run V2.1 (Option A)
        v2_1_weighted = 0.0
        for p in panel:
            res = interview_persona_v2_1(p, q["text"], api_key=GEMINI_KEY)
            v2_1_weighted += res["target_metric_score"] * p.population_weight
            time.sleep(1.0)

        # 2. Run V2.2 (Option B)
        v2_2_weighted = 0.0
        for p in panel:
            res = interview_persona_v2_2(p, q["text"], api_key=GEMINI_KEY)
            v2_2_weighted += res["target_metric_score"] * p.population_weight
            time.sleep(1.0)

        gt = q["ground_truth"]
        err_v1 = abs(q["v1_score"] - gt)
        err_v2_1 = abs(v2_1_weighted - gt)
        err_v2_2 = abs(v2_2_weighted - gt)

        winner = "V2.1 (Option A)" if err_v2_1 < err_v2_2 else "V2.2 (Option B)"

        print(f"  🎯 V2.1 Score (Opt A): {v2_1_weighted:>5.1f}% (Error: {v2_1_weighted - gt:>+5.1f}%)")
        print(f"  ⚡ V2.2 Score (Opt B): {v2_2_weighted:>5.1f}% (Error: {v2_2_weighted - gt:>+5.1f}%)")
        print(f"  🏆 Winner for this question: {winner}")

        scorecard.append({
            "id": q["id"],
            "title": q["title"],
            "ground_truth": gt,
            "v1_score": q["v1_score"],
            "v1_error": round(err_v1, 1),
            "v2_1_score": round(v2_1_weighted, 1),
            "v2_1_error": round(err_v2_1, 1),
            "v2_2_score": round(v2_2_weighted, 1),
            "v2_2_error": round(err_v2_2, 1),
            "winner": winner
        })

    print("\n" + "=" * 90)
    print(" 🏁 FINAL A/B TEST SCORECARD")
    print("=" * 90)
    print(f"{'Test':<28} | {'GT':<6} | {'V1 (Δ)':<12} | {'V2.1 Opt A (Δ)':<16} | {'V2.2 Opt B (Δ)':<16} | {'Winner'}")
    print("-" * 90)
    total_mae_v1 = 0.0
    total_mae_v2_1 = 0.0
    total_mae_v2_2 = 0.0

    for s in scorecard:
        total_mae_v1 += s["v1_error"]
        total_mae_v2_1 += s["v2_1_error"]
        total_mae_v2_2 += s["v2_2_error"]
        v1_str = f"{s['v1_score']:.1f}% ({s['v1_error']:.1f}%)"
        v2_1_str = f"{s['v2_1_score']:.1f}% ({s['v2_1_error']:.1f}%)"
        v2_2_str = f"{s['v2_2_score']:.1f}% ({s['v2_2_error']:.1f}%)"
        print(f"{s['id'] + ': ' + s['title'][:18]:<28} | {s['ground_truth']:>4.1f}% | {v1_str:>12} | {v2_1_str:>16} | {v2_2_str:>16} | {s['winner']}")

    n = len(scorecard)
    print("-" * 90)
    print(f"🎯 V1 Baseline MAE:     {total_mae_v1 / n:.1f}%")
    print(f"🚀 V2.1 (Option A) MAE: {total_mae_v2_1 / n:.1f}%")
    print(f"⚡ V2.2 (Option B) MAE: {total_mae_v2_2 / n:.1f}%")
    print("=" * 90)

if __name__ == "__main__":
    # Default: Run Deloitte suite or Indian suite based on argument
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "deloitte"
    if mode == "india":
        run_suite("Indian Consumer Empirical Study (N=2,500)", INDIA_QUESTIONS)
    else:
        run_suite("Deloitte Digital Media Trends Study (N=2,005)", DELOITTE_QUESTIONS)
