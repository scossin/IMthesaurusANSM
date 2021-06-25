import unittest

from python.Interactions.PDDIManuallyCurated import PDDIManullyCurated


class MyTestCase(unittest.TestCase):
    def test_is_a_manually_curated_description(self):
        description_string = "CI - PE\nAvec le méthotrexate utilisé à des doses > 20 mg/semaine : \n- contre-indication avec l'acide acétylsalicylique utilisé à doses \nantalgiques, antipyrétiques ou anti-inflammatoires\n- précaution d'emploi avec des doses antiagrégantes plaquettaires \nd'acide acétylsalicylique. Contrôle hebdomadaire de l’hémogramme \ndurant les premières semaines de l’association. Surveillance accrue en \ncas d’altération (même légère) de la fonction rénale, ainsi que chez le \nsujet âgé.\n\nAvec le méthotrexate utilisé à des doses =< 20 mg/semaine :\n- précaution d'emploi avec l'acide acétylsalicylique utilisé à doses \nantalgiques, antipyrétiques ou anti-inflammatoires. Contrôle \nhebdomadaire de l’hémogramme durant les premières semaines de \nl’association. Surveillance accrue en cas d’altération (même légère) de \nla fonction rénale, ainsi que chez le sujet âgé.\n\nMajoration de la toxicité, notamment hématologique, du \nméthotrexate (diminution de sa clairance rénale par l'acide \nacétylsalicylique)."
        pddis_man_curated = PDDIManullyCurated()
        self.assertTrue(pddis_man_curated.is_a_manually_curated_description(description_string))

    def test_is_not_a_manually_curated_description(self):
        description_string = "another string description"
        pddis_man_curated = PDDIManullyCurated()
        self.assertFalse(pddis_man_curated.is_a_manually_curated_description(description_string))

    def test_first_pddi_curated_object(self):
        description_string = "CI - PE\nAvec le méthotrexate utilisé à des doses > 20 mg/semaine : \n- contre-indication avec l'acide acétylsalicylique utilisé à doses \nantalgiques, antipyrétiques ou anti-inflammatoires\n- précaution d'emploi avec des doses antiagrégantes plaquettaires \nd'acide acétylsalicylique. Contrôle hebdomadaire de l’hémogramme \ndurant les premières semaines de l’association. Surveillance accrue en \ncas d’altération (même légère) de la fonction rénale, ainsi que chez le \nsujet âgé.\n\nAvec le méthotrexate utilisé à des doses =< 20 mg/semaine :\n- précaution d'emploi avec l'acide acétylsalicylique utilisé à doses \nantalgiques, antipyrétiques ou anti-inflammatoires. Contrôle \nhebdomadaire de l’hémogramme durant les premières semaines de \nl’association. Surveillance accrue en cas d’altération (même légère) de \nla fonction rénale, ainsi que chez le sujet âgé.\n\nMajoration de la toxicité, notamment hématologique, du \nméthotrexate (diminution de sa clairance rénale par l'acide \nacétylsalicylique)."
        pddis_man_curated = PDDIManullyCurated()
        curated_pddi = pddis_man_curated.get_manually_curated_pddi(description_string)
        self.assertTrue(len(curated_pddi.severity_levels) == 2)
        self.assertTrue(curated_pddi.severity_levels[0].level == "CONTRE-INDICATION")
        self.assertTrue(curated_pddi.severity_levels[1].level == "Précaution d'emploi")


if __name__ == '__main__':
    unittest.main()
