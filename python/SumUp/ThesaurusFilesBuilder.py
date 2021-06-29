import os
import pathlib
from typing import List

from python.SumUp.ThesaurusFiles import ThesaurusFiles


class ThesaurusFilesBuilder:
    def __init__(self):
        pass

    @classmethod
    def thesauri_files(cls) -> List[ThesaurusFiles]:
        current_dir = pathlib.Path(__file__).parent.absolute()
        path_thesauri = str(current_dir) + "/../../thesauri"
        thesauri_files = []
        for root, subdirs, files in os.walk(path_thesauri):
            json_files = list(filter(cls._is_a_json_file, files))
            new_thesaurus_files = cls.__create_thesaurus_files(root, json_files)
            thesauri_files.append(new_thesaurus_files)
        thesauri_files: List[ThesaurusFiles] = [thesaurus_files for thesaurus_files in thesauri_files
                                                if thesaurus_files is not None]
        [thesaurus_files.check_files() for thesaurus_files in thesauri_files]
        thesauri_files = sorted(thesauri_files, key=lambda thesaurus_file: thesaurus_file.thesaurus_version)
        return thesauri_files

    @classmethod
    def __create_thesaurus_files(cls, root, json_files) -> ThesaurusFiles:
        if len(json_files) == 0:
            return None
        thesaurus_file = ThesaurusFiles(root)
        [thesaurus_file.add_json_file(json_file) for json_file in json_files]
        return thesaurus_file

    @classmethod
    def _is_a_json_file(cls, file: str):
        return file.endswith(".json")
