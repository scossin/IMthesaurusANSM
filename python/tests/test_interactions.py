import unittest

from python.Interactions.DrugPDDIs import DrugPDDIs
from python.Interactions.Exceptions import MainDrugError, PDDIerror
from python.Interactions.PDDI import PDDI
from python.Interactions.Severity_Levels import get_severity_levels_multiple
from python.Interactions.interaction_functions import _is_metadata, _line_matched_main_drug, _line_matched_plus_drug, \
    detect_line_tag, LineTag, check_main_drugs_are_ordered


class MyTestCase(unittest.TestCase):
    def test_metadata_interaction(self):
        self.assertEqual(_is_metadata("2 "), True)

    def test_matched_main_drug(self):
        self.assertEqual(_line_matched_main_drug("EFAVIRENZ"), True)
        self.assertEqual(_line_matched_main_drug("+ EFAVIRENZ"), False)
        self.assertEqual(_line_matched_main_drug("CONTRE INDICATION"), False)
        self.assertEqual(_line_matched_main_drug("Association Déconseillée"), False)
        self.assertEqual(_line_matched_main_drug("CI - PE"), False)
        self.assertEqual(_line_matched_main_drug("CYP3A4."), False)
        self.assertEqual(_line_matched_main_drug("ANTI-INFECTIEUX ET HEMOSTASE"), False)

    def test_matched_plus_drug(self):
        self.assertEqual(_line_matched_plus_drug("EFAVIRENZ"), False)
        self.assertEqual(_line_matched_plus_drug("+ EFAVIRENZ"), True)
        self.assertEqual(_line_matched_plus_drug("CONTRE INDICATION"), False)

    def test_detect_line_tag(self):
        self.assertEqual(detect_line_tag("EFAVIRENZ"), LineTag.MAIN_DRUG)
        self.assertEqual(detect_line_tag("+ EFAVIRENZ"), LineTag.PLUS_DRUG)
        self.assertEqual(detect_line_tag("CONTRE INDICATION"), LineTag.OTHER)
        self.assertEqual(detect_line_tag("Association Déconseillée"), LineTag.OTHER)

    def test_main_drugs_ordered(self):
        main_drugs = ["BUPROPION", "BUSPIRONE", "BUSULFAN"]
        self.assertTrue(check_main_drugs_are_ordered(main_drugs) is None)
        main_drugs = ["BUPROPION", "BUSPIRONE", "WRONG PLACE", "BUSULFAN"]
        self.assertRaises(MainDrugError,
                          check_main_drugs_are_ordered,
                          main_drugs)

    def test_DrugPDDIs_pddi_text(self):
        pddi_text = "ANTI-VITAMINE K"
        self.assertRaises(TypeError,
                          DrugPDDIs,
                          pddi_text)

        pddi_text = ["ANTI-VITAMINE K"]
        self.assertRaises(PDDIerror,
                          DrugPDDIs,
                          pddi_text)

        pddi_text = ["ANTI-VITAMINE K", "+ Anticoagulant"]
        self.assertEqual(DrugPDDIs(pddi_text).main_drug, "ANTI-VITAMINE K")

    def test_PDDI_severity_level_detection(self):
        main_drug = "ACIDE ACETYLSALICYLIQUE"
        plus_drug = "+ ACETAZOLAMIDE"
        desription = ["\n",
                      "Association DECONSEILLEEMajoration des effets indésirables, et notamment de l'acidose"
                      ]
        pddi = PDDI(main_drug, plus_drug, desription)
        self.assertEqual(pddi.severity_level, "Association DECONSEILLEE")

    def test_severity_levels_multiple(self):
        multiple_severity_level = get_severity_levels_multiple()
        self.assertEqual(len(multiple_severity_level), 5)


if __name__ == '__main__':
    unittest.main()
