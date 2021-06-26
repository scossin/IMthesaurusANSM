class ThesaurusFiles:
    """
    Store the substance and the thesaurus file of a thesaurus version
    """

    def __init__(self, root_folder):
        self.thesaurus_version: str = self.get_thesaurus_version(root_folder)
        self.root_folder = root_folder
        self.substance_file: str = ""
        self.thesaurus_file: str = ""

    def get_substance_file_path(self):
        return self.root_folder + "/" + self.substance_file

    def get_thesaurus_file_path(self):
        return self.root_folder + "/" + self.thesaurus_file

    @staticmethod
    def get_thesaurus_version(root_folder):
        thesaurus_version = root_folder.replace("./thesauri/", "").replace("/JSON", "")
        return thesaurus_version

    def add_json_file(self, json_file):
        if self._is_a_substance_file(json_file):
            self.substance_file = json_file
        elif self._is_a_thesaurus_file(json_file):
            self.thesaurus_file = json_file
        else:
            raise TypeError(f"{json_file} is not a thesaurus or a substance file")

    def _is_a_substance_file(self, file: str) -> bool:
        return self._contains_substance(file)

    def _is_a_thesaurus_file(self, file: str) -> bool:
        return self._contains_thesaurus(file)

    @staticmethod
    def _contains_substance(file: str) -> bool:
        return "substance" in file or "Substance" in file

    @staticmethod
    def _contains_thesaurus(file: str) -> bool:
        return "thesaurus" in file or "Thesaurus" in file

    def check_files(self):
        self.check_file(self.thesaurus_file, "thesaurus_file")
        self.check_file(self.substance_file, "substance_file")

    def check_file(self, json_file, filename):
        if json_file == "":
            raise TypeError(f"{filename} of thesaurus version {self.thesaurus_version} was not set")


def create_thesaurus_files(root, json_files) -> ThesaurusFiles:
    if len(json_files) == 0:
        return None
    thesaurus_file = ThesaurusFiles(root)
    [thesaurus_file.add_json_file(json_file) for json_file in json_files]
    return thesaurus_file
