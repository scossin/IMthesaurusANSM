from typing import List

import pydantic

from python.Interactions.PDDIobject import SubstanceObject
from python.Check.ThesaurusFiles import ThesaurusFiles


class Substances:

    def __init__(self, thesaurus_files: ThesaurusFiles):
        self.thesaurus_files: ThesaurusFiles = thesaurus_files
        self.substances_objects: List[SubstanceObject] = self.__get_substances()

    def __get_substances(self) -> List[SubstanceObject]:
        substance_file_path = self.thesaurus_files.get_substance_file_path()
        substances = pydantic.parse_file_as(List[SubstanceObject], substance_file_path)
        return substances
