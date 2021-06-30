
from python.SumUp.AllSubstances import AllSubstances
from python.SumUp.DrugClasses import DrugClasses
from python.SumUp.ThesaurusFilesBuilder import ThesaurusFilesBuilder

if __name__ == "__main__":
    all_thesaurus_files = ThesaurusFilesBuilder.thesauri_files()
    all_substances = AllSubstances(all_thesaurus_files)
    all_substances.dump_substances_history("all_substance_history.json")
    all_substances.dump_unique_substances("unique_substances.json")

    for substances in all_substances.all_substances:
        print(substances.thesaurus_files.thesaurus_version)
        drugclasses = DrugClasses(substances)
        drugclasses.detect_missing_entries()
