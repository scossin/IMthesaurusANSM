import json
import pathlib

from python.Interactions.PDDIManuallyCurated import Singleton
from python.SumUp.DrugClasses import DrugClasses
from python.utils.utils import Utils


class AltDrugClassLabels(metaclass=Singleton):
    dict_alt_2_main_label = {}
    dict_main_2_alt_label = {}

    def __init__(self):
        self.dict_alt_2_main_label = self.__load_alt_classes_labels()
        self.__transform_alt_2_main_label(self.dict_alt_2_main_label)

    def __transform_alt_2_main_label(self, dict_alt_2_main_label):
        """
        reverse key / value pair
        :return:
        """
        for alt_label in dict_alt_2_main_label:
            main_labels = dict_alt_2_main_label[alt_label]
            for main_label in main_labels:
                normalized_main_label = Utils.remove_accents_and_lower_case(main_label)
                self.dict_main_2_alt_label[normalized_main_label] = alt_label

    @staticmethod
    def __load_alt_classes_labels() -> dict:
        current_dir = pathlib.Path(__file__).parent.absolute()
        filepath = str(current_dir) + "/altClassLabels.json"
        with open(filepath) as json_file:
            data = json.load(json_file)
        return data

    @classmethod
    def add_alternative_class_labels(cls, substance_object):
        for drug_class in substance_object.drug_classes:
            if AltDrugClassLabels.drug_class_has_alternative_label(drug_class):
                AltDrugClassLabels.add_alternative_label_if_not_added_yet(drug_class, substance_object)

    @classmethod
    def drug_class_has_alternative_label(cls, drug_class):
        normalized_drug_class = Utils.remove_accents_and_lower_case(drug_class)
        if normalized_drug_class in cls.dict_main_2_alt_label:
            return True

    @classmethod
    def add_alternative_label_if_not_added_yet(cls, drug_class, substance_object):
        normalized_drug_class = Utils.remove_accents_and_lower_case(drug_class)
        alt_label_drug_class = cls.dict_main_2_alt_label[normalized_drug_class]
        if alt_label_drug_class not in substance_object.drug_classes:
            substance_object.drug_classes.append(alt_label_drug_class)
