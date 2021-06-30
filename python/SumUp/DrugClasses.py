from typing import List, Set

import pydantic

from python.Interactions.PDDIobject import SubstanceObject, PDDIobject
from python.SumUp.Substances import Substances
from python.Substance.AltDrugClassLabels import AltDrugClassLabels
from python.utils.utils import Utils


class DrugClasses:
    CLASSES_WO_MOLECULES = ["preservatifs en latex"]

    CLASSES_ROUTE_OF_ADMIN = ["medicaments administres par voie orale",
                              "medicaments utilises par voie vaginale",
                              "sels de fer par voie injectable"]

    ENTRIES_NOT_MOLECULES = ["consommation d'alcool",
                             "alcool (boisson ou excipient)",
                             "theine",
                             "jus de pamplemousse",
                             "pamplemousse (jus et fruit)"]

    @classmethod
    def is_a_class_without_molecules(cls, class_name):
        return class_name in cls.CLASSES_WO_MOLECULS

    def __init__(self, substances: Substances):

        self.substances = substances
        self.thesaurus_files = self.substances.thesaurus_files

        self.__create_set_substances(substances.substances_objects)
        pddis: List[PDDIobject] = pydantic.parse_file_as(List[PDDIobject],
                                                         self.thesaurus_files.get_thesaurus_file_path())
        self.__create_set_thesauris_entries(pddis)

    def detect_missing_entries(self):
        missing_entry_in_substances_files = [thesaurus_entry for thesaurus_entry in self.set_thesaurus_entries
                                             if not self.__entry_is_in_substance_file(thesaurus_entry)]
        print(missing_entry_in_substances_files)

    def __entry_is_in_substance_file(self, entry):
        return entry in self.set_substances_file \
               or self.__found_if_begings_by_autres(entry) \
               or DrugClasses.__entry_to_ignore(entry)

    @classmethod
    def __entry_to_ignore(cls, entry):
        return entry in cls.CLASSES_WO_MOLECULES \
               or entry in cls.CLASSES_ROUTE_OF_ADMIN \
               or entry in cls.ENTRIES_NOT_MOLECULES

    def __found_if_begings_by_autres(self, entry):
        if 'autres' not in entry:
            return False
        else:
            return self.__is_found_when_beginning_by_autres(entry)

    def __is_found_when_beginning_by_autres(self, entry):
        alt_labels = AltDrugClassLabels().dict_alt_2_main_label
        if entry not in alt_labels:
            return False
        main_labels = alt_labels[entry]
        return any(list(main_label in self.set_substances_file for main_label in main_labels))

    @staticmethod
    def __remove_autres(entry: str):
        entry_wo_autres = entry.replace("(autres)", "").replace("autres", "")
        return entry_wo_autres.strip()

    def __create_set_substances(self, substances: List[SubstanceObject]):
        list_substances = [Utils.remove_accents_and_lower_case(substance.substance) for substance in substances]
        set_substances = self.create_normalized_set(list_substances)

        drug_classes = [substance.drug_classes for substance in substances]
        list_drug_classes = [drug_class for sublist in drug_classes for drug_class in sublist]
        set_drug_classes = self.create_normalized_set(list_drug_classes)
        self.set_substances_file = set_substances.union(set_drug_classes)

    def __create_set_thesauris_entries(self, pddis) -> None:
        list_main_drugs = [pddi.main_drug for pddi in pddis]
        set_main_drugs = self.create_normalized_set(list_main_drugs)

        list_plus_drugs = [pddi.plus_drug for pddi in pddis]
        set_plus_drugs = self.create_normalized_set(list_plus_drugs)
        self.set_thesaurus_entries = set_main_drugs.union(set_plus_drugs)

    @staticmethod
    def normalize_list_of_string(list_of_string: List[str]) -> List[str]:
        list_of_string_normalized = [Utils.remove_accents_and_lower_case(string) for string in list_of_string]
        return list_of_string_normalized

    def create_normalized_set(self, list_of_string: List[str]) -> Set[str]:
        list_of_string_normalized = self.normalize_list_of_string(list_of_string)
        normalized_set = set(list_of_string_normalized)
        return normalized_set
