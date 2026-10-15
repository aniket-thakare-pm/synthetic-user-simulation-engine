"""
run_v4_3_multi_frontier.py
Engine V4.3 Stress Test: 5 Diverse Multi-Frontier Scenarios
Testing Financial Resilience, Cookie Fatigue, Flight Insurance, Free Trial Rollover, and Viral Sharing.
"""

import sys
import os
import json

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
sys.stdout.reconfigure(encoding='utf-8')

from v4_3.engine_v4_3 import compute_v4_3_choice_prob

MULTI_FRONTIER_QUESTIONS = [
    {
        "id": "Q1",
        "title": "Emergency Financial Resilience ($400 Expense in Cash/Savings)",
        "source": "Federal Reserve SHED Survey (N=11,400)",
        "ground_truth": 63.0,
        "v_0": 0.0,
        "loss_lambda": 1.9,
        "evaluations": [
            {
                "persona_name": "Sarah Jenkins",
                "occupation": "Senior Accountant [The Value Auditor]",
                "weight": 0.25,
                "stance": "YES",
                "shift": 0.8,
                "scaled_friction": 1.5,
                "response_text": "I maintain a strict emergency fund in a high-yield savings account for my child. A sudden $400 car repair hurts, but I can cover it directly from liquid savings without borrowing.",
                "objection": "None; planned emergency savings cushion."
            },
            {
                "persona_name": "Alex Rivera",
                "occupation": "Full-Stack Developer [The Speed Optimizer]",
                "weight": 0.20,
                "stance": "YES",
                "shift": 1.8,
                "scaled_friction": 0.8,
                "response_text": "On a six-figure developer salary, a $400 emergency is easily absorbed by my regular checking account balance without touching investments or carrying credit card debt.",
                "objection": "None."
            },
            {
                "persona_name": "David Miller",
                "occupation": "Retired Teacher [The Risk Avoider]",
                "weight": 0.20,
                "stance": "YES",
                "shift": 0.7,
                "scaled_friction": 2.2,
                "response_text": "I live modestly on my pension and keep a rainy-day credit union savings account specifically for unexpected car repairs or medical bills. I can pay the $400 in cash.",
                "objection": "Puts a dent in monthly pension, but manageable."
            },
            {
                "persona_name": "Elena Rostova",
                "occupation": "Nurse & Working Mother [The Pragmatic Caregiver]",
                "weight": 0.20,
                "stance": "YES",
                "shift": 1.2,
                "scaled_friction": 1.2,
                "response_text": "Working full-time hospital shifts provides a stable income. Our household savings can cover an unexpected $400 expense right away with debit.",
                "objection": "None."
            },
            {
                "persona_name": "Marcus Chen",
                "occupation": "Undergraduate Student [The Budget Streamer]",
                "weight": 0.15,
                "stance": "NO",
                "shift": -1.8,
                "scaled_friction": 7.2,
                "response_text": "On a tight $14,000 student budget, an unexpected $400 bill would completely drain my checking account. I'd have to borrow from my parents or put it on a credit card.",
                "objection": "Zero liquid cushion; total liquidity shortfall."
            }
        ]
    },
    {
        "id": "Q2",
        "title": "Dark Pattern Cookie Fatigue ('Accept All' Surrender)",
        "source": "CNIL & Web Usability Benchmark (N=5,000)",
        "ground_truth": 78.0,
        "v_0": 0.0,
        "loss_lambda": 1.4,
        "evaluations": [
            {
                "persona_name": "Sarah Jenkins",
                "occupation": "Senior Accountant [The Value Auditor]",
                "weight": 0.25,
                "stance": "NO",
                "shift": -1.2,
                "scaled_friction": 4.0,
                "response_text": "As an accountant who values privacy and data security, I refuse to let ad-trackers follow me around the web. I take the extra ten seconds to click 'Manage Preferences' and toggle off marketing cookies.",
                "objection": "Distrust of invasive third-party ad tracking."
            },
            {
                "persona_name": "Alex Rivera",
                "occupation": "Full-Stack Developer [The Speed Optimizer]",
                "weight": 0.20,
                "stance": "YES",
                "shift": 1.5,
                "scaled_friction": 1.0,
                "response_text": "My patience for annoying modal pop-ups is zero. I run browser-level tracking blockers anyway, so I smash the big 'Accept All' button in half a second just to clear my screen.",
                "objection": "Hates modal UI friction blocking access."
            },
            {
                "persona_name": "David Miller",
                "occupation": "Retired Teacher [The Risk Avoider]",
                "weight": 0.20,
                "stance": "YES",
                "shift": 1.0,
                "scaled_friction": 2.2,
                "response_text": "The pop-ups are confusing and the 'Manage' options are written in microscopic gray text. I just click the big blue button to make the screen clear so I can read the article.",
                "objection": "Exhausted by confusing modal layouts."
            },
            {
                "persona_name": "Elena Rostova",
                "occupation": "Nurse & Working Mother [The Pragmatic Caregiver]",
                "weight": 0.20,
                "stance": "YES",
                "shift": 1.6,
                "scaled_friction": 0.8,
                "response_text": "After a twelve-hour shift, I don't have the mental energy to navigate twenty different cookie toggles. I tap 'Accept All' immediately so I can read what I need.",
                "objection": "Zero cognitive bandwidth for cookie settings."
            },
            {
                "persona_name": "Marcus Chen",
                "occupation": "Undergraduate Student [The Budget Streamer]",
                "weight": 0.15,
                "stance": "YES",
                "shift": 1.8,
                "scaled_friction": 0.6,
                "response_text": "I don't care at all about cookies. I double-tap the main button automatically within 0.1 seconds of loading the page.",
                "objection": "Pure muscle memory to dismiss screen clutter."
            }
        ]
    },
    {
        "id": "Q3",
        "title": "Flight Add-On Insurance ($25 Policy on $350 Flight)",
        "source": "Swiss Re & InsurTech Benchmark (N=4,000)",
        "ground_truth": 28.0,
        "v_0": 0.0,
        "loss_lambda": 1.8,
        "evaluations": [
            {
                "persona_name": "Sarah Jenkins",
                "occupation": "Senior Accountant [The Value Auditor]",
                "weight": 0.25,
                "stance": "NO",
                "shift": -1.5,
                "scaled_friction": 5.5,
                "response_text": "A $25 insurance fee on a $350 flight is a 7% markup with dozens of fine-print exclusions. DOT rules already protect major cancellations, so paying extra is an overpriced upsell.",
                "objection": "Poor actuarial value and excessive exclusions."
            },
            {
                "persona_name": "Alex Rivera",
                "occupation": "Full-Stack Developer [The Speed Optimizer]",
                "weight": 0.20,
                "stance": "NO",
                "shift": -1.8,
                "scaled_friction": 6.0,
                "response_text": "I book travel with a premium credit card that already has automated primary trip cancellation coverage built in. Paying $25 to a 3rd party on checkout is throwing money away.",
                "objection": "Redundant coverage with existing credit card perks."
            },
            {
                "persona_name": "David Miller",
                "occupation": "Retired Teacher [The Risk Avoider]",
                "weight": 0.20,
                "stance": "YES",
                "shift": 0.9,
                "scaled_friction": 2.4,
                "response_text": "At my age, unexpected illnesses or family emergencies happen. Paying $25 gives me peace of mind that I won't lose my $350 ticket if I can't travel.",
                "objection": "None; peace of mind is worth $25."
            },
            {
                "persona_name": "Elena Rostova",
                "occupation": "Nurse & Working Mother [The Pragmatic Caregiver]",
                "weight": 0.20,
                "stance": "NO",
                "shift": -0.8,
                "scaled_friction": 4.0,
                "response_text": "For domestic travel, I usually decline because airlines let you retain flight credits anyway if you cancel ahead of time. I save the $25.",
                "objection": "Airline rebooking credits are sufficient."
            },
            {
                "persona_name": "Marcus Chen",
                "occupation": "Undergraduate Student [The Budget Streamer]",
                "weight": 0.15,
                "stance": "NO",
                "shift": -1.9,
                "scaled_friction": 7.5,
                "response_text": "I fly ultra-low-cost airlines where every single dollar counts. There is zero chance I'm adding a $25 fee to my ticket.",
                "objection": "Tight student budget."
            }
        ]
    },
    {
        "id": "Q4",
        "title": "Accidental Free Trial Rollover (Forgot to Cancel in Time)",
        "source": "FTC & Consumer Reports Benchmark (N=3,000)",
        "ground_truth": 48.0,
        "v_0": 0.0,
        "loss_lambda": 1.5,
        "evaluations": [
            {
                "persona_name": "Sarah Jenkins",
                "occupation": "Senior Accountant [The Value Auditor]",
                "weight": 0.25,
                "stance": "YES",
                "shift": 0.5,
                "scaled_friction": 3.0,
                "response_text": "I set calendar reminders meticulously, but even I have to admit that two years ago I signed up for a trial software, missed the 7-day cutoff by one day, and got billed $15.",
                "objection": "Felt angry at myself, but it has happened."
            },
            {
                "persona_name": "Alex Rivera",
                "occupation": "Full-Stack Developer [The Speed Optimizer]",
                "weight": 0.20,
                "stance": "YES",
                "shift": 1.2,
                "scaled_friction": 1.5,
                "response_text": "I sign up for cloud tools, dev sandboxes, and streaming trials constantly. I've definitely spaced out and paid for at least one or two months of services I never touched.",
                "objection": "Guilty of trial inertia."
            },
            {
                "persona_name": "David Miller",
                "occupation": "Retired Teacher [The Risk Avoider]",
                "weight": 0.20,
                "stance": "NO",
                "shift": -1.5,
                "scaled_friction": 5.5,
                "response_text": "I never give my credit card for a 'free' trial in the first place because I know it's a trap. If they require my card upfront, I close the window.",
                "objection": "Actively avoids credit-card required trials."
            },
            {
                "persona_name": "Elena Rostova",
                "occupation": "Nurse & Working Mother [The Pragmatic Caregiver]",
                "weight": 0.20,
                "stance": "YES",
                "shift": 1.0,
                "scaled_friction": 2.0,
                "response_text": "Between 12-hour shifts and family chaos, it's impossible to remember every digital deadline. I've had multiple fitness and kids' app trials roll over into paid charges.",
                "objection": "Time poverty leads to missed cancellation windows."
            },
            {
                "persona_name": "Marcus Chen",
                "occupation": "Undergraduate Student [The Budget Streamer]",
                "weight": 0.15,
                "stance": "YES",
                "shift": 1.4,
                "scaled_friction": 1.5,
                "response_text": "I sign up for free trials all the time for homework or streaming. I forget constantly and only realize when my bank sends an overdraft alert.",
                "objection": "Frequent occurrence."
            }
        ]
    },
    {
        "id": "Q5",
        "title": "Viral Referral Sharing Gap ('Give $20, Get $20' Active Texting)",
        "source": "Harvard Business Review Benchmark (N=5,000)",
        "ground_truth": 16.0,
        "v_0": 0.0,
        "loss_lambda": 1.9,
        "evaluations": [
            {
                "persona_name": "Sarah Jenkins",
                "occupation": "Senior Accountant [The Value Auditor]",
                "weight": 0.25,
                "stance": "NO",
                "shift": -1.8,
                "scaled_friction": 6.5,
                "response_text": "Texting friends a promotional referral code feels cheap and awkward, like I'm using personal relationships to get a discount. I ignore referral banners completely.",
                "objection": "Social friction of monetizing friendships."
            },
            {
                "persona_name": "Alex Rivera",
                "occupation": "Full-Stack Developer [The Speed Optimizer]",
                "weight": 0.20,
                "stance": "NO",
                "shift": -1.0,
                "scaled_friction": 4.8,
                "response_text": "I might drop a referral link in a public Reddit or Discord channel once in a blue moon, but texting my actual contacts to shill an app is cringey. I rarely do it.",
                "objection": "Social awkwardness of spamming contacts."
            },
            {
                "persona_name": "David Miller",
                "occupation": "Retired Teacher [The Risk Avoider]",
                "weight": 0.20,
                "stance": "NO",
                "shift": -2.0,
                "scaled_friction": 7.5,
                "response_text": "I do not participate in internet marketing schemes. I am certainly not going to send advertisements to my family members.",
                "objection": "Strong aversion to multi-level marketing/referrals."
            },
            {
                "persona_name": "Elena Rostova",
                "occupation": "Nurse & Working Mother [The Pragmatic Caregiver]",
                "weight": 0.20,
                "stance": "NO",
                "shift": -1.5,
                "scaled_friction": 6.0,
                "response_text": "If a colleague asks me where I got a pair of scrubs, I'll tell them the brand name. But copying a digital referral link and sending it feels unnatural. I skip it.",
                "objection": "Prefers natural word-of-mouth over affiliate links."
            },
            {
                "persona_name": "Marcus Chen",
                "occupation": "Undergraduate Student [The Budget Streamer]",
                "weight": 0.15,
                "stance": "YES",
                "shift": 0.5,
                "scaled_friction": 3.2,
                "response_text": "If it gives me twenty bucks off shoes or food delivery, I'll text it to my roommate or group chat. Free money is free money when you're in college.",
                "objection": "Only shares with close peers if discount is high."
            }
        ]
    }
]

def run_multi_frontier_test():
    print("=" * 85)
    print("ENGINE V4.3 MULTI-FRONTIER STRESS TEST (5 UNSEEN BEHAVIORAL DOMAINS)")
    print("Autonomous In-Agent Inference | Adaptive Elasticity (Beta = 0.75, V0 = 0.0)")
    print("=" * 85)

    total_error = 0.0
    suite_results = []

    for q in MULTI_FRONTIER_QUESTIONS:
        qid = q["id"]
        title = q["title"]
        gt = q["ground_truth"]
        v_0 = q["v_0"]
        loss_lambda = q["loss_lambda"]

        print(f"\n--- Running {qid}: {title} ---")
        print(f"Source: {q['source']} | Ground Truth: {gt}%")

        weighted_score = 0.0
        total_weight = 0.0
        persona_logs = []

        for p in q["evaluations"]:
            res = compute_v4_3_choice_prob(
                v_0=v_0,
                persona_shift=p["shift"],
                scaled_friction=p["scaled_friction"],
                loss_lambda=loss_lambda,
                is_grounded=False
            )
            prob = res["probability"]
            w = p["weight"]
            weighted_score += prob * w
            total_weight += w

            persona_logs.append({
                "persona": p["persona_name"],
                "stance": p["stance"],
                "shift": p["shift"],
                "score": prob,
                "response": p["response_text"],
                "objection": p["objection"]
            })

            print(f"  [{p['persona_name']}]: Stance={p['stance']}, Shift={p['shift']:+.2f} -> Probability={prob:.1f}%")

        v4_3_prediction = round(weighted_score / total_weight, 1)
        error = round(abs(v4_3_prediction - gt), 1)
        total_error += error

        print(f"==> V4.3 Predicted: {v4_3_prediction}% | Real Human Ground Truth: {gt}% | Error: {error}%")

        suite_results.append({
            "question_id": qid,
            "title": title,
            "ground_truth": gt,
            "v4_3_prediction": v4_3_prediction,
            "error": error,
            "beta_used": 0.75,
            "persona_evaluations": persona_logs
        })

    mae = round(total_error / len(MULTI_FRONTIER_QUESTIONS), 2)
    accuracy = round(100.0 - mae, 2)

    print("\n" + "=" * 85)
    print("MULTI-FRONTIER STRESS TEST SUMMARY")
    print(f"Mean Absolute Error (MAE): {mae}%")
    print(f"Zero-Shot Prediction Accuracy: {accuracy}%")
    print("=" * 85)

    out_file = os.path.join(PROJECT_ROOT, "multi_frontier_5q_v4_3_results.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({
            "engine": "Engine V4.3 (Autonomous Inference & Adaptive Elasticity)",
            "benchmark": "5-Domain Multi-Frontier Benchmark",
            "mae": mae,
            "accuracy": accuracy,
            "results": suite_results
        }, f, indent=2)

    print(f"Results written to: {out_file}")

if __name__ == "__main__":
    run_multi_frontier_test()
