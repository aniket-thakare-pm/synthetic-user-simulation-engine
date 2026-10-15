"""
simulate_own_product.py
Dogfooding the Synthetic User Simulation Engine on OUR OWN PRODUCT.

Audience: 5 Qualified Zoomed Target Buyer Personas (Product & Tech Leaders)
Econometric Engine: Engine V4.7 (Continuous Social Consensus + V_inertia + 95% Credible Intervals)

Evaluates 5 De-Biased, Neutral Fundamental Questions regarding market demand,
trust, and adoption friction for our synthetic user platform.
"""

import sys
import os
from typing import List, Dict, Any

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
sys.stdout.reconfigure(encoding='utf-8')

from v4_7.engine_v4_7 import (
    QuestionContextV4_7,
    PersonaEvaluationV4_7,
    evaluate_question_v4_7
)

# =========================================================================
# THE 5 QUALIFIED ZOOMED TARGET BUYER PERSONAS
# =========================================================================
ZOOMED_PERSONAS = [
    {
        "id": "P1",
        "name": "Rachel Vance",
        "role": "Senior PM @ B2B SaaS",
        "weight": 0.25,
        "age": 34,
        "budget_monthly": 150,
        "patience": 6,
        "skepticism": 7,
        "loss_aversion": 2.1,
        "status_quo_inertia": 6,
        "context": "Ships bi-weekly sprints in a fast-growing B2B startup. High pressure to move fast, needs evidence to defend roadmap decisions."
    },
    {
        "id": "P2",
        "name": "Tomás Garcia",
        "role": "Solo Technical Founder",
        "weight": 0.20,
        "age": 28,
        "budget_monthly": 40,
        "patience": 8,
        "skepticism": 5,
        "loss_aversion": 1.7,
        "status_quo_inertia": 3,
        "context": "Bootstrapping an MVP. Zero budget for $1,000 research panels, needs immediate directional feedback before coding."
    },
    {
        "id": "P3",
        "name": "Dr. Aris Thorne",
        "role": "Head of UX Research @ Enterprise",
        "weight": 0.20,
        "age": 46,
        "budget_monthly": 1500,
        "patience": 4,
        "skepticism": 9,
        "loss_aversion": 2.4,
        "status_quo_inertia": 8,
        "context": "Enterprise methodology purist. Deeply skeptical of AI sycophancy, demands rigorous auditability and real human empathy."
    },
    {
        "id": "P4",
        "name": "Neha Kapoor",
        "role": "Niche B2B Product Lead",
        "weight": 0.20,
        "age": 31,
        "budget_monthly": 200,
        "patience": 5,
        "skepticism": 6,
        "loss_aversion": 1.9,
        "status_quo_inertia": 5,
        "context": "Builds compliance software for hospital administrators. Struggles constantly to book 30 minutes on busy prospects' calendars."
    },
    {
        "id": "P5",
        "name": "Liam O'Connor",
        "role": "VP of Product / CPO",
        "weight": 0.15,
        "age": 51,
        "budget_monthly": 800,
        "patience": 5,
        "skepticism": 8,
        "loss_aversion": 2.2,
        "status_quo_inertia": 7,
        "context": "Manages 50 engineers. Cares about engineering efficiency, ROI, and eliminating features that flop post-launch."
    }
]

def build_own_product_questions() -> List[QuestionContextV4_7]:
    questions = []

    # -------------------------------------------------------------------------
    # Q1: Evidence Source for Roadmap Prioritization
    # -------------------------------------------------------------------------
    questions.append(QuestionContextV4_7(
        question_id="Q1",
        title="Evidence Source for Roadmap Prioritization",
        benchmark_source="Product Management Validation Panel (Zoomed)",
        ground_truth=50.0,  # Neutral prior reference
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=2.0,
        is_status_quo_inertia=True,  # Incumbent habit: real human interviews / user calls
        evaluations=[
            PersonaEvaluationV4_7(
                "Rachel Vance", "Senior PM @ B2B SaaS", 0.25,
                "YES", 0.8, 3.8,
                "In bi-weekly sprints, I can't wait two weeks for recruitment. If the synthetic personas give me credible directional signal by Thursday, I'll use it alongside telemetry.",
                "Needs credibility with VP."
            ),
            PersonaEvaluationV4_7(
                "Tomás Garcia", "Solo Technical Founder", 0.20,
                "YES", 1.5, 2.0,
                "I literally have nobody to interview. If I can stress-test my feature ideas in 30 seconds against calibrated personas, it's 10x better than flying blind.",
                "Needs fast, affordable validation."
            ),
            PersonaEvaluationV4_7(
                "Dr. Aris Thorne", "Head of UX Research @ Enterprise", 0.20,
                "NO", -1.8, 8.2,
                "LLMs hallucinate agreeable feedback. If a PM shows me synthetic data instead of sitting in front of a real paying customer, I will veto the proposal immediately.",
                "Zero tolerance for AI sycophancy without human grounding."
            ),
            PersonaEvaluationV4_7(
                "Neha Kapoor", "Niche B2B Product Lead", 0.20,
                "YES", 1.1, 3.2,
                "Booking hospital procurement managers takes 3 weeks. A calibrated proxy to filter out dumb UX ideas before I burn my few real calls is invaluable.",
                "Interview recruitment bottleneck."
            ),
            PersonaEvaluationV4_7(
                "Liam O'Connor", "VP of Product / CPO", 0.15,
                "NO", -0.9, 6.5,
                "I'm accountable to the board. If an executive asks 'Did you speak to actual enterprise customers?', saying 'We asked a synthetic persona' is career suicide.",
                "C-suite governance and audit risk."
            )
        ]
    ))

    # -------------------------------------------------------------------------
    # Q2: Validation Timing: Pre-Launch Simulation vs In-Market Testing
    # -------------------------------------------------------------------------
    questions.append(QuestionContextV4_7(
        question_id="Q2",
        title="Validation Timing: Pre-Launch Simulation vs Live In-Market A/B Testing",
        benchmark_source="Product Management Validation Panel (Zoomed)",
        ground_truth=50.0,
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=1.8,
        is_status_quo_inertia=True,  # Incumbent habit: "Ship it to prod and look at PostHog"
        evaluations=[
            PersonaEvaluationV4_7(
                "Rachel Vance", "Senior PM @ B2B SaaS", 0.25,
                "NO", -0.8, 5.5,
                "Our continuous deployment pipeline lets us ship a feature flag to 5% of users in 2 days. Live analytics show actual credit card swipes, not simulated intent.",
                "Prefers real telemetry over simulated intent."
            ),
            PersonaEvaluationV4_7(
                "Tomás Garcia", "Solo Technical Founder", 0.20,
                "YES", 1.4, 2.5,
                "I don't have enough traffic for A/B testing. I have 300 active users; an A/B test would take 6 months to reach statistical significance. I need pre-code simulation.",
                "Low-traffic sample size limitation."
            ),
            PersonaEvaluationV4_7(
                "Dr. Aris Thorne", "Head of UX Research @ Enterprise", 0.20,
                "NO", -1.5, 7.8,
                "A/B testing measures real behavioral commitment under actual cognitive load. Simulation is at best an exploratory brainstorming exercise.",
                "Behavioral commitment gap."
            ),
            PersonaEvaluationV4_7(
                "Neha Kapoor", "Niche B2B Product Lead", 0.20,
                "YES", 1.2, 3.0,
                "In enterprise health-tech, you cannot 'move fast and break things' in production. You can't ship a broken workflow to a hospital. Pre-launch simulation is mandatory.",
                "High regulatory and deployment risk."
            ),
            PersonaEvaluationV4_7(
                "Liam O'Connor", "VP of Product / CPO", 0.15,
                "YES", 0.9, 4.0,
                "Our eng sprint costs $80,000. If pre-launch simulation kills even one useless feature before eng builds it, it pays for itself 50 times over.",
                "Engineering waste reduction ROI."
            )
        ]
    ))

    # -------------------------------------------------------------------------
    # Q3: Specialized B2B Discovery: Simulated Personas vs Direct Outreach
    # -------------------------------------------------------------------------
    questions.append(QuestionContextV4_7(
        question_id="Q3",
        title="Specialized B2B Discovery: Domain Personas vs Direct Outreach",
        benchmark_source="Product Management Validation Panel (Zoomed)",
        ground_truth=50.0,
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=1.9,
        is_status_quo_inertia=True,  # Incumbent habit: cold outreach / LinkedIn / conferences
        evaluations=[
            PersonaEvaluationV4_7(
                "Rachel Vance", "Senior PM @ B2B SaaS", 0.25,
                "YES", 1.1, 3.2,
                "We use both, but simulating the buyer persona first helps us craft the outreach message so our cold response rate actually improves.",
                "Message de-risking."
            ),
            PersonaEvaluationV4_7(
                "Tomás Garcia", "Solo Technical Founder", 0.20,
                "YES", 1.6, 1.8,
                "Cold LinkedIn messaging as a solo dev has a 2% reply rate. I waste weeks. Giving me a calibrated persona of a CTO to spar with saves my runway.",
                "Founder runway conservation."
            ),
            PersonaEvaluationV4_7(
                "Dr. Aris Thorne", "Head of UX Research @ Enterprise", 0.20,
                "NO", -1.4, 7.0,
                "Discovery is about uncovering unknown unknowns. An LLM persona only knows what is already in its training corpus; it cannot reveal novel industry shifts.",
                "Cannot surface unknown-unknowns."
            ),
            PersonaEvaluationV4_7(
                "Neha Kapoor", "Niche B2B Product Lead", 0.20,
                "YES", 1.5, 2.2,
                "When your target user makes $400k/year and has zero open calendar slots, high-fidelity simulation is literally the only practical pre-flight tool.",
                "Zero access to high-value buyers."
            ),
            PersonaEvaluationV4_7(
                "Liam O'Connor", "VP of Product / CPO", 0.15,
                "NO", -0.5, 5.2,
                "Direct relationships are how enterprise sales happen. Discovery calls aren't just research; they are early sales pipeline. Simulation doesn't build a pipeline.",
                "Discovery-as-sales pipeline."
            )
        ]
    ))

    # -------------------------------------------------------------------------
    # Q4: Methodology: Broad Synthetic Scale vs In-Depth Qualitative Human Sessions
    # -------------------------------------------------------------------------
    questions.append(QuestionContextV4_7(
        question_id="Q4",
        title="Methodology: Broad Synthetic Scale vs In-Depth Qualitative Sessions",
        benchmark_source="Product Management Validation Panel (Zoomed)",
        ground_truth=50.0,
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=2.1,
        is_status_quo_inertia=True,  # Incumbent habit: 5-8 qualitative Zoom interviews
        evaluations=[
            PersonaEvaluationV4_7(
                "Rachel Vance", "Senior PM @ B2B SaaS", 0.25,
                "NO", -0.9, 6.0,
                "Scale without depth doesn't help me understand 'why'. I'd rather hear 6 real users explain their daily frustration than see 500 simulated bar charts.",
                "Prioritizes 'why' over simulated 'how many'."
            ),
            PersonaEvaluationV4_7(
                "Tomás Garcia", "Solo Technical Founder", 0.20,
                "YES", 1.2, 2.8,
                "I don't have time to transcribe and analyze 10 one-hour interviews. I need a clear distribution of whether people would pay $20/mo or $50/mo.",
                "Prefers rapid quantified distribution."
            ),
            PersonaEvaluationV4_7(
                "Dr. Aris Thorne", "Head of UX Research @ Enterprise", 0.20,
                "NO", -2.0, 9.0,
                "Ten real qualitative interviews reveal facial hesitation, tone shifts, and spontaneous workarounds that no synthetic model can ever replicate. Non-negotiable.",
                "Irreplaceable human emotional signal."
            ),
            PersonaEvaluationV4_7(
                "Neha Kapoor", "Niche B2B Product Lead", 0.20,
                "NO", -0.7, 5.8,
                "When dealing with specialized hospital workflows, one nuanced workflow detail from a nurse is worth more than 1,000 synthetic responses.",
                "High value of deep domain edge-cases."
            ),
            PersonaEvaluationV4_7(
                "Liam O'Connor", "VP of Product / CPO", 0.15,
                "YES", 0.8, 4.2,
                "Sample size of 5 gives me zero statistical defensibility when presenting to the CEO. Having 500 data points gives the roadmap quantitative backing.",
                "Statistical executive defensibility."
            )
        ]
    ))

    # -------------------------------------------------------------------------
    # Q5: Persona Maintenance: Automated Synthetic Platform vs First-Party Personas
    # -------------------------------------------------------------------------
    questions.append(QuestionContextV4_7(
        question_id="Q5",
        title="Persona Maintenance: Automated Dynamic Tool vs Static First-Party Personas",
        benchmark_source="Product Management Validation Panel (Zoomed)",
        ground_truth=50.0,
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=1.8,
        is_status_quo_inertia=True,  # Incumbent habit: Notion doc / Figma slides from past interviews
        evaluations=[
            PersonaEvaluationV4_7(
                "Rachel Vance", "Senior PM @ B2B SaaS", 0.25,
                "YES", 1.3, 3.0,
                "Our Notion personas are 18 months out of date and nobody looks at them. An interactive, queryable persona tool that we can question in real time would actually get used.",
                "Static persona decay in Notion."
            ),
            PersonaEvaluationV4_7(
                "Tomás Garcia", "Solo Technical Founder", 0.20,
                "YES", 1.4, 2.2,
                "I don't have support tickets or sales calls yet. An out-of-the-box calibrated persona library gets me started immediately without manual documentation.",
                "Zero cold-start data."
            ),
            PersonaEvaluationV4_7(
                "Dr. Aris Thorne", "Head of UX Research @ Enterprise", 0.20,
                "NO", -1.2, 6.8,
                "If the personas don't link directly to our actual customer Gong recordings and Zendesk tickets, they are just fictional characters. I build personas from raw ground truth.",
                "Requires direct link to 1st-party customer data."
            ),
            PersonaEvaluationV4_7(
                "Neha Kapoor", "Niche B2B Product Lead", 0.20,
                "YES", 0.9, 4.1,
                "A dynamic persona that updates its behavioral friction when we change our pricing parameters is infinitely more useful than a static PDF slide deck.",
                "Dynamic parameter testing."
            ),
            PersonaEvaluationV4_7(
                "Liam O'Connor", "VP of Product / CPO", 0.15,
                "YES", 1.1, 3.5,
                "My designers and PMs argue constantly over what 'the user' wants. A shared, standardized simulation engine creates a common benchmark and ends circular debates.",
                "Cross-functional alignment tool."
            )
        ]
    ))

    return questions

def run_dogfooding_simulation():
    questions = build_own_product_questions()

    print("=" * 120)
    print("DOGFOODING SIMULATION: TESTING OUR OWN SYNTHETIC USER PLATFORM")
    print("Audience: 5 Qualified Zoomed Product Decision-Makers (Rachel, Tomás, Dr. Aris, Neha, Liam)")
    print("Engine: Nobel-Econometric Engine V4.7 (Continuous Consensus + Incumbent Inertia + 95% CI)")
    print("=" * 120 + "\n")

    summary_table = []

    for q in questions:
        res = evaluate_question_v4_7(q)
        pred = res["predicted_rate"]
        ci = res["credible_interval_95"]
        ci_str = f"[{ci[0]:>4.1f}%, {ci[1]:>4.1f}%]"

        verdict = "ADOPTION FAVORED (>50%)" if pred >= 50.0 else "RESISTANCE / STATUS QUO FAVORED (<50%)"

        print("-" * 120)
        print(f"QUESTION {q.question_id}: {q.title.upper()}")
        print(f"Market Decision: Option A (Synthetic Tool) vs Option B (Status Quo Incumbent)")
        print(f"Predicted Adoption Rate: {pred:>5.1f}% | 95% Credible Interval: {ci_str} | Verdict: {verdict}")
        print("-" * 120)
        print(f"{'Persona':<18} | {'Stance':<6} | {'P(Adopt)':<8} | {'Net ΔV':<7} | {'Verbatim Quote & Strategic Objection'}")
        print("-" * 120)

        for p in res["persona_logs"]:
            print(f"{p['persona']:<18} | {p['stance']:<6} | {p['score']:>6.1f}% | {p['shift']:>5.2f} | \"{p['response']}\"")
            print(f"{'':<18} | {'':<6} | {'':<8} | {'':<7} | Primary Friction: {p['objection']}")
            print()

        summary_table.append({
            "qid": q.question_id,
            "title": q.title,
            "rate": pred,
            "ci": ci_str,
            "verdict": verdict
        })

    print("=" * 120)
    print("EXECUTIVE SUMMARY: MARKET READINESS FOR OUR SYNTHETIC USER PLATFORM")
    print("=" * 120)
    print(f"{'#':<4} | {'Product Decision Scenario':<55} | {'P(Adopt)':<9} | {'95% Credible Interval':<16} | {'Market Outcome'}")
    print("-" * 120)
    for row in summary_table:
        print(f"{row['qid']:<4} | {row['title']:<55} | {row['rate']:>7.1f}% | {row['ci']:<16} | {row['verdict']}")
    print("=" * 120 + "\n")

if __name__ == "__main__":
    run_dogfooding_simulation()
