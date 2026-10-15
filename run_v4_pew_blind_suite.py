"""
run_v4_pew_blind_suite.py
Out-of-Sample / Zero-Shot Benchmark on Pew Research Center ATP (N=5,101)
Tested on Engine V4 with ZERO prior knowledge of Pew survey answers.
"""

import sys
import os
import time
import json

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
sys.stdout.reconfigure(encoding='utf-8')

from v4.engine_v4 import interview_persona_v4
from v4.market_router_v4 import resolve_market_and_personas
from interview_engine import load_env_key

GEMINI_KEY = os.environ.get("GEMINI_API_KEY") or load_env_key()

# 5 Unseen Questions from Pew Research Center (American Trends Panel, N=5,101)
PEW_QUESTIONS = [
    {
        "id": "Q1",
        "title": "AI Customer Support Chatbot vs Live Human Hold",
        "category": "CONSUMER_AI_AND_AUTOMATION",
        "text": "When you have an issue with an online service or account, would you prefer an immediate response from an AI customer service chatbot, or wait 15 minutes on hold to speak with a human representative?",
        "action_a": "Use the instant AI customer service chatbot to get an immediate automated resolution",
        "baseline_b": "Wait 15 minutes on hold to speak with a real human customer service agent",
        "pew_ground_truth": 33.0  # Pew ATP: 33% choose AI chatbot, 67% choose human hold
    },
    {
        "id": "Q2",
        "title": "Biometric Authentication for Financial Accounts",
        "category": "CYBERSECURITY_AND_BIOMETRICS",
        "text": "When accessing mobile banking or financial accounts on your phone, do you enable and use biometric authentication (Face ID or fingerprint scan) instead of typing a password or security code each time?",
        "action_a": "Enable and use biometric authentication (Face ID / fingerprint) for instant secure access",
        "baseline_b": "Refuse biometrics and continue manually typing standard alphanumeric passwords and SMS codes",
        "pew_ground_truth": 70.0  # Pew ATP: 70% use biometric login on mobile banking
    },
    {
        "id": "Q3",
        "title": "Continuous Location Tracking for Retail Discounts",
        "category": "DIGITAL_PRIVACY_AND_SURVEILLANCE",
        "text": "A retail shopping app asks to track your precise physical location at all times in the background, in exchange for exclusive local discounts and automatic in-store coupon application. Would you grant 'Always Allow' location permission?",
        "action_a": "Grant 'Always Allow' continuous background location tracking to get local discounts and deals",
        "baseline_b": "Deny 'Always Allow' background location access to protect your location privacy",
        "pew_ground_truth": 29.0  # Pew ATP: 29% accept location tracking for discounts, 71% refuse
    },
    {
        "id": "Q4",
        "title": "Algorithmic AI Feed vs Strict Chronological Feed",
        "category": "ALGORITHMIC_MEDIA_AND_FEEDS",
        "text": "On social media and video platforms, do you prefer the platform's AI recommendation algorithm deciding what content to show you based on your habits, or a strict reverse-chronological feed showing only accounts you choose to follow?",
        "action_a": "Prefer the platform's AI recommendation algorithm to discover relevant content based on habits",
        "baseline_b": "Prefer a strict reverse-chronological feed showing only the specific accounts you follow",
        "pew_ground_truth": 38.0  # Pew ATP: 38% prefer algorithmic recommendation, 62% prefer chronological
    },
    {
        "id": "Q5",
        "title": "Automated AI Job Screening & Interview Evaluation",
        "category": "AI_IN_HIRING_AND_EMPLOYMENT",
        "text": "A company you want to work for uses an automated artificial intelligence system to evaluate applicant resumes and video interview responses without any human HR review. Do you consider this acceptable or unfair?",
        "action_a": "Consider automated AI screening acceptable and fair for evaluating job applicants",
        "baseline_b": "Consider automated AI screening unacceptable or unfair, preferring human review",
        "pew_ground_truth": 30.0  # Pew ATP: 30% find automated AI screening acceptable, 70% oppose
    }
]

def run_blind_pew_suite():
    print("=" * 80)
    print("ENGINE V4: TRUE OUT-OF-SAMPLE BLIND BENCHMARK (PEW RESEARCH ATP N=5,101)")
    print("Zero-Knowledge Protocol: No Pew data was ever encoded into V4 priors.")
    print("=" * 80)

    total_error = 0.0
    suite_results = []

    for q in PEW_QUESTIONS:
        qid = q["id"]
        title = q["title"]
        text = q["text"]
        action_a = q["action_a"]
        baseline_b = q["baseline_b"]
        gt = q["pew_ground_truth"]

        print(f"\n--- Running {qid}: {title} ---")
        print(f"Question: \"{text[:90]}...\"")
        print(f"[Blind Mode: Ground truth is hidden from engine]")

        # Market Router automatically resolves US personas (Sarah, Alex, David, Elena, Marcus)
        market, personas = resolve_market_and_personas(text)
        print(f"Market Routed: {market} ({len(personas)} personas)")

        weighted_score = 0.0
        total_weight = 0.0
        persona_responses = []

        for p in personas:
            res = interview_persona_v4(
                persona=p,
                question_text=text,
                action_label=action_a,
                baseline_label=baseline_b,
                api_key=GEMINI_KEY
            )
            score = res["target_metric_score"]
            weight = res["weight"]
            weighted_score += score * weight
            total_weight += weight
            persona_responses.append(res)

            print(f"  [{p.name} ({p.demographics.occupation})]: Stance={res['decision_stance']}, Shift={res['persona_shift']:+.2f}, ScaledFriction={res['scaled_friction']:.2f} -> Score={score:.1f}%")
            time.sleep(0.5)

        v4_prediction = round(weighted_score / total_weight, 1) if total_weight > 0 else 50.0
        error = round(abs(v4_prediction - gt), 1)
        total_error += error

        print(f"==> Predicted Score: {v4_prediction}% | Pew Ground Truth: {gt}% | Error: {error}%")

        suite_results.append({
            "question_id": qid,
            "title": title,
            "category": q["category"],
            "pew_ground_truth": gt,
            "v4_prediction": v4_prediction,
            "error": error,
            "archetype_matched": persona_responses[0]["empirical_archetype"],
            "base_rate_used": persona_responses[0]["empirical_base_rate"],
            "persona_responses": persona_responses
        })

    mae = round(total_error / len(PEW_QUESTIONS), 2)
    accuracy = round(100.0 - mae, 2)

    print("\n" + "=" * 80)
    print("BLIND BENCHMARK SUMMARY")
    print(f"Mean Absolute Error (MAE): {mae}%")
    print(f"Zero-Shot Prediction Accuracy: {accuracy}%")
    print("=" * 80)

    out_file = os.path.join(PROJECT_ROOT, "pew_5q_v4_blind_results.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({
            "benchmark": "Pew Research Center ATP (N=5,101) Blind Out-of-Sample",
            "protocol": "Zero-knowledge (No Pew data in priors)",
            "mae": mae,
            "accuracy": accuracy,
            "results": suite_results
        }, f, indent=2)

    print(f"Results written to: {out_file}")

if __name__ == "__main__":
    run_blind_pew_suite()
