import os
from typing import List

from python.SumUp.AllSubstances import AllSubstances
from python.SumUp.DrugClasses import DrugClasses
from python.SumUp.ThesaurusFiles import create_thesaurus_files, ThesaurusFiles


def thesauri_files() -> List[str]:
    rootdir = "./thesauri"
    thesauri_files = []
    for root, subdirs, files in os.walk(rootdir):
        json_files = list(filter(_is_a_json_file, files))
        new_thesaurus_files = create_thesaurus_files(root, json_files)
        thesauri_files.append(new_thesaurus_files)
    thesauri_files: List[ThesaurusFiles] = [thesaurus_files for thesaurus_files in thesauri_files
                                                 if thesaurus_files is not None]
    [thesaurus_files.check_files() for thesaurus_files in thesauri_files]
    thesauri_files = sorted(thesauri_files, key=lambda thesaurus_file: thesaurus_file.thesaurus_version)
    return thesauri_files


def _is_a_json_file(file: str):
    return file.endswith(".json")


if __name__ == "__main__":
    path_pddis_file = "./thesauri/2019_09/JSON/Thesaurus_09_2019.json"
    path_substances_file = "./thesauri/2019_09/JSON/index_des_substances_09_2019.json"

    all_thesaurus_files = thesauri_files()
    all_substances = AllSubstances(all_thesaurus_files)
    # all_substances.dump_substances_history("test.json")
    # all_substances.dump_unique_substances("substances.json")

    # drug_classes = [DrugClasses(substances) for substances in all_substances.all_substances]
    drug_classes = []
    for substances in all_substances.all_substances:
        print(substances.thesaurus_files.thesaurus_version)
        DrugClasses(substances)

