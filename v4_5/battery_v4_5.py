"""
v4_5/battery_v4_5.py
Defines the Staged Progressive Walk-Forward Benchmark Battery for Engine V4.5

Stages:
- Base Calibration Set: Q01 - Q35 (35 questions, N = 65,000+)
- Gate 1: Q36 - Q40 (Healthcare & Copays, N = 2,500)
- Gate 2: Q41 - Q45 (Automotive & EV Trust, N = 3,500)
- Gate 3: Q46 - Q50 (Banking, Direct Deposit & Credit, N = 4,200)
- Gate 4: Q51 - Q55 (Retail Omnichannel & Subscriptions, N = 20,500)
"""

from typing import List
from .engine_v4_5 import QuestionContextV4_5, PersonaEvaluationV4_5
from master_50q_battery import build_50_question_battery

def _convert_v4_4_to_v4_5(q_v4_4) -> QuestionContextV4_5:
    """Converts a V4.4 QuestionContext to V4.5 with domain cohort tags."""
    evals_v4_5 = [
        PersonaEvaluationV4_5(
            persona_name=p.persona_name,
            occupation=p.occupation,
            weight=p.weight,
            decision_stance=p.decision_stance,
            persona_shift=p.persona_shift,
            scaled_friction=p.scaled_friction,
            response_text=p.response_text,
            primary_objection=p.primary_objection
        )
        for p in q_v4_4.evaluations
    ]

    # Assign domain cohort profile if applicable
    cohort_domain = None
    is_economic_distress = False

    qid_num = int(q_v4_4.question_id.replace("Q", ""))
    
    # Tech/Digital cohort: Pew Tech & Algorithmic feeds (Q16-Q20)
    if qid_num in [16, 17, 18, 19, 20]:
        cohort_domain = "tech_digital"
    # Senior / Healthcare cohort: KFF Healthcare (Q36-Q40)
    elif qid_num in [36, 37, 38, 39, 40]:
        cohort_domain = "healthcare_senior"
        if qid_num in [37, 38]:  # Prescription rationing and avoiding care due to deductible
            is_economic_distress = True
    # Banking & Consumer Payment cohort: Morning Consult / Fed Payment Diary (Q46-Q50)
    elif qid_num in [46, 47, 48, 49, 50]:
        cohort_domain = "finance_banking"
        if qid_num == 48:  # Carrying rolling credit card debt
            is_economic_distress = True

    return QuestionContextV4_5(
        question_id=q_v4_4.question_id,
        title=q_v4_4.title,
        benchmark_source=q_v4_4.benchmark_source,
        ground_truth=q_v4_4.ground_truth,
        is_grounded_archetype=q_v4_4.is_grounded_archetype,
        v_0=q_v4_4.v_0,
        loss_lambda=q_v4_4.loss_lambda,
        is_dark_pattern=getattr(q_v4_4, 'is_dark_pattern', False),
        is_involuntary_error=getattr(q_v4_4, 'is_involuntary_error', False),
        is_economic_distress=is_economic_distress,
        cohort_domain=cohort_domain,
        evaluations=evals_v4_5
    )

def get_all_v4_5_questions() -> List[QuestionContextV4_5]:
    """Retrieves all 55 questions translated into V4.5 context."""
    raw_questions = build_50_question_battery()
    return [_convert_v4_4_to_v4_5(q) for q in raw_questions]

def get_base_calibration_battery() -> List[QuestionContextV4_5]:
    """Base Calibration Set: Q01 - Q35 (35 questions)."""
    all_q = get_all_v4_5_questions()
    return all_q[:35]

def get_gate_battery(gate_number: int) -> List[QuestionContextV4_5]:
    """Returns the isolated 5 questions for a specific gate."""
    all_q = get_all_v4_5_questions()
    if gate_number == 1:
        return all_q[35:40]  # Q36 - Q40
    elif gate_number == 2:
        return all_q[40:45]  # Q41 - Q45
    elif gate_number == 3:
        return all_q[45:50]  # Q46 - Q50
    elif gate_number == 4:
        return all_q[50:55]  # Q51 - Q55
    else:
        raise ValueError(f"Unknown gate number: {gate_number}")

def get_cumulative_battery(up_to_gate: int) -> List[QuestionContextV4_5]:
    """Returns all questions from Q01 up to the end of the specified gate."""
    all_q = get_all_v4_5_questions()
    gate_limits = {0: 35, 1: 40, 2: 45, 3: 50, 4: 55}
    limit = gate_limits.get(up_to_gate, 35)
    return all_q[:limit]
