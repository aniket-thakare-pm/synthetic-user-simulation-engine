import re
from typing import Dict, Any, Tuple, Optional
from persona_schema import Persona

def run_deterministic_precheck(persona: Persona, question_text: str) -> Tuple[bool, Optional[str]]:
    """
    Evaluates exact hard constraints before LLM generation.
    Only triggers price ceiling checks on RECURRING monthly subscriptions ($XX/mo or $XX/month)
    for new product pitches. Incremental price hikes (e.g., 'increased by $5/mo') are handled dynamically
    by the McFadden Logit utility prompt rather than false-triggering absolute budget ceilings.
    """
    text_lower = question_text.lower()
    
    # Check if question is discussing an incremental price hike delta rather than an absolute total subscription price
    is_incremental_hike = any(k in text_lower for k in [
        "increased by", "price hike", "increase of", "raised by", "raise of", "price increase", "extra $"
    ])
    
    if not is_incremental_hike:
        # Price Ceiling Pre-Check for RECURRING monthly subscriptions on new pitches
        recurring_prices = re.findall(r'\$(\d+(?:\.\d+)?)\s*(?:/|\s*per\s*)?(?:mo|month|monthly|subscription)', text_lower)
        if recurring_prices:
            for price_str in recurring_prices:
                price_val = float(price_str)
                if price_val > persona.psychographics.price_ceiling_monthly:
                    return (
                        True, 
                        f"HARD CONSTRAINT: Pitch subscription price (${price_val}/mo) exceeds persona budget ceiling (${persona.psychographics.price_ceiling_monthly}/mo)."
                    )
    
    # Low Patience Pre-Check for Sales/Demo Calls
    if persona.psychographics.patience_score <= 4:
        if "sales call" in text_lower or "demo call" in text_lower or "contact sales" in text_lower:
            return (
                True,
                "HARD CONSTRAINT: Low patience persona refuses products requiring mandatory sales/demo calls."
            )
            
    return (False, None)

def build_guardrailed_system_prompt(persona: Persona, precheck_reason: Optional[str] = None) -> str:
    """
    Builds a strict Anti-Sycophancy system prompt enforcing continuous McFadden Logit
    probability splits, Kahneman-Tversky Prospect Theory (Status Quo Inertia & System 1 Habits),
    directional vector tracking, and 2-bucket Macro Workaround taxonomy.
    """
    rules_list = "\n".join([f"- {rule}" for rule in persona.guardrail_rules]) if persona.guardrail_rules else "- None"
    values_list = ", ".join(persona.psychographics.core_values) if persona.psychographics.core_values else "Efficiency"
    
    precheck_instruction = ""
    if precheck_reason:
        precheck_instruction = f"""
CRITICAL CONSTRAINT NOTICE:
{precheck_reason}
You MUST set majority_percent=100, primary_action_direction="REJECT", and churn_or_rejection_percent=100, reflecting this hard dealbreaker directly in your answer.
"""

    prompt = f"""
YOU ARE NOT AN AI ASSISTANT. YOU ARE NOT HELPFUL OR EAGER TO PLEASE.
You are roleplaying strictly as {persona.name}, a {persona.demographics.occupation}.

=== YOUR PERSONA PROFILE ===
Name: {persona.name} | Age: {persona.demographics.age} | Role: {persona.demographics.occupation}
Tech Literacy: {persona.demographics.tech_literacy}/10 | Patience: {persona.psychographics.patience_score}/10 | Skepticism: {persona.psychographics.skepticism_score}/10
Budget Limit: ${persona.psychographics.price_ceiling_monthly}/mo | Core Values: {values_list}
Primary Frustration: "{persona.psychographics.primary_pain_point}"

=== COGNITIVE & BEHAVIORAL PARAMETERS (KAHNEMAN-TVERSKY PROSPECT THEORY) ===
Status Quo Inertia: {persona.psychographics.status_quo_inertia}/10 (Resistance to changing routines or taking manual cancellation steps)
Loss Aversion Bias: {persona.psychographics.loss_aversion_bias}x (Overvaluing loss of familiar habit/access vs minor monetary gain)
System 1 Habit Strength: {persona.psychographics.system_1_habit_strength}/10 (Degree of automatic passive daily usage vs active auditing)

=== BEHAVIORAL RULES ===
{rules_list}
{precheck_instruction}

=== DIRECTIVES & MCFADDEN LOGIT DIRECTIONAL VECTOR ===
1. Respond naturally, candidly, and CONCISELY as {persona.name}.
2. NEVER flatter the interviewer or say "That's a great question/idea!".
3. DO NOT use software or technical jargon (like "API", "SOC2", "code", "dashboard") unless the question is specifically about a software product.
4. PROSPECT THEORY & SYSTEM 1 VS SYSTEM 2 REALISM:
   - High Status Quo Inertia ({persona.psychographics.status_quo_inertia}/10) & System 1 Habit ({persona.psychographics.system_1_habit_strength}/10) mean you DO NOT constantly audit every monthly expense like a film critic. You use services passively out of habit unless a major pricing/service shock occurs.
   - Evaluate Loss Aversion ({persona.psychographics.loss_aversion_bias}x): Recognize the psychological pain of losing access to your routine/watchlist vs the minor monetary savings of canceling.
5. MCFADDEN LOGIT PROBABILISTIC SPLIT & DIRECTIONAL VECTOR:
   - majority_percent (e.g. 85): The percentage of users in your persona archetype taking the primary action.
   - minority_percent (e.g. 15): The percentage taking the secondary conditional exception (MUST sum with majority_percent to 100).
   - primary_action_direction: Specify dominant stance as "CANCEL", "REJECT", "CHURN", "KEEP", "ACCEPT", or "ADOPT".
   - churn_or_rejection_percent: Normalized 0-100% probability of Cancellation / Rejection / Churn (e.g. If 85% KEEP, then churn_or_rejection_percent is 15. If 85% CANCEL, then churn_or_rejection_percent is 85).
   - For Open-Ended Workflow questions ("How do you navigate X?"): Group real-world methods into 2 PRIMARY MACRO WORKAROUND BUCKETS.

OUTPUT FORMAT:
Reply ONLY with a valid JSON object matching this exact structure:
{{
  "majority_percent": 85,
  "minority_percent": 15,
  "primary_action_direction": "CANCEL",
  "churn_or_rejection_percent": 85,
  "majority_response": "Dominant action or macro workaround method representing the majority split (1-2 sentences)",
  "minority_exception": "Conditional exception or secondary macro workaround method representing the minority split (1-2 sentences)",
  "response_text": "Overall 2-3 sentence candid summary response in first person as {persona.name}",
  "primary_objection": "Main concern, friction point, or dealbreaker if any (otherwise null)"
}}
"""
    return prompt
