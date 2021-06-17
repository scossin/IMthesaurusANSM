import unittest
import pathlib

from extractInteraction import extract_pddis
from python.Interactions.DrugPDDIs import DrugPDDIs
from python.Interactions.Exceptions import MainDrugError, PDDIerror, SeverityLevelerror, PlusDrugUnfounderror, \
    PDDIdescriptionError
from python.Interactions.PDDI import PDDI
from python.Interactions.Severity_Levels import get_severity_levels_multiple, get_abbreviation
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
        self.assertRaises(TypeError, DrugPDDIs, pddi_text)

        pddi_text = ["ANTI-VITAMINE K"]
        self.assertRaises(PDDIerror, DrugPDDIs, pddi_text)

        pddi_text = ["ANTI-VITAMINE K", "+ Anticoagulant"]
        self.assertRaises(PDDIdescriptionError, DrugPDDIs, pddi_text)

        pddi_text = ["ANTI-VITAMINE K", "+ Anticoagulant", "Majoration du risque hémorragique"]
        error_message = "no severity level detected in this description: ['Majoration du risque hémorragique']"
        self.assertEqual(DrugPDDIs(pddi_text).pddis[0].interaction_mechanism, error_message)

        pddi_text = ["ANTI-VITAMINE K", "+ Anticoagulant", "Association DECONSEILLEE",
                     "Majoration du risque hémorragique"]
        self.assertEqual(DrugPDDIs(pddi_text).pddis[0].plus_drug, "Anticoagulant")

    def test_PDDI_severity_level_detection(self):
        main_drug = "ACIDE ACETYLSALICYLIQUE"
        plus_drug = "+ ACETAZOLAMIDE"
        between_main_and_plus_drug = ""
        desription = ["\n",
                      "Association DECONSEILLEEMajoration des effets indésirables, et notamment de l'acidose"
                      ]
        pddi = PDDI(main_drug, plus_drug, between_main_and_plus_drug, desription)
        self.assertEqual(pddi.severity_levels[0].level, "Association DECONSEILLEE")

    def test_severity_levels_multiple(self):
        multiple_severity_level = get_severity_levels_multiple()
        self.assertEqual(len(multiple_severity_level), 5)

    def test_extract_pddis(self):
        current_dir = pathlib.Path(__file__).parent.absolute()
        filepath = str(current_dir) + "/interaction_test_abatacept.txt"
        with open(filepath, "r") as f:
            lines = f.readlines()
            pddis = extract_pddis(lines, False)
            # check 2 potential drug drug interactions are detected
            self.assertEqual(len(pddis), 2)
            # check the content of the first PDDI
            pddi0 = pddis[0]
            self.assertEqual(pddi0.main_drug, 'ABATACEPT')
            self.assertEqual(pddi0.plus_drug, 'ANTI-TNF ALPHA')
            self.assertEqual(pddi0.severity_levels[0].level, 'Association DECONSEILLEE')
            self.assertEqual(pddi0.interaction_mechanism, 'Majoration de l’immunodépression.')
            # check the content of the second PDDI
            pddi1 = pddis[1]
            self.assertEqual(pddi1.main_drug, 'ABATACEPT')
            self.assertEqual(pddi1.plus_drug, 'VACCINS VIVANTS ATTÉNUÉS')
            self.assertEqual(pddi1.severity_levels[0].level, 'Association DECONSEILLEE')
            self.assertEqual(pddi1.severity_levels[0].info,
                             "ainsi que pendant les 3 mois suivant l'arrêt du traitement.")
            self.assertEqual(pddi1.interaction_mechanism,
                             "Risque de maladie vaccinale généralisée, éventuellement mortelle.")

    def test_get_long_forms(self):
        abbreviation = get_abbreviation("CI")
        self.assertEqual(abbreviation.long, 'Contre-indication')
        self.assertRaises(SeverityLevelerror,
                          get_abbreviation,
                          "AD")


if __name__ == '__main__':
    unittest.main()
