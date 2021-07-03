from python.Check.Substances import Substances
from python.Check.ThesaurusFiles import ThesaurusFiles
from python.Check.DrugClasses import DrugClasses


class Thesaurus:
    def __init__(self, thesaurus_files: ThesaurusFiles):
        self.substances = Substances(thesaurus_files)
        self.drug_classes = DrugClasses(self.substances, thesaurus_files, self.substances)
