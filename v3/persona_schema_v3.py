"""
Persona Schema V3: Behavioral Profiles for Mental Accounting
Reuses and refines PersonaV2 with explicit Mental Accounting support.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from v2.persona_schema_v2 import (
    Capabilities, CulturalMindset, SocialProofAndNetwork,
    CognitiveFriction, Demographics, Psychographics, PersonaV2
)

# PersonaV3 inherits full schema from PersonaV2
class PersonaV3(PersonaV2):
    pass
