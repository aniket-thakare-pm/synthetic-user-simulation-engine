"""
run_staged_walkforward_v4.py
The Rigorous Staged Walk-Forward Benchmark Runner for Engine V4.4

OPERATIONAL LAWS:
1. Pure Rollback Baseline: Uses frozen v4_4/engine_v4_4.py.
2. Zero Micro-Adjustments: We do NOT tune numbers to pass failed questions.
3. Staged Progression:
   - Stage 0: Base Calibration (10 core questions)
   - Gate 1: Healthcare & Medical Involuntary Choices (5 questions)
   - Gate 2: Automotive, Physical Safety & Autonomous Trust (5 questions)
   - Gate 3: Banking, Direct Deposit & Revolving Credit (5 questions)
   - Gate 4: Retail Omnichannel, Curbside Pickup & Subscriptions (5 questions)
4. Cumulative Regression: Every gate is validated against all previous questions.
"""

import sys
import os
import argparse
from typing import List, Dict, Any

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
sys.stdout.reconfigure(encoding='utf-8')

from v4_4.engine_v4_4 import QuestionContextV4_4, PersonaEvaluationV4_4, evaluate_question_v4_4
from master_50q_battery import build_50_question_battery

def get_battery_by_stage(stage: str) -> List[QuestionContextV4_4]:
    """Retrieves questions partitioned into strict stages."""
    all_q = build_50_question_battery()
    q_map = {q.question_id: q for q in all_q}

    # Stage 0: 10 Core Questions across diverse baseline domains
    if stage == "base":
        base_ids = ["Q01", "Q02", "Q06", "Q11", "Q12", "Q26", "Q27", "Q31", "Q32", "Q36"]
        return [q_map[qid] for qid in base_ids if qid in q_map]

    # Gate 1: Healthcare & Prescription Copays (5 questions: Q37 to Q40 + Q07)
    if stage == "gate1":
        g1_ids = ["Q37", "Q38", "Q39", "Q40", "Q07"]
        return [q_map[qid] for qid in g1_ids if qid in q_map]

    # Gate 2: Automotive, EV Driving & In-Vehicle Controls (5 questions: Q41 to Q45)
    if stage == "gate2":
        g2_ids = ["Q41", "Q42", "Q43", "Q44", "Q45"]
        return [q_map[qid] for qid in g2_ids if qid in q_map]

    # Gate 3: Banking, Direct Deposit & Consumer Credit (5 questions: Q46 to Q50)
    if stage == "gate3":
        g3_ids = ["Q46", "Q47", "Q48", "Q49", "Q50"]
        return [q_map[qid] for qid in g3_ids if qid in q_map]

    # Gate 4: Retail Omnichannel & Subscriptions (5 questions: Q51 to Q55)
    if stage == "gate4":
        g4_ids = ["Q51", "Q52", "Q53", "Q54", "Q55"]
        return [q_map[qid] for qid in g4_ids if qid in q_map]

    raise ValueError(f"Unknown stage: {stage}")

def run_suite(questions: List[QuestionContextV4_4], title: str) -> Dict[str, Any]:
    print("=" * 105)
    print(f"EVALUATING: {title} (Total Questions: {len(questions)})")
    print("=" * 105)
    print(f"{'#':<5} | {'Question Title':<42} | {'Source':<18} | {'GT':<6} | {'V4.4':<6} | {'Err':<6} | {'Acc':<6} | Status")
    print("-" * 105)

    total_error = 0.0
    above_90_count = 0
    above_95_count = 0
    results = []

    for q in questions:
        res = evaluate_question_v4_4(q)
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
        print(f"{q.question_id:<5} | {q.title[:42]:<42} | {q.benchmark_source[:18]:<18} | {q.ground_truth:>5.1f}% | {res['predicted_rate']:>5.1f}% | {err:>5.1f}% | {acc:>5.1f}% | {status_str}")

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

def main():
    parser = argparse.ArgumentParser(description="Staged Walk-Forward Runner for Engine V4.4")
    parser.add_argument("--stage", type=str, default="base", choices=["base", "gate1", "gate2", "gate3", "gate4", "all"])
    args = parser.parse_args()

    stage_map = {
        "base": ["base"],
        "gate1": ["base", "gate1"],
        "gate2": ["base", "gate1", "gate2"],
        "gate3": ["base", "gate1", "gate2", "gate3"],
        "gate4": ["base", "gate1", "gate2", "gate3", "gate4"],
        "all": ["base", "gate1", "gate2", "gate3", "gate4"]
    }

    stages_to_run = stage_map[args.stage]
    cumulative_questions = []

    for idx, s in enumerate(stages_to_run):
        stage_questions = get_battery_by_stage(s)
        
        if s == "base":
            print("\n" + "#" * 105)
            print("STAGE 0: BASE CALIBRATION (10 CORE BENCHMARK QUESTIONS)")
            print("#" * 105 + "\n")
            res = run_suite(stage_questions, "STAGE 0: BASE CALIBRATION (10 Questions)")
            if not res["all_passed_90"]:
                print(f"HALT: Stage 0 encountered failures. Stopping.")
                sys.exit(1)
            cumulative_questions.extend(stage_questions)
        else:
            gate_num = s.replace("gate", "")
            print("\n" + "#" * 105)
            print(f">>> UNLOCKING GATE {gate_num} BLIND OUT-OF-SAMPLE TEST >>>")
            print("#" * 105 + "\n")
            
            # 1. Blind Test on the isolated 5 questions
            blind_res = run_suite(stage_questions, f"GATE {gate_num} BLIND TEST (5 Questions)")
            
            # 2. Cumulative regression test
            cumulative_questions.extend(stage_questions)
            cumul_res = run_suite(cumulative_questions, f"GATE {gate_num} CUMULATIVE REGRESSION ({len(cumulative_questions)} Questions)")
            
            if not (blind_res["all_passed_90"] and cumul_res["all_passed_90"]):
                print(f"HALT: Gate {gate_num} failed or caused regression. Stopping.")
                sys.exit(1)

    print("\n" + "#" * 105)
    print("STAGED WALK-FORWARD PIPELINE COMPLETED SUCCESSFULLY WITH ZERO REGRESSIONS!")
    print("#" * 105 + "\n")
    sys.exit(0)

if __name__ == "__main__":
    main()
