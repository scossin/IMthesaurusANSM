from typing import List, Dict, Set

from pydantic import BaseModel


class SeverityLevel(BaseModel):
    level: str
    info: str


class CuratedPDDIobject(BaseModel):
    severity_levels: List[SeverityLevel]
    interaction_mechanism: str
    description: str
