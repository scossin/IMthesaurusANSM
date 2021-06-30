import unittest

import pydantic

from python.Interactions.PDDIobject import SubstanceObject
from python.Interactions.interaction_functions import get_index_first_entry
from python.Substance.AltDrugClassLabels import AltDrugClassLabels
from python.Substance.Exceptions import SubstanceNotFound
from python.Substance.SubstanceDrugClasses import SubstanceClass
from python.Substance.substance_functions import is_a_paragraph_2_ignore, remove_wrong_p_tag

p_text = [" ", "abatacept\nInteraction", "acetylsulfafurazol"]
p_text_without_abatacept = [" ", "acetylsulfafurazol\nInteraction", "carbamazepine"]


class TestsSubstance(unittest.TestCase):

    def test_get_index_first_substance_found(self):
        index_first_substance = get_index_first_entry(p_text)
        self.assertEqual(index_first_substance, 1)

    def test_get_index_first_substance_unfound(self):
        self.assertRaises(SubstanceNotFound,
                          get_index_first_entry,
                          p_text_without_abatacept)

    def test_is_a_paragraph_2_ignore_metadata_lowerCase(self):
        text = "page 1/2"
        self.assertEqual(is_a_paragraph_2_ignore(text), True)

    def test_is_a_paragraph_2_ignore_empty(self):
        text = " "
        self.assertEqual(is_a_paragraph_2_ignore(text), True)

    def test_iec_is_not_a_paragraph_2_ignore_empty(self):
        text = "inhibiteurs de l'enzyme de conversion "  # conversion contains Version but should be ignored
        self.assertEqual(not is_a_paragraph_2_ignore(text), True)

    def test_substance_famille(self):
        text = """acide alendronique\nVoir : bisphosphonates - substances à absorption réduite"""

        substance_class = SubstanceClass(text)
        self.assertEqual(substance_class.substance, "acide alendronique")
        self.assertEqual(substance_class.drug_classes, ["bisphosphonates",
                                                        "substances à absorption réduite"])

    def test_remove_wrong_tag(self):
        all_lines = ["<p>acide alendronique", "</p>", "<p>Voir : bisphosphonates", "</p>"]
        remove_wrong_p_tag(all_lines)
        new_lines = ["<p>acide alendronique", "", "Voir : bisphosphonates", "</p>"]
        self.assertEqual(all_lines, new_lines)

    def test_alt_label(self):
        output_expected = {
            "substance": "dabigatran",
            "drug_classes": [
                "anticoagulants oraux",
                "autres anticoagulants oraux",
                "autres médicaments agissant sur l'hémostase"
            ]
        }
        input_value = {
            "substance": "dabigatran",
            "drug_classes": [
                "anticoagulants oraux"
            ]
        }
        substance_object = SubstanceObject.parse_obj(input_value)
        alt_drugs_classes = AltDrugClassLabels()
        alt_drugs_classes.add_alternative_class_labels(substance_object)
        self.assertEqual(substance_object.dict(), output_expected)


if __name__ == "__main__":
    unittest.main()
