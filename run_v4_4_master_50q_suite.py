"""
run_v4_4_master_50q_suite.py
Executes Engine V4.4 on the Complete Master 50-Question Benchmark Battery
Spanning 10 Studies and 75,000+ Real Human Survey Respondents.
"""

import sys
import os
import json

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
sys.stdout.reconfigure(encoding='utf-8')

from v4_4.engine_v4_4 import evaluate_question_v4_4
from master_50q_battery import build_50_question_battery

def run_master_50q_suite():
    print("=" * 95)
    print("ENGINE V4.4 ENTERPRISE BENCHMARK: THE 50-QUESTION MASTER BATTERY")
    print("Testing 10 Published Empirical Studies Across 75,000+ Real Human Respondents")
    print("Features: Consensus Amplification, Cognitive Fatigue Damping, Adaptive Elasticity")
    print("=" * 95)

    questions = build_50_question_battery()
    total_questions = len(questions)

    total_error = 0.0
    above_90_count = 0
    suite_results = []

    print(f"\nEvaluating {total_questions} Benchmark Questions...\n")
    print(f"{'#':<4} | {'Question Title':<45} | {'Source':<20} | {'GT':<6} | {'V4.4':<6} | {'Err':<6} | {'Acc':<6} | Status")
    print("-" * 115)

    for idx, q in enumerate(questions, 1):
        res = evaluate_question_v4_4(q)
        err = res["error"]
        acc = res["accuracy"]
        total_error += err

        is_passed = acc >= 90.0
        if is_passed:
            above_90_count += 1
            status_str = "PASS (>=90%)"
        else:
            status_str = f"FAIL (<90%: {acc}%)"

        suite_results.append(res)

        print(f"{q.question_id:<4} | {q.title[:45]:<45} | {q.benchmark_source[:20]:<20} | {q.ground_truth:>5.1f}% | {res['predicted_rate']:>5.1f}% | {err:>5.1f}% | {acc:>5.1f}% | {status_str}")

    mae = round(total_error / total_questions, 2)
    overall_accuracy = round(100.0 - mae, 2)
    pass_percentage = round((above_90_count / total_questions) * 100.0, 1)

    print("\n" + "=" * 95)
    print("MASTER 50-QUESTION BENCHMARK SUMMARY")
    print(f"Total Questions Evaluated:         {total_questions}")
    print(f"Questions with >= 90% Accuracy:   {above_90_count} / {total_questions} ({pass_percentage}%)")
    print(f"Mean Absolute Error (MAE):         {mae}%")
    print(f"Grand Overall Prediction Accuracy: {overall_accuracy}%")
    print("=" * 95)

    out_file = os.path.join(PROJECT_ROOT, "master_50q_v4_4_results.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({
            "engine": "Engine V4.4 (Master Cognitive Choice Architecture)",
            "total_questions": total_questions,
            "passed_above_90": above_90_count,
            "pass_rate_percentage": pass_percentage,
            "grand_mae": mae,
            "grand_accuracy": overall_accuracy,
            "results": suite_results
        }, f, indent=2)

    print(f"Complete results written to: {out_file}\n")
    return above_90_count, total_questions, mae, overall_accuracy

if __name__ == "__main__":
    run_master_50q_suite()
