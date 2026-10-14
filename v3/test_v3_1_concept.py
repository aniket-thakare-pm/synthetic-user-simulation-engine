import sys
import os
import json
import math

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
sys.stdout.reconfigure(encoding='utf-8')

from v3.category_schema_v3 import detect_or_resolve_category
from v3.sample_personas_v3 import SAMPLE_PERSONAS_V3
from interview_engine import call_llm_api, load_env_key

key = load_env_key()
sarah = SAMPLE_PERSONAS_V3[0] # Sarah Jenkins

q_text = "When shopping online, would you abandon your order if the store forces you to create an account before completing checkout?"
account = detect_or_resolve_category(q_text, api_key=key)

prompt = f"""
You are roleplaying as {sarah.name}, a {sarah.demographics.occupation}.
Category: {account.display_name}
{account.context_directive}

Question: "{q_text}"

Evaluate these two choices:
• ACTION A: Abandon your shopping cart and leave without the item.
• BASELINE B: Create the account, complete checkout, and get the item you spent time finding.

Rate:
1. v_action_a (1-10): Objective utility of abandoning and leaving empty-handed
2. v_baseline_b (1-10): Objective utility of creating the account and receiving your item
3. switching_friction (1-10): Friction of the account setup
4. decision_stance: "YES" if you choose Action A (abandon), "NO" if you choose Baseline B (complete order).

Reply ONLY in JSON:
{{"decision_stance": "NO", "v_action_a": 3.0, "v_baseline_b": 7.0, "switching_friction": 4.0, "reason": "..."}}
"""

res = call_llm_api(key, prompt, q_text)
print("Sarah on Baymard Q2:", json.dumps(res, indent=2))

v_a = float(res.get("v_action_a", 3.0))
v_b = float(res.get("v_baseline_b", 7.0))
fric = float(res.get("switching_friction", 4.0))
loss_mult = sarah.psychographics.loss_aversion_bias
delta_v = (v_a - v_b) - ((fric / 10.0) * loss_mult)
p_abandon = (1.0 / (1.0 + math.exp(-0.32 * delta_v))) * 100.0
p_abandon = max(10.0, min(90.0, p_abandon))
print(f"\nΔV = ({v_a} - {v_b}) - ({fric}/10 * {loss_mult}) = {delta_v:.2f}")
print(f"Computed Abandonment Probability P(Abandon): {p_abandon:.1f}%")
print(f"Empirical Ground Truth: 25.0%")
