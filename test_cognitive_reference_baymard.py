import sys
import os
import json

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
sys.stdout.reconfigure(encoding='utf-8')

from v3.engine_v3_1 import interview_persona_v3_1, build_prompt_v3_1, compute_mental_accounting_friction, derive_action_and_baseline
from v3.sample_personas_v3 import SAMPLE_PERSONAS_V3
from v3.category_schema_v3 import detect_or_resolve_category
from v3.cognitive_reference_engine import detect_cognitive_reference
from interview_engine import call_llm_api, load_env_key

GEMINI_KEY = os.environ.get("GEMINI_API_KEY") or load_env_key()

TEST_QUESTIONS = [
    {
        "id": "Q3",
        "title": "Slow / Unclear Delivery Speeds",
        "category": "ECOMMERCE_CHECKOUT_AND_RETAIL",
        "text": "When shopping online, would you abandon your order if estimated delivery speed is too slow or delivery time is not clearly displayed before payment?",
        "action_a": "Abandon your order and look elsewhere / leave without buying",
        "baseline_b": "Accept the slower/unclear shipping and complete checkout to get the item",
        "ground_truth": 23.0,
        "v3_1_score": 53.5
    },
    {
        "id": "Q4",
        "title": "Customer Reviews & Star Ratings Reliance",
        "category": "ECOMMERCE_CHECKOUT_AND_RETAIL",
        "text": "When considering a purchase on an e-commerce platform, do you actively check customer reviews and star ratings before deciding to buy?",
        "action_a": "Actively check customer reviews and star ratings before buying",
        "baseline_b": "Buy directly based on images/product description without checking reviews",
        "ground_truth": 75.0,
        "v3_1_score": 58.4
    },
    {
        "id": "Q5",
        "title": "Strict / Friction Return Policy",
        "category": "ECOMMERCE_CHECKOUT_AND_RETAIL",
        "text": "When shopping online, would you abandon your order if the return policy is strict, short (e.g. under 14 days), or requires you to pay return shipping?",
        "action_a": "Abandon your order and do not buy from this store",
        "baseline_b": "Accept the strict return policy risk and complete the purchase",
        "ground_truth": 18.0,
        "v3_1_score": 47.3
    }
]

def interview_with_cognitive_anchor(persona, q, api_key):
    account = detect_or_resolve_category(q["text"], explicit_category=q["category"], api_key=api_key)
    action_a = q["action_a"]
    baseline_b = q["baseline_b"]
    cog_ref = detect_cognitive_reference(q["text"], category=q["category"])

    base_prompt = build_prompt_v3_1(persona, q["text"], action_a, baseline_b, account)
    
    # Inject Cognitive Anchor into prompt
    enhanced_prompt = base_prompt.replace(
        "=== REAL-WORLD OUTCOME VALUATION",
        f"=== EMPIRICAL BEHAVIORAL GROUNDING (Psych-101 Benchmark) ===\n{cog_ref.anchor_directive}\n\n=== REAL-WORLD OUTCOME VALUATION"
    )

    json_output = call_llm_api(api_key, enhanced_prompt, q["text"])
    stance = str(json_output.get("decision_stance", "NO")).upper().strip()
    v_a = float(json_output.get("v_action_a", 5.0))
    v_b = float(json_output.get("v_baseline_b", 5.0))
    switch_f = float(json_output.get("switching_friction", 3.0))

    f_eff, _ = compute_mental_accounting_friction(persona, account, switch_f)
    
    # Use empirical lambda from Psych-101 reference
    lambda_loss = cog_ref.loss_aversion_lambda
    delta_v = (v_a - v_b) - ((f_eff / 10.0) * lambda_loss)

    import math
    prob = 1.0 / (1.0 + math.exp(-0.32 * delta_v))
    action_rate = round(prob * 100.0, 1)

    return action_rate, v_a, v_b, f_eff, delta_v, json_output.get("response_text", "")

print("=" * 80)
print(" 🔬 TESTING COGNITIVE REFERENCE ENGINE ON PREVIOUS BAYMARD OUTLIERS")
print("=" * 80)

for q in TEST_QUESTIONS:
    print(f"\n📋 Evaluating {q['id']}: {q['title']}")
    print(f"   Ground Truth: {q['ground_truth']}% | V3.1 Score: {q['v3_1_score']}%")
    cog = detect_cognitive_reference(q["text"], q["category"])
    print(f"   [Anchor Assigned: {cog.display_name} (Lambda={cog.loss_aversion_lambda})]")
    
    weighted_sum = 0.0
    for p in SAMPLE_PERSONAS_V3:
        rate, va, vb, feff, dv, reason = interview_with_cognitive_anchor(p, q, GEMINI_KEY)
        weighted_sum += rate * p.population_weight
        print(f"   • {p.name} (w={p.population_weight}): V_A={va} vs V_B={vb} -> Score={rate}%")
    
    print(f"   🎯 Calibrated Score: {weighted_sum:.1f}% (Ground Truth: {q['ground_truth']}%)")
    print(f"   📐 Error: {abs(weighted_sum - q['ground_truth']):.1f}% (vs V3.1 Error: {abs(q['v3_1_score'] - q['ground_truth']):.1f}%)")
