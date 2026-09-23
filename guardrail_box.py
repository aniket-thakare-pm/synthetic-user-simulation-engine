import re
from typing import Dict, Any, Tuple, Optional
from persona_schema import Persona

def run_deterministic_precheck(persona: Persona, question_text: str) -> Tuple[bool, Optional[str]]:
    """
    Evaluates exact hard constraints before LLM generation.
    Returns (auto_rejected: bool, reason: str)
    """
    text_lower = question_text.lower()
    
    # 1. Price Ceiling Pre-Check
    prices = re.findall(r'\$(\d+(?:\.\d+)?)', question_text)
    if prices:
        for price_str in prices:
            price_val = float(price_str)
            if price_val > persona.psychographics.price_ceiling_monthly:
                return (
                    True, 
                    f"HARD CONSTRAINT: Pitch price (${price_val}/mo) exceeds persona budget ceiling (${persona.psychographics.price_ceiling_monthly}/mo)."
                )
    
    # 2. Low Patience Pre-Check
    if persona.psychographics.patience_score <= 4:
        if "sales call" in text_lower or "demo call" in text_lower or "contact sales" in text_lower:
            return (
                True,
                "HARD CONSTRAINT: Low patience persona refuses products requiring mandatory sales/demo calls."
            )
            
    return (False, None)

def build_guardrailed_system_prompt(persona: Persona, precheck_reason: Optional[str] = None) -> str:
    """
    Builds a strict Anti-Sycophancy system prompt for concise, single-response answers.
    """
    rules_list = "\n".join([f"- {rule}" for rule in persona.guardrail_rules]) if persona.guardrail_rules else "- None"
    values_list = ", ".join(persona.psychographics.core_values) if persona.psychographics.core_values else "Efficiency"
    
    precheck_instruction = ""
    if precheck_reason:
        precheck_instruction = f"""
CRITICAL CONSTRAINT NOTICE:
{precheck_reason}
You MUST reflect this dealbreaker directly in your answer.
"""

    prompt = f"""
YOU ARE NOT AN AI ASSISTANT. YOU ARE NOT HELPFUL OR EAGER TO PLEASE.
You are roleplaying strictly as {persona.name}, a {persona.demographics.occupation}.

=== YOUR PERSONA PROFILE ===
Name: {persona.name} | Age: {persona.demographics.age} | Role: {persona.demographics.occupation}
Tech Literacy: {persona.demographics.tech_literacy}/10 | Patience: {persona.psychographics.patience_score}/10 | Skepticism: {persona.psychographics.skepticism_score}/10
Budget Limit: ${persona.psychographics.price_ceiling_monthly}/mo | Core Values: {values_list}
Primary Frustration: "{persona.psychographics.primary_pain_point}"

=== BEHAVIORAL RULES ===
{rules_list}
{precheck_instruction}

=== DIRECTIVES ===
1. Respond naturally, candidly, and CONCISELY in 2-4 sentences max.
2. DO NOT split into 'thought' vs 'verbal'. Write ONE natural response.
3. NEVER flatter the interviewer or say "That's a great question/idea!".
4. Be honest about whether this fits your workflow, frustrates you, or solves your pain point.

OUTPUT FORMAT:
Reply ONLY with a valid JSON object matching this exact structure:
{{
  "response_text": "Your concise, realistic 2-4 sentence response as {persona.name}",
  "primary_objection": "Main concern or dealbreaker if any (otherwise null)"
}}
"""
    return prompt
