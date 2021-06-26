from typing import List

from pydantic import BaseModel


class SeverityLevel(BaseModel):
    level: str
    info: str


class PDDIobject(BaseModel):
    main_drug: str
    between_main_and_plus_drug: str
    plus_drug: str
    severity_levels: List[SeverityLevel]
    interaction_mechanism: str
    description: str


class SubstanceObject(BaseModel):
    substance: str
    drug_classes: List[str]
