"""
simulate_own_product_round2.py
Dogfooding Round 2: Reframed Positioning for Our Synthetic User Engine.

Reframed Core Use-Case:
- NOT a replacement for deep human qualitative interviews.
- A "Pre-Flight Flight Simulator" for rapid micro-decisions, numerical pricing sensitivity,
  backlog pruning, and turning decaying static Notion personas into interactive query tools.

Audience: 5 Qualified Zoomed Product Decision-Makers (Rachel, Tomás, Dr. Aris, Neha, Liam)
Engine: Nobel-Econometric Engine V4.7 (Continuous Consensus + Incumbent Inertia + 95% CI)
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

def build_round2_product_questions() -> List[QuestionContextV4_7]:
    questions = []

    # -------------------------------------------------------------------------
    # Q1: Micro-Decision Speed (Fast UI/UX & Flow Choices)
    # -------------------------------------------------------------------------
    questions.append(QuestionContextV4_7(
        question_id="Q1",
        title="Micro-Decision Speed: Synthetic Rapid Pre-Flight vs Internal Guesswork",
        benchmark_source="Product Management Validation Panel (Zoomed - Round 2)",
        ground_truth=50.0,
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=1.8,
        is_status_quo_inertia=True,  # Incumbent habit: designer gut feel & internal team debate
        evaluations=[
            PersonaEvaluationV4_7(
                "Rachel Vance", "Senior PM @ B2B SaaS", 0.25,
                "YES", 1.5, 2.2,
                "We waste hours in sprint planning arguing over whether mandatory phone verification will hurt conversion. A 30-second simulation settles micro-debates with objective data instead of designer ego.",
                "Ends circular team debates."
            ),
            PersonaEvaluationV4_7(
                "Tomás Garcia", "Solo Technical Founder", 0.20,
                "YES", 1.7, 1.5,
                "As a solo dev, I have nobody to bounce micro-decisions off. Testing onboarding steps in 30 seconds gives me external perspective instantly.",
                "Instant feedback loop."
            ),
            PersonaEvaluationV4_7(
                "Dr. Aris Thorne", "Head of UX Research @ Enterprise", 0.20,
                "YES", 0.9, 3.8,
                "I don't have the UXR bandwidth to run 2-week studies on button copy and billing toggles. If PMs use this for minor mechanical micro-choices, it frees my team to focus on deep strategic human studies.",
                "Relieves UXR team from low-level tickets."
            ),
            PersonaEvaluationV4_7(
                "Neha Kapoor", "Niche B2B Product Lead", 0.20,
                "YES", 1.4, 2.4,
                "Micro-friction in enterprise software kills adoption. Being able to simulate 5 variations of a multi-step form before assigning eng tickets is pure velocity.",
                "Prevents enterprise form drop-offs."
            ),
            PersonaEvaluationV4_7(
                "Liam O'Connor", "VP of Product / CPO", 0.15,
                "YES", 1.2, 2.8,
                "My team's biggest velocity killer is bike-shedding over minor UX decisions. If this creates a standardized, data-backed standard for micro-decisions, it speeds up shipping by 25%.",
                "Eliminates internal bike-shedding."
            )
        ]
    ))

    # -------------------------------------------------------------------------
    # Q2: Numerical Pricing & Packaging Sensitivity
    # -------------------------------------------------------------------------
    questions.append(QuestionContextV4_7(
        question_id="Q2",
        title="Numerical Pricing: Calibrated Elasticity vs Live In-Market Guesswork",
        benchmark_source="Product Management Validation Panel (Zoomed - Round 2)",
        ground_truth=50.0,
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=2.0,
        is_status_quo_inertia=True,  # Incumbent habit: copy competitors & test on live users
        evaluations=[
            PersonaEvaluationV4_7(
                "Rachel Vance", "Senior PM @ B2B SaaS", 0.25,
                "YES", 1.3, 2.6,
                "You can't ask humans 'would you pay $29/mo' in interviews because they always say yes to be polite. An econometric model factoring in budget caps and loss aversion gives far more honest price floors.",
                "Bypasses human politeness bias in pricing."
            ),
            PersonaEvaluationV4_7(
                "Tomás Garcia", "Solo Technical Founder", 0.20,
                "YES", 1.6, 1.8,
                "Pricing an MVP is terrifying. You underprice because you're scared, or overprice and get zero sales. Running price sensitivity curves across personas takes the terror out of pricing.",
                "Eliminates founder pricing anxiety."
            ),
            PersonaEvaluationV4_7(
                "Dr. Aris Thorne", "Head of UX Research @ Enterprise", 0.20,
                "NO", -0.6, 5.5,
                "Van Westendorp Price Sensitivity Meter and conjoint analysis are already established quantitative methods. A synthetic model is interesting, but I need proof it matches Van Westendorp curves.",
                "Demands validation against Van Westendorp."
            ),
            PersonaEvaluationV4_7(
                "Neha Kapoor", "Niche B2B Product Lead", 0.20,
                "YES", 1.2, 3.0,
                "Testing price hikes on live enterprise customers can cause PR disasters and churn spikes. Having a simulated econometric sandbox to model customer loss aversion beforehand is essential.",
                "Risk-free pricing sandbox."
            ),
            PersonaEvaluationV4_7(
                "Liam O'Connor", "VP of Product / CPO", 0.15,
                "YES", 1.3, 2.5,
                "Price elasticity is purely mathematical. If the engine uses Nobel McFadden utility with income constraints, this is exactly the kind of numerical simulation software should be doing.",
                "Grounded in economic theory."
            )
        ]
    ))

    # -------------------------------------------------------------------------
    # Q3: Pre-Interview Question & Screener Optimization (The "Pre-Flight" Pilot)
    # -------------------------------------------------------------------------
    questions.append(QuestionContextV4_7(
        question_id="Q3",
        title="Pre-Flight Research Pilot: Synthetic Script Dry-Run vs Flying Blind",
        benchmark_source="Product Management Validation Panel (Zoomed - Round 2)",
        ground_truth=50.0,
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=1.7,
        is_status_quo_inertia=True,  # Incumbent habit: pilot on colleagues or wing it
        evaluations=[
            PersonaEvaluationV4_7(
                "Rachel Vance", "Senior PM @ B2B SaaS", 0.25,
                "YES", 1.4, 2.1,
                "Our real interviews cost $150 each. If I can dry-run my interview questions through synthetic personas to see which questions fall flat or confuse the personas, my real interviews become 2x more valuable.",
                "Maximizes ROI of expensive human interviews."
            ),
            PersonaEvaluationV4_7(
                "Tomás Garcia", "Solo Technical Founder", 0.20,
                "YES", 1.5, 2.0,
                "I've never been trained in user research; I ask leading questions. Having a simulator point out where my questions trigger confusion helps me learn how to interview properly.",
                "Research coaching and script de-biasing."
            ),
            PersonaEvaluationV4_7(
                "Dr. Aris Thorne", "Head of UX Research @ Enterprise", 0.20,
                "YES", 1.2, 3.0,
                "Now THIS makes methodological sense. We routinely pilot discussion guides. Using synthetic agents as a fast stress-test for question clarity and semantic ambiguity before human field deployment is a legitimate use case.",
                "Legitimate pilot methodology."
            ),
            PersonaEvaluationV4_7(
                "Neha Kapoor", "Niche B2B Product Lead", 0.20,
                "YES", 1.3, 2.2,
                "When I only get one 20-minute call with a hospital CFO, every single question must be laser-sharp. Using simulation as a sparring partner before the call is a no-brainer.",
                "High-stakes interview preparation."
            ),
            PersonaEvaluationV4_7(
                "Liam O'Connor", "VP of Product / CPO", 0.15,
                "YES", 1.0, 3.2,
                "Anything that makes our junior PMs ask better questions and stops them from bringing back garbage qualitative data from customer calls improves decision quality.",
                "Improves qualitative research quality."
            )
        ]
    ))

    # -------------------------------------------------------------------------
    # Q4: Feature Pruning / Backlog Elimination (Killing Bad Ideas Early)
    # -------------------------------------------------------------------------
    questions.append(QuestionContextV4_7(
        question_id="Q4",
        title="Feature Pruning: Fast Friction Scoring vs Subjective RICE Estimation",
        benchmark_source="Product Management Validation Panel (Zoomed - Round 2)",
        ground_truth=50.0,
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=1.9,
        is_status_quo_inertia=True,  # Incumbent habit: RICE spreadsheets with made-up numbers
        evaluations=[
            PersonaEvaluationV4_7(
                "Rachel Vance", "Senior PM @ B2B SaaS", 0.25,
                "YES", 1.3, 2.8,
                "RICE spreadsheets are a joke—PMs just make up 'Confidence' and 'Impact' numbers to justify whatever feature their favorite executive wants. Having objective friction scores kills pet projects fairly.",
                "Replaces politicized RICE spreadsheets."
            ),
            PersonaEvaluationV4_7(
                "Tomás Garcia", "Solo Technical Founder", 0.20,
                "YES", 1.6, 1.8,
                "I have 50 ideas and 1 pair of hands. I need a tool that tells me 'Feature A causes 8.2 friction and negative utility, don't build it'. That saves months of coding.",
                "Prevents coding features that flop."
            ),
            PersonaEvaluationV4_7(
                "Dr. Aris Thorne", "Head of UX Research @ Enterprise", 0.20,
                "NO", -0.7, 5.8,
                "Ranking features by simulated score can create a false sense of certainty. It might weed out obvious blunders, but groundbreaking innovations often score poorly on early adoption models.",
                "Risk of filtering out non-consensus innovation."
            ),
            PersonaEvaluationV4_7(
                "Neha Kapoor", "Niche B2B Product Lead", 0.20,
                "YES", 1.2, 3.0,
                "Every customer asks for custom integrations. Simulating whether the broader persona base would actually adopt it stops us from becoming a bespoke dev shop for one vocal client.",
                "Prevents vocal minority feature creep."
            ),
            PersonaEvaluationV4_7(
                "Liam O'Connor", "VP of Product / CPO", 0.15,
                "YES", 1.4, 2.2,
                "The highest ROI in software is not building faster; it's deciding what NOT to build. If this tool gives my PMs an objective kill-switch for bad features, I will mandate it across all squads.",
                "High executive ROI on not building."
            )
        ]
    ))

    # -------------------------------------------------------------------------
    # Q5: Living Interactive Workspace vs Static Notion/Figma Specs
    # -------------------------------------------------------------------------
    questions.append(QuestionContextV4_7(
        question_id="Q5",
        title="Persona Utility: Interactive Simulation Workspace vs Static Notion Specs",
        benchmark_source="Product Management Validation Panel (Zoomed - Round 2)",
        ground_truth=50.0,
        is_grounded_archetype=False,
        v_0=0.0,
        loss_lambda=1.8,
        is_status_quo_inertia=True,  # Incumbent habit: static Notion documents
        evaluations=[
            PersonaEvaluationV4_7(
                "Rachel Vance", "Senior PM @ B2B SaaS", 0.25,
                "YES", 1.6, 2.0,
                "Static personas in Notion die within 3 months. An interactive workspace where an engineer can type 'Will the accountant persona understand this export dialog?' and get an immediate answer makes personas active.",
                "Brings dead Notion personas to life."
            ),
            PersonaEvaluationV4_7(
                "Tomás Garcia", "Solo Technical Founder", 0.20,
                "YES", 1.5, 1.9,
                "Having a calibrated panel of 5 diverse users permanently available in my browser tab is like having an advisory board on call 24/7.",
                "24/7 advisory board."
            ),
            PersonaEvaluationV4_7(
                "Dr. Aris Thorne", "Head of UX Research @ Enterprise", 0.20,
                "YES", 0.8, 4.0,
                "As long as we can ground the personas with our own interview transcripts and guardrails, an interactive simulator is a powerful dissemination tool to help product managers actually empathize with user friction.",
                "Empathy and alignment tool."
            ),
            PersonaEvaluationV4_7(
                "Neha Kapoor", "Niche B2B Product Lead", 0.20,
                "YES", 1.3, 2.5,
                "Our cross-functional teams constantly misinterpret the target user. Giving everyone a shared interactive workbench eliminates conflicting assumptions.",
                "Shared cross-functional alignment."
            ),
            PersonaEvaluationV4_7(
                "Liam O'Connor", "VP of Product / CPO", 0.15,
                "YES", 1.3, 2.4,
                "I spend \$40k a year on research agencies whose reports sit in Google Drive unread. An interactive tool that developers and PMs actually open every sprint is worth every dollar.",
                "High engagement vs static agency PDFs."
            )
        ]
    ))

    return questions

def run_round2_simulation():
    questions = build_round2_product_questions()

    print("=" * 120)
    print("DOGFOODING SIMULATION — ROUND 2: REFRAMED USE-CASE & PRODUCT-SPECIFIC POSITIONING")
    print("Core Premise: Pre-Flight Micro-Decisions, Price Sensitivity & Dynamic Persona Workspace (NOT Human Replacement)")
    print("Audience: 5 Qualified Zoomed Product Decision-Makers (Rachel, Tomás, Dr. Aris, Neha, Liam)")
    print("Engine: Nobel-Econometric Engine V4.7 (Continuous Consensus + Incumbent Inertia + 95% CI)")
    print("=" * 120 + "\n")

    summary_table = []

    for q in questions:
        res = evaluate_question_v4_7(q)
        pred = res["predicted_rate"]
        ci = res["credible_interval_95"]
        ci_str = f"[{ci[0]:>4.1f}%, {ci[1]:>4.1f}%]"

        verdict = "STRONG ADOPTION (>60%)" if pred >= 60.0 else ("ADOPTION FAVORED (>50%)" if pred >= 50.0 else "RESISTANCE (<50%)")

        print("-" * 120)
        print(f"QUESTION {q.question_id}: {q.title.upper()}")
        print(f"Decision: Option A (Synthetic Tool) vs Option B (Status Quo Incumbent)")
        print(f"Predicted Adoption Rate: {pred:>5.1f}% | 95% Credible Interval: {ci_str} | Verdict: {verdict}")
        print("-" * 120)
        print(f"{'Persona':<18} | {'Stance':<6} | {'P(Adopt)':<8} | {'Net ΔV':<7} | {'Verbatim Quote & Strategic Objection'}")
        print("-" * 120)

        for p in res["persona_logs"]:
            print(f"{p['persona']:<18} | {p['stance']:<6} | {p['score']:>6.1f}% | {p['shift']:>5.2f} | \"{p['response']}\"")
            print(f"{'':<18} | {'':<6} | {'':<8} | {'':<7} | Strategic Benefit: {p['objection']}")
            print()

        summary_table.append({
            "qid": q.question_id,
            "title": q.title,
            "rate": pred,
            "ci": ci_str,
            "verdict": verdict
        })

    print("=" * 120)
    print("ROUND 2 EXECUTIVE COMPARISON: REFRAMED PRODUCT POSITIONING SCORECARD")
    print("=" * 120)
    print(f"{'#':<4} | {'Reframed Product Specific Use-Case':<60} | {'P(Adopt)':<9} | {'95% Credible Interval':<16} | {'Market Verdict'}")
    print("-" * 120)
    for row in summary_table:
        print(f"{row['qid']:<4} | {row['title']:<60} | {row['rate']:>7.1f}% | {row['ci']:<16} | {row['verdict']}")
    print("=" * 120 + "\n")

if __name__ == "__main__":
    run_round2_simulation()
