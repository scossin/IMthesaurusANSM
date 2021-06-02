import unittest

from python.Exceptions import SubstanceNotFound
from python.substance_functions import get_index_first_substance, is_a_paragraph_2_ignore

p_text = [" ", "abatacept\nInteraction", "acetylsulfafurazol"]


class TestsSubstance(unittest.TestCase):

    def test_get_index_first_substance_found(self):
        substance = "abatacept"
        index_first_substance = get_index_first_substance(p_text, substance)
        self.assertEqual(index_first_substance, 1)

    def test_get_index_first_substance_unfound(self):
        substance = "abciximab"
        self.assertRaises(SubstanceNotFound,
                          get_index_first_substance,
                          p_text, substance)

    def test_is_a_paragraph_2_ignore_metadata_lowerCase(self):
        text = "page 1/2"
        self.assertEqual(is_a_paragraph_2_ignore(text), True)

    def test_is_a_paragraph_2_ignore_empty(self):
        text = " "
        self.assertEqual(is_a_paragraph_2_ignore(text), True)


if __name__ == "__main__":
    unittest.main()
