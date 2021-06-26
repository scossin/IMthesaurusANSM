from typing import List, Set

import pydantic
from text_unidecode import unidecode

from python.Interactions.PDDIobject import SubstanceObject, PDDIobject
from python.SumUp.Substances import Substances


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

    ALTERNATIVE_LABELS = {
        'autres medicaments hyponatremiants': ["hyponatremiants"],
        'autres medicaments abaissant le seuil epileptogene': ["medicaments abaissant le seuil epileptogene"],
        'autres medicaments sedatifs': ["medicaments sedatifs"],
        'autres hyperkaliemiants': ["hyperkaliemiants"],
        'autres medicaments anticholinesterasiques': ["anticholinesterasiques"],
        'autres anti-inflammatoires non steroidiens': ["anti-inflammatoires non steroidiens"],
        'autres hypokaliemiants': ["hypokaliemiants"],
        'autres diuretiques epargneurs de potassium (seuls ou associes)': ["diuretiques epargneurs de potassium (seuls ou associes)"],
        'autres analgesiques morphiniques agonistes': ["analgesiques morphiniques agonistes"],
        'autres medicaments nephrotoxiques': ["medicaments nephrotoxiques"],
        'autres sympathomimetiques indirects': ["sympathomimetiques indirects"],
        'autres bradycardisants': ["bradycardisants"],
        'autres medicaments atropiniques': ["medicaments atropiniques"],
        'autres antiarythmiques': ["antiarythmiques"],
        'autres hypnotiques': ["hypnotiques"],
        'autres aminosides': ["aminosides"],
        'fibrates (autres)': ["fibrates"],
        'autres medicaments ototoxiques': ["medicaments ototoxiques", "ototoxiques"],
        'autres retinoides': ["retinoides"],
        'autres anticoagulants oraux': ["anticoagulants oraux"],
        'autres medicaments methemoglobinisants': ["medicaments methemoglobinisants"],
        'autres medicaments agissant sur l\'hemostase': ["medicaments agissant sur l'hemostase"],
        'autres medicaments a risque d\'angio-oedeme': ["medicaments, bradykinine et angio-oedeme"],
        'autres medicaments a l\'origine d\'un syndrome serotoninergique': ["medicaments a l'origine d'un syndrome serotoninergique"]
    }

    def __init__(self, substances: Substances):
        self.substances = substances
        self.thesaurus_files = self.substances.thesaurus_files

        self.__create_set_substances(substances.substances_objects)
        pddis: List[PDDIobject] = pydantic.parse_file_as(List[PDDIobject], self.thesaurus_files.get_thesaurus_file_path())
        self.__create_set_thesauris_entries(pddis)
        self.detect_missing_entries()

    def detect_missing_entries(self):
        missing_entry_in_substances_files = [entry for entry in self.set_thesaurus_entries
                                             if not self.__entry_is_in_substance_file(entry)]
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
        if entry not in self.ALTERNATIVE_LABELS:
            return False
        alternative_labels = self.ALTERNATIVE_LABELS[entry]
        return any(list(alt_label in self.set_substances_file for alt_label in alternative_labels))
        # entry_wo_autres = self.__remove_autres(entry)
        # return entry_wo_autres in self.set_substances_file

    @staticmethod
    def __remove_autres(entry: str):
        entry_wo_autres = entry.replace("(autres)", "").replace("autres", "")
        return entry_wo_autres.strip()

    def __create_set_substances(self, substances: List[SubstanceObject]):
        list_substances = [self.normalize_string(substance.substance) for substance in substances]
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

    @classmethod
    def normalize_string(cls, string: str) -> str:
        lower_string = string.lower()
        unaccented_lower_string = unidecode(lower_string)
        return unaccented_lower_string

    def normalize_list_of_string(self, list_of_string: List[str]) -> List[str]:
        list_of_string_normalized = [self.normalize_string(string) for string in list_of_string]
        return list_of_string_normalized

    def create_normalized_set(self, list_of_string: List[str]) -> Set[str]:
        list_of_string_normalized = self.normalize_list_of_string(list_of_string)
        normalized_set = set(list_of_string_normalized)
        return normalized_set

    @classmethod
    def is_a_class_without_molecules(cls, class_name):
        return class_name in cls.CLASSES_WO_MOLECULS

    @classmethod
    def get_alt_labels(cls, self, label):
        return cls.ALTERNATIVE_LABELS.get(label, {})
