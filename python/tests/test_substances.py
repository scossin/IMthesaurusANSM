import unittest

from python.Interactions.interaction_functions import get_index_first_entry
from python.Substance.Exceptions import SubstanceNotFound
from python.Substance.SubstanceDrugClasses import SubstanceClass
from python.Substance.substance_functions import is_a_paragraph_2_ignore

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

    def test_substance_famille(self):
        text = """acide alendronique\nVoir : bisphosphonates - substances à absorption réduite"""

        substance_class = SubstanceClass(text)
        self.assertEqual(substance_class.substance, "acide alendronique")
        self.assertEqual(substance_class.drug_classes, ["bisphosphonates",
                                                        "substances à absorption réduite"])


if __name__ == "__main__":
    unittest.main()
