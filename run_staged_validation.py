"""
run_staged_validation.py
Executes the Progressive Walk-Forward Staged Benchmark for Engine V4.5

Stages:
- base:  Base Calibration Set (Q01 - Q35)
- gate1: Gate 1 Blind Test (Q36 - Q40) + Full Regression (Q01 - Q40)
- gate2: Gate 2 Blind Test (Q41 - Q45) + Full Regression (Q01 - Q45)
- gate3: Gate 3 Blind Test (Q46 - Q50) + Full Regression (Q01 - Q50)
- gate4: Gate 4 Blind Test (Q51 - Q55) + Full Regression (Q01 - Q55)
- all:   Runs the complete progression sequentially, halting if any gate fails
"""

import sys
import os
import argparse
import json

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
sys.stdout.reconfigure(encoding='utf-8')

from v4_5.engine_v4_5 import evaluate_question_v4_5
from v4_5.battery_v4_5 import (
    get_base_calibration_battery,
    get_gate_battery,
    get_cumulative_battery
)

def evaluate_battery(questions, title):
    print("=" * 105)
    print(f"EVALUATING: {title} (Total Questions: {len(questions)})")
    print("=" * 105)
    print(f"{'#':<4} | {'Question Title':<42} | {'Source':<18} | {'GT':<6} | {'V4.5':<6} | {'Err':<6} | {'Acc':<6} | Status")
    print("-" * 105)

    total_error = 0.0
    above_90_count = 0
    above_95_count = 0
    results = []

    for q in questions:
        res = evaluate_question_v4_5(q)
        err = res["error"]
        acc = res["accuracy"]
        total_error += err

        if acc >= 95.0:
            above_95_count += 1
            above_90_count += 1
            status_str = "PASS (★ >=95%)"
        elif acc >= 90.0:
            above_90_count += 1
            status_str = "PASS (>=90%)"
        else:
            status_str = f"FAIL (<90%: {acc}%)"

        results.append(res)
        print(f"{q.question_id:<4} | {q.title[:42]:<42} | {q.benchmark_source[:18]:<18} | {q.ground_truth:>5.1f}% | {res['predicted_rate']:>5.1f}% | {err:>5.1f}% | {acc:>5.1f}% | {status_str}")

    n = len(questions)
    mae = round(total_error / n, 2)
    grand_acc = round(100.0 - mae, 2)
    pct_90 = round((above_90_count / n) * 100.0, 1)
    pct_95 = round((above_95_count / n) * 100.0, 1)

    print("-" * 105)
    print(f"SUMMARY FOR {title}:")
    print(f"  • Total Questions:          {n}")
    print(f"  • Questions >= 90% Acc:     {above_90_count} / {n} ({pct_90}%)")
    print(f"  • Questions >= 95% Acc (★): {above_95_count} / {n} ({pct_95}%)")
    print(f"  • Mean Absolute Error (MAE): {mae}%")
    print(f"  • Grand Overall Accuracy:   {grand_acc}%")
    print("=" * 105 + "\n")

    return {
        "title": title,
        "count": n,
        "above_90": above_90_count,
        "above_95": above_95_count,
        "mae": mae,
        "grand_acc": grand_acc,
        "all_passed_90": above_90_count == n,
        "results": results
    }

def run_stage(stage_name):
    stage_name = stage_name.lower()

    if stage_name == "base":
        base_q = get_base_calibration_battery()
        summary = evaluate_battery(base_q, "STAGE 0: BASE CALIBRATION (Q01 - Q35)")
        return summary["all_passed_90"]

    gate_map = {"gate1": 1, "gate2": 2, "gate3": 3, "gate4": 4}
    if stage_name in gate_map:
        gate_num = gate_map[stage_name]
        gate_q = get_gate_battery(gate_num)
        
        # 1. Blind Test on isolated 5 questions
        blind_summary = evaluate_battery(gate_q, f"GATE {gate_num} BLIND OUT-OF-SAMPLE TEST (5 Questions)")
        
        # 2. Cumulative Regression Test from Q01 to end of this gate
        cumul_q = get_cumulative_battery(gate_num)
        cumul_summary = evaluate_battery(cumul_q, f"GATE {gate_num} FULL REGRESSION (Q01 to end of Gate {gate_num}, {len(cumul_q)} Questions)")
        
        return blind_summary["all_passed_90"] and cumul_summary["all_passed_90"]

    if stage_name == "all":
        print("\n" + "#" * 105)
        print("STARTING FULL PROGRESSIVE WALK-FORWARD VALIDATION PIPELINE")
        print("#" * 105 + "\n")

        # Step 0: Base
        if not run_stage("base"):
            print("ERROR: Base Calibration failed! Halting pipeline.")
            return False

        # Steps 1 to 4:
        for g in [1, 2, 3, 4]:
            print(f"\n>>> UNLOCKING GATE {g} >>>\n")
            passed = run_stage(f"gate{g}")
            if not passed:
                print(f"HALT: Gate {g} encountered failures. Need calibration before proceeding.")
                return False

        print("\n" + "#" * 105)
        print("ALL 4 GATES PASSED CLEANLY! PROGRESSIVE WALK-FORWARD VALIDATION COMPLETE!")
        print("#" * 105 + "\n")
        return True

    print(f"Unknown stage: {stage_name}")
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Progressive Walk-Forward Staged Validation Runner")
    parser.add_argument("--stage", type=str, default="base", choices=["base", "gate1", "gate2", "gate3", "gate4", "all"],
                        help="Stage to execute (base, gate1, gate2, gate3, gate4, all)")
    args = parser.parse_args()

    success = run_stage(args.stage)
    sys.exit(0 if success else 1)
