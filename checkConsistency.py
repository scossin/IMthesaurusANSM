
from python.SumUp.AllSubstances import AllSubstances
from python.SumUp.DrugClasses import DrugClasses
from python.SumUp.ThesaurusFilesBuilder import ThesaurusFilesBuilder

if __name__ == "__main__":
    path_pddis_file = "./thesauri/2019_09/JSON/Thesaurus_09_2019.json"
    path_substances_file = "./thesauri/2019_09/JSON/index_des_substances_09_2019.json"

    all_thesaurus_files = ThesaurusFilesBuilder.thesauri_files()
    all_substances = AllSubstances(all_thesaurus_files)
    all_substances.dump_substances_history("all_substance_history.json")
    all_substances.dump_unique_substances("unique_substances.json")

    # drug_classes = [DrugClasses(substances) for substances in all_substances.all_substances]
    drug_classes = []
    for substances in all_substances.all_substances:
        print(substances.thesaurus_files.thesaurus_version)
        drugclasses = DrugClasses(substances)
        drugclasses.detect_missing_entries()
