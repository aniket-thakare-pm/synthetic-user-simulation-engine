import os
import sys
import json
import time

# Enforce UTF-8 encoding for standard output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from sample_personas import SAMPLE_PERSONAS
from interview_engine import interview_persona_stateless

def log(msg=""):
    print(msg, flush=True)

def run_deloitte_benchmark(api_key: str):
    log("=" * 80)
    log(" DELOITTE DIGITAL MEDIA TRENDS BENCHMARK TEST SUITE")
    log("=" * 80)

    questions = [
        {
            "id": "Q1",
            "name": "Deloitte Q1: $5 Monthly Price Hike Cancellation",
            "text": "Would you cancel your favorite video streaming service if the monthly subscription price increased by $5 per month, and why?",
            "deloitte_human_benchmark": 61.0
        },
        {
            "id": "Q2",
            "name": "Deloitte Q2: Show Hopping / Serial Churn Behavior",
            "text": "Do you subscribe to a streaming service just to watch a specific movie or show, and then cancel as soon as you finish watching it?",
            "deloitte_human_benchmark": 47.0
        }
    ]

    for q_idx, q in enumerate(questions, 1):
        log(f"\n{'='*80}")
        log(f" TEST {q_idx}: {q['name']}")
        log(f" Question: \"{q['text']}\"")
        log(f" Deloitte Human Control Baseline: {q['deloitte_human_benchmark']}%")
        log(f"{'='*80}")

        valid_responses = []
        for persona in SAMPLE_PERSONAS:
            weight_pct = int(persona.population_weight * 100)
            log(f"\n[Persona: {persona.name}] — {persona.demographics.occupation} (Population Weight: {weight_pct}%)")
            try:
                response = interview_persona_stateless(persona, q['text'], api_key)
                valid_responses.append(response)
                
                if response.deterministic_rule_triggered:
                    log(f"  HARD CONSTRAINT: {response.deterministic_rule_triggered}")
                
                log(f"   Majority Stance [{response.majority_percent}% {response.primary_action_direction}]: {response.majority_response}")
                log(f"   Minority Stance [{response.minority_percent}%]: {response.minority_exception}")
                log(f"   Persona Normalized Churn/Action Score: {response.churn_or_rejection_percent}%")
                log(f"   Persona Summary: \"{response.response_text}\"")
                if response.primary_objection:
                    log(f"   Concern: {response.primary_objection}")
            except Exception as e:
                log(f"  Error: {e}")
            log("-" * 80)
            time.sleep(1.2)  # Respect free tier rate limits

        if valid_responses:
            total_w = sum(r.population_weight for r in valid_responses)
            unweighted_avg = sum(r.churn_or_rejection_percent for r in valid_responses) / len(valid_responses)
            weighted_score = sum(r.population_weight * r.churn_or_rejection_percent for r in valid_responses) / total_w if total_w > 0 else 0
            
            diff_unweighted = abs(unweighted_avg - q['deloitte_human_benchmark'])
            diff_weighted = abs(weighted_score - q['deloitte_human_benchmark'])
            
            log(f"\nRESULTS FOR {q['id']}:")
            log(f"   Deloitte Real Human Control Benchmark: {q['deloitte_human_benchmark']:.1f}%")
            log(f"   Unweighted Synthetic Panel Score:       {unweighted_avg:.1f}% (Error Delta: {diff_unweighted:.1f}%)")
            log(f"   Post-Stratified Weighted Score (Wi):    {weighted_score:.1f}% (Error Delta: {diff_weighted:.1f}%)")
            log("=" * 80)

        time.sleep(2)

if __name__ == "__main__":
    key = os.environ.get("GEMINI_API_KEY")
    if not key and len(sys.argv) > 1:
        key = sys.argv[1]
    if not key:
        log("Missing API key")
        sys.exit(1)
    run_deloitte_benchmark(key)
