import os
from typing import List

import pydantic

from python.Interactions.CuratedPDDIobject import CuratedPDDIobject


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class PDDIManullyCurated(metaclass=Singleton):
    """
    Some mechanism of action and severity levels are too difficult to extract automatically from the PDDI's description
    I put, in a JSON file, these difficult cases and curate them manually.
    When extracting the mechanism of action and the severity levels in a description,
    I check if the description matches a curated one.
    """
    FILENAME = "./pddis_manually_extracted.json"

    def __init__(self):
        self.map_description_to_pddi = {}
        self.load_pddis_manually_curated()

    def load_pddis_manually_curated(self):
        current_dir = os.path.dirname(__file__)
        path = current_dir + "/" + PDDIManullyCurated.FILENAME
        pddis_curated = pydantic.parse_file_as(List[CuratedPDDIobject], path)
        for pddi in pddis_curated:
            self.map_description_to_pddi[pddi.description] = pddi

    def is_a_manually_curated_description(self, description_string) -> bool:
        return description_string in self.map_description_to_pddi

    def get_manually_curated_pddi(self, description_string) -> CuratedPDDIobject:
        return self.map_description_to_pddi.get(description_string)
