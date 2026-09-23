import json
import urllib.request
from typing import List
from persona_schema import Persona, Demographics, Psychographics

def generate_dynamic_mece_panel(product_or_domain: str, api_key: str, num_personas: int = 5) -> List[Persona]:
    """
    Generates a Mutually Exclusive, Collectively Exhaustive (MECE) panel of personas
    tailored specifically to a target product or domain on-the-fly.
    """
    api_key = api_key.strip().strip("'").strip('"')
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    prompt = f"""
You are a expert User Research Architect. Generate a set of {num_personas} Mutually Exclusive, Collectively Exhaustive (MECE) personas specifically tailored to test products in the following domain or product category:

DOMAIN / PRODUCT CATEGORY: "{product_or_domain}"

REQUIREMENTS:
1. Each persona must represent a distinctly different behavioral archetype with high contrast in patience, skepticism, tech literacy, and budget.
2. Personas must differ significantly on domain-specific traits relevant to "{product_or_domain}".
3. Provide explicit negative guardrail rules for each persona to prevent flattery or generic answers.

OUTPUT FORMAT:
Return ONLY a valid JSON array of objects with this exact structure:
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
    
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.5,
            "responseMimeType": "application/json"
        }
    }
    
    headers = {"Content-Type": "application/json"}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as resp:
            resp_data = json.loads(resp.read().decode("utf-8"))
            text_content = resp_data["candidates"][0]["content"]["parts"][0]["text"]
            json_list = json.loads(text_content)
            
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

def generate_zoomed_subpanel(selected_personas: List[Persona], product_context: str, api_key: str, num_subpersonas: int = 5) -> List[Persona]:
    """
    Funnel Zooming: Takes qualified interested personas and expands their core traits
    into a 5 Micro-MECE Sub-Persona Panel tailored for deep feature/pricing testing.
    """
    api_key = api_key.strip().strip("'").strip('"')
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    selected_summary = "\n".join([
        f"- {p.name} ({p.demographics.occupation}): Pain point = '{p.psychographics.primary_pain_point}', Budget Cap = ${p.psychographics.price_ceiling_monthly}/mo"
        for p in selected_personas
    ])
    
    prompt = f"""
You are a Lead Product Strategist doing deep-dive sub-segmentation research.

CONTEXT:
We conducted a screening interview for the product concept: "{product_context}".
Out of the initial broad audience, the following target personas were QUALIFIED as interested potential buyers:

QUALIFIED INTERESTED TARGET AUDIENCE:
{selected_summary}

YOUR TASK:
Take this specific target audience and EXPAND it into {num_subpersonas} Micro-MECE Sub-Personas.
These sub-personas represent distinct sub-segments of this target buyer pool (e.g. High-volume Power User, Email-first User, Tax Compliance Stickler, Team Admin, Mobile-only User).

REQUIREMENTS:
1. Each sub-persona MUST be a potential buyer of "{product_context}", but differ sharply on workflow preferences, feature priorities, team size, and micro-frustrations.
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
    
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.5,
            "responseMimeType": "application/json"
        }
    }
    
    headers = {"Content-Type": "application/json"}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as resp:
            resp_data = json.loads(resp.read().decode("utf-8"))
            text_content = resp_data["candidates"][0]["content"]["parts"][0]["text"]
            json_list = json.loads(text_content)
            
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
