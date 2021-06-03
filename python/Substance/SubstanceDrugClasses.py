class SubstanceClass:

    def __init__(self, text):
        """

        :param text: content of a paragraph. Ex: trihexyphenidyle\nVoir : antiparkinsoniens anticholinergiques - médicaments atropiniques\n
        """
        self.substance = ""
        self.drug_classes = []
        self._extract_substance_and_families(text)

    def get_dic_representation(self):
        """

        :return: a dictionary representation of the instance
        """
        dic = {
            "substance": self.substance,
            "drug_classes": self.drug_classes
        }
        return dic

    def _extract_substance_and_families(self, text):
        """

        :param text: text extraction from a paragraph <p>text content</p> in the PDF document
        :return:
        """
        text_split = text.split("\n")
        self.substance = text_split[0]
        tokens = text_split[1:]
        normalized_tokens = map(self._normalize_text_split, tokens)
        normalized_tokens = list(filter(self._is_not_empty_string, normalized_tokens))
        # ['antihypertenseurs sauf alpha-bloquants - bradycardisants - bêta-bloquants (sauf esmolol et sotalol) - bêta-bloquants (sauf esmolol) - médicaments abaissant la',
        #  'pression artérielle']
        if len(normalized_tokens) != 0:
            families_string = " ".join(normalized_tokens)
            self.drug_classes = families_string.split(" - ")
        return None

    @staticmethod
    def _normalize_text_split(text_split_wo_substance: str) -> str:
        return text_split_wo_substance \
            .replace("Interactions en propre mais voir aussi :", "") \
            .replace("Interactions en propre seulement", "") \
            .replace("Voir :", "") \
            .strip()

    @staticmethod
    def _is_not_empty_string(string):
        return string != ""
