import json
import pathlib
from typing import Dict, List

from pydantic import BaseModel

from python.Interactions.PDDIManuallyCurated import Singleton
from python.Interactions.PDDIobject import SubstanceObject
from python.utils.utils import Utils


class AltValues(BaseModel):
    __root__: Dict[str, List[str]]  # map a label to a list of other labels


class AltDrugClassLabels(metaclass=Singleton):
    """
    The purpose of this class is to add alternative drug class labels to substance_object
    For example, in the thesaurus file, we have a drug_class "anticoagulants oraux" also called "autres anticoagulants oraux"
    But in the substance file, we only have "anticoagulants oraux" that appears. This class adds "autres anticoagulants oraux"
    To every substance that has the "anticoagulants oraux" drug class
    """
    FILENAME_ALT_LABELS = "/altClassLabels.json"
    dict_alt_2_main_label: AltValues = {}  # map an alternative label to a list of main labels
    dict_main_2_alt_label: AltValues = {}  # map a main label to a list of alternative labels

    def __init__(self):
        self.dict_alt_2_main_label = self.__load_alt_classes_labels()
        self.__transform_alt_2_main_label(self.dict_alt_2_main_label)

    @classmethod
    def add_alternative_class_labels(cls, substance_object):
        for drug_class in substance_object.drug_classes:
            if AltDrugClassLabels.__drug_class_has_alternative_label(drug_class):
                AltDrugClassLabels.__add_alternative_label_if_not_added_yet(drug_class, substance_object)
                
    @classmethod
    def __transform_alt_2_main_label(cls, dict_alt_2_main_label):
        """
        reverse key / value pair
        :return:
        """
        for alt_label in dict_alt_2_main_label:
            main_labels = dict_alt_2_main_label[alt_label]
            for main_label in main_labels:
                normalized_main_label = Utils.remove_accents_and_lower_case(main_label)
                cls.__add_alt_label(normalized_main_label, alt_label)

    @classmethod
    def __add_alt_label(cls, normalized_main_label, alt_label):
        if normalized_main_label not in cls.dict_main_2_alt_label:
            cls.dict_main_2_alt_label[normalized_main_label] = []
        cls.dict_main_2_alt_label[normalized_main_label].append(alt_label)

    @classmethod
    def __load_alt_classes_labels(cls) -> dict:
        current_dir = pathlib.Path(__file__).parent.absolute()
        filepath = str(current_dir) + cls.FILENAME_ALT_LABELS
        with open(filepath) as json_file:
            data = json.load(json_file)
        return data

    @classmethod
    def __drug_class_has_alternative_label(cls, drug_class):
        normalized_drug_class = Utils.remove_accents_and_lower_case(drug_class)
        if normalized_drug_class in cls.dict_main_2_alt_label:
            return True

    @classmethod
    def __add_alternative_label_if_not_added_yet(cls, drug_class: str, substance_object: SubstanceObject):
        normalized_drug_class = Utils.remove_accents_and_lower_case(drug_class)
        alt_labels_drug_class: List[str] = cls.dict_main_2_alt_label[normalized_drug_class]
        for alt_label in alt_labels_drug_class:
            if alt_label not in substance_object.drug_classes:
                substance_object.drug_classes.append(alt_label)
