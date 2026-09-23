import json
from typing import List, Dict, Any, Optional
from persona_schema import Persona, Demographics, Psychographics
from interview_engine import call_gemini_api

def generate_dynamic_mece_panel(product_or_domain: str, api_key: str, num_personas: int = 5) -> List[Persona]:
    """
    Generates a Mutually Exclusive, Collectively Exhaustive (MECE) panel of personas
    tailored specifically to a target product or domain on-the-fly.
    Uses call_gemini_api for model fallbacks, retries, and timeouts.
    """
    system_prompt = f"""
You are an expert User Research Architect. Generate a set of {num_personas} Mutually Exclusive, Collectively Exhaustive (MECE) personas specifically tailored to test products in the domain: "{product_or_domain}".

REQUIREMENTS:
1. Each persona must represent a distinctly different behavioral archetype with high contrast in patience, skepticism, tech literacy, and budget.
2. Personas must differ significantly on domain-specific traits relevant to "{product_or_domain}".
3. Provide explicit negative guardrail rules for each persona to prevent flattery or generic answers.

OUTPUT FORMAT:
Return ONLY a valid JSON array of objects matching this exact structure:
[
  {{
    "id": "p_01",
    "name": "Full Name",
    "demographics": {{
      "age": 35,
      "occupation": "Job Title",
      "income_bracket": "Low / Mid / High / Enterprise",
      "tech_literacy": 7
    }},
    "psychographics": {{
      "patience_score": 4,
      "skepticism_score": 8,
      "price_ceiling_monthly": 49.0,
      "primary_pain_point": "Domain-specific frustration",
      "core_values": ["Value1", "Value2"]
    }},
    "guardrail_rules": [
      "Rule 1 specific to this persona",
      "Rule 2 specific to budget or domain friction"
    ]
  }}
]
"""
    
    user_query = f"Generate {num_personas} MECE personas for domain '{product_or_domain}' in JSON format."
    
    try:
        json_list = call_gemini_api(api_key, system_prompt, user_query)
        if isinstance(json_list, dict) and "personas" in json_list:
            json_list = json_list["personas"]
            
        personas = []
        for item in json_list:
            personas.append(
                Persona(
                    id=item.get("id", f"p_{len(personas)+1}"),
                    name=item.get("name", "Generated Persona"),
                    demographics=Demographics(**item["demographics"]),
                    psychographics=Psychographics(**item["psychographics"]),
                    guardrail_rules=item.get("guardrail_rules", [])
                )
            )
        return personas
    except Exception as e:
        raise RuntimeError(f"Failed to generate dynamic personas for domain '{product_or_domain}': {str(e)}")

def generate_zoomed_subpanel(
    selected_personas: List[Persona], 
    product_context: str, 
    api_key: str, 
    interview_history: Optional[List[Dict[str, Any]]] = None,
    num_subpersonas: int = 5
) -> List[Persona]:
    """
    Funnel Zooming: Takes qualified interested personas AND their expressed interview answers
    (problem-first responses) to expand into a 5 Micro-MECE Sub-Persona Panel tailored for deep testing.
    Uses call_gemini_api for model fallbacks, retries, and timeouts.
    """
    selected_summary = "\n".join([
        f"- {p.name} ({p.demographics.occupation}): Primary Pain = '{p.psychographics.primary_pain_point}', Budget Cap = ${p.psychographics.price_ceiling_monthly}/mo"
        for p in selected_personas
    ])
    
    history_str = ""
    if interview_history:
        history_str = "\nEXPRESSED PROBLEM-FIRST INTERVIEW RESPONSES FROM SESSION:\n"
        for idx, item in enumerate(interview_history[-10:], 1):
            history_str += f"Q: '{item['question']}'\n   -> {item['persona_name']}: \"{item['response_text']}\"\n"
            if item.get('primary_objection'):
                history_str += f"      [Expressed Concern: {item['primary_objection']}]\n"

    system_prompt = f"""
You are a Lead Product Strategist executing Funnel Zooming (Sub-Segment Research).

CONTEXT & PRODUCT DOMAIN:
"{product_context}"

QUALIFIED TARGET PERSONAS SELECTED FOR ZOOM:
{selected_summary}
{history_str}

YOUR TASK:
Analyze the expressed pain points, workarounds, and frustrations in the interview transcript above.
Expand this qualified target audience into {num_subpersonas} Micro-MECE Sub-Personas.
These sub-personas MUST represent distinct micro-archetypes of this interested target group (e.g. High-volume Power User, Email-first User, Compliance Stickler, Team Admin, Mobile-only User).

REQUIREMENTS:
1. Ground the sub-personas directly in the pain points expressed in the interview transcript.
2. Provide explicit guardrail rules for each sub-persona to test edge-case workflow failures.

OUTPUT FORMAT:
Return ONLY a valid JSON array of objects matching this exact structure:
[
  {{
    "id": "zp_01",
    "name": "Full Name",
    "demographics": {{
      "age": 32,
      "occupation": "Sub-Segment Role Title [e.g. Power User]",
      "income_bracket": "Mid / High",
      "tech_literacy": 8
    }},
    "psychographics": {{
      "patience_score": 5,
      "skepticism_score": 6,
      "price_ceiling_monthly": 39.0,
      "primary_pain_point": "Specific workflow friction",
      "core_values": ["SubValue1", "SubValue2"]
    }},
    "guardrail_rules": [
      "Rule 1 for this micro-workflow",
      "Rule 2 for feature dealbreakers"
    ]
  }}
]
"""
    
    user_query = f"Generate {num_subpersonas} zoomed micro-MECE sub-personas in JSON format."
    
    try:
        json_list = call_gemini_api(api_key, system_prompt, user_query)
        if isinstance(json_list, dict) and "personas" in json_list:
            json_list = json_list["personas"]
            
        personas = []
        for item in json_list:
            personas.append(
                Persona(
                    id=item.get("id", f"zp_{len(personas)+1}"),
                    name=item.get("name", "Zoom Sub-Persona"),
                    demographics=Demographics(**item["demographics"]),
                    psychographics=Psychographics(**item["psychographics"]),
                    guardrail_rules=item.get("guardrail_rules", [])
                )
            )
        return personas
    except Exception as e:
        raise RuntimeError(f"Failed to generate zoomed subpanel: {str(e)}")
