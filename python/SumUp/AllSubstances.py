import json
from typing import List

from text_unidecode import unidecode

from python.SumUp.Substances import Substances
from python.SumUp.ThesaurusFiles import ThesaurusFiles


class AllSubstances:
    def __init__(self, all_thesaurus_files: List[ThesaurusFiles]):
        self.all_substances = [Substances(thesaurus_files) for thesaurus_files in all_thesaurus_files]
        self.dic_substances = {}
        self.__load_dic_substances()

    def __load_dic_substances(self):
        for substances_thesaurus in self.all_substances:
            for substance_object in substances_thesaurus.substances_objects:
                substance = substance_object.substance
                drug_classes = substance_object.drug_classes
                thesaurus_version = substances_thesaurus.thesaurus_files.thesaurus_version
                self._add_substance_2_dic_if_not_exists(substance)
                self._add_substance_information(substance, drug_classes, thesaurus_version)

    def _add_substance_information(self, substance, drug_classes, thesaurus_version):
        info_object = self._get_info_object(thesaurus_version, drug_classes)
        substances_info = self.dic_substances[substance]
        substances_info.append(info_object)

    @staticmethod
    def _get_info_object(thesaurus_version, drug_classes):
        return {
            "thesaurus_version": thesaurus_version,
            "drug_classes": drug_classes
        }

    def _add_substance_2_dic_if_not_exists(self, substance):
        if substance not in self.dic_substances:
            self.dic_substances[substance] = []

    def dump_substances_history(self, output_file):
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.dic_substances, f, ensure_ascii=False, indent=4)

    def dump_unique_substances(self, output_file):
        unique_substance = sorted([k for k in self.dic_substances], key=lambda string: unidecode(string).lower())
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(unique_substance, f, ensure_ascii=False, indent=4)