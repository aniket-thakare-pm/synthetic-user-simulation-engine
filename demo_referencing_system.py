import sys
import os
import json

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
sys.stdout.reconfigure(encoding='utf-8')

from v3.engine_v3_1 import build_prompt_v3_1, compute_mental_accounting_friction
from v3.sample_personas_v3 import SAMPLE_PERSONAS_V3
from v3.indian_personas_v3 import INDIAN_PERSONAS_V3
from v3.category_schema_v3 import detect_or_resolve_category
from v3.cognitive_reference_engine import detect_cognitive_reference
from interview_engine import call_llm_api, load_env_key

GEMINI_KEY = os.environ.get("GEMINI_API_KEY") or load_env_key()

print("=" * 90)
print(" 🔬 DEMONSTRATION: IS THE COGNITIVE REFERENCING SYSTEM WORKING?")
print("=" * 90)

# 1. TEST US PERSONA: Sarah Jenkins on Slow Delivery (E-Commerce)
q_us = {
    "text": "When shopping online, would you abandon your order if estimated delivery speed is too slow or delivery time is not clearly displayed before payment?",
    "action_a": "Abandon your order and look elsewhere / leave without buying",
    "baseline_b": "Accept the slower/unclear shipping and complete checkout to get the item",
    "category": "ECOMMERCE_CHECKOUT_AND_RETAIL"
}

account_us = detect_or_resolve_category(q_us["text"], explicit_category=q_us["category"], api_key=GEMINI_KEY)
cog_us = detect_cognitive_reference(q_us["text"], q_us["category"])

print(f"\n[Case 1: US Persona - Sarah Jenkins]")
print(f"Question: \"{q_us['text'][:80]}...\"")
print(f"Referenced Archetype from Psych-101: {cog_us.display_name}")
print(f"Empirical Anchor Injected:\n>>> {cog_us.anchor_directive.strip()} <<<\n")

# Prompt with Anchor
base_prompt = build_prompt_v3_1(SAMPLE_PERSONAS_V3[0], q_us["text"], q_us["action_a"], q_us["baseline_b"], account_us)
anchored_prompt = base_prompt.replace(
    "=== REAL-WORLD OUTCOME VALUATION",
    f"=== EMPIRICAL BEHAVIORAL GROUNDING (Psych-101 Reference) ===\n{cog_us.anchor_directive}\n\n=== REAL-WORLD OUTCOME VALUATION"
)

resp_anchored = call_llm_api(GEMINI_KEY, anchored_prompt, q_us["text"])
va = float(resp_anchored.get("v_action_a", 5.0))
vb = float(resp_anchored.get("v_baseline_b", 5.0))
f_eff, _ = compute_mental_accounting_friction(SAMPLE_PERSONAS_V3[0], account_us, float(resp_anchored.get("switching_friction", 3.0)))
delta_v = (va - vb) - ((f_eff / 10.0) * cog_us.loss_aversion_lambda)
import math
prob_anchored = round((1.0 / (1.0 + math.exp(-0.32 * delta_v))) * 100.0, 1)

print(f"Result WITH Psych-101 Reference Anchor:")
print(f"  • Stance: {resp_anchored.get('decision_stance')} | V_A (Abandon): {va} | V_B (Complete): {vb} | ΔV: {delta_v:.2f}")
print(f"  • Computed Abandonment Probability: {prob_anchored}% (Real Human Ground Truth: 23.0%)")
print(f"  • Sarah's Reasoning: \"{resp_anchored.get('response_text')}\"")

# 2. TEST INDIAN PERSONA: Suresh Verma on Telemedicine
q_in = {
    "text": "Would you consult a certified doctor over a scheduled video call on a smartphone app instead of physically visiting a local neighborhood clinic for common health issues?",
    "action_a": "Consult a certified doctor over scheduled video call on a smartphone app",
    "baseline_b": "Physically visit a local neighborhood clinic for common health issues",
    "category": "HEALTH_AND_DIAGNOSTICS"
}

account_in = detect_or_resolve_category(q_in["text"], explicit_category=q_in["category"], api_key=GEMINI_KEY)
cog_in = detect_cognitive_reference(q_in["text"], q_in["category"])

print(f"\n" + "-" * 90)
print(f"[Case 2: Indian Persona - Suresh Verma (Retired Bank Clerk, Bhopal)]")
print(f"Question: \"{q_in['text'][:80]}...\"")
print(f"Referenced Archetype from Psych-101: {cog_in.display_name}")
print(f"Empirical Anchor Injected:\n>>> {cog_in.anchor_directive.strip()} <<<\n")

base_prompt_in = build_prompt_v3_1(INDIAN_PERSONAS_V3[3], q_in["text"], q_in["action_a"], q_in["baseline_b"], account_in)
anchored_prompt_in = base_prompt_in.replace(
    "=== REAL-WORLD OUTCOME VALUATION",
    f"=== EMPIRICAL BEHAVIORAL GROUNDING (Psych-101 Reference) ===\n{cog_in.anchor_directive}\n\n=== REAL-WORLD OUTCOME VALUATION"
)

resp_in = call_llm_api(GEMINI_KEY, anchored_prompt_in, q_in["text"])
va_in = float(resp_in.get("v_action_a", 5.0))
vb_in = float(resp_in.get("v_baseline_b", 5.0))
f_eff_in, _ = compute_mental_accounting_friction(INDIAN_PERSONAS_V3[3], account_in, float(resp_in.get("switching_friction", 3.0)))
delta_v_in = (va_in - vb_in) - ((f_eff_in / 10.0) * cog_in.loss_aversion_lambda)
prob_in = round((1.0 / (1.0 + math.exp(-0.32 * delta_v_in))) * 100.0, 1)

print(f"Result WITH Psych-101 Reference Anchor:")
print(f"  • Stance: {resp_in.get('decision_stance')} | V_A (Video Doctor): {va_in} | V_B (Physical Clinic): {vb_in} | ΔV: {delta_v_in:.2f}")
print(f"  • Computed Adoption Probability: {prob_in}% (Real Human Ground Truth: 15-20% for conservative elderly)")
print(f"  • Suresh's Reasoning: \"{resp_in.get('response_text')}\"")
