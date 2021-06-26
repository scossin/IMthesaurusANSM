from python.SumUp.Substances import Substances
from python.SumUp.ThesaurusFiles import ThesaurusFiles
from python.SumUp.DrugClasses import DrugClasses


class Thesaurus:
    def __init__(self, thesaurus_files: ThesaurusFiles):
        self.substances = Substances(thesaurus_files)
        self.drug_classes = DrugClasses(self.substances, thesaurus_files, self.substances)
