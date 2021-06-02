from bs4 import BeautifulSoup
from python.substance_functions import get_index_first_substance, is_a_paragraph_2_ignore, __is_empty_paragraph
import json


def _normalize_text_split(text_split_wo_substance):
    return text_split_wo_substance \
        .replace("Interactions en propre mais voir aussi :", "") \
        .replace("Interactions en propre seulement", "") \
        .replace("Voir :", "") \
        .strip()


def _is_not_empty_string(string):
    return string != ""


class SubstanceFamille:

    def __init__(self, text):
        """

        :param text: content of a paragraph. Ex: trihexyphenidyle\nVoir : antiparkinsoniens anticholinergiques - médicaments atropiniques\n
        """
        self.substance = ""
        self.drug_classes = []
        self._extract_substance_and_families(text)

    def _extract_substance_and_families(self, text):
        text_split = text.split("\n")
        self.substance = text_split[0]
        tokens = text_split[1:]
        normalized_tokens = map(_normalize_text_split, tokens)
        normalized_tokens = list(filter(_is_not_empty_string, normalized_tokens))
        # ['antihypertenseurs sauf alpha-bloquants - bradycardisants - bêta-bloquants (sauf esmolol et sotalol) - bêta-bloquants (sauf esmolol) - médicaments abaissant la',
        #  'pression artérielle']
        if len(normalized_tokens) != 0:
            families_string = " ".join(normalized_tokens)
            self.drug_classes = families_string.split(" - ")
        return None

    def get_dic_representation(self):
        dic = {
            "substance": self.substance,
            "drug_classes": self.drug_classes
        }
        return dic


if __name__ == "__main__":
    filename = '../R/092019/TXT/index_substances092019.txt'
    with open(filename) as fp:
        soup = BeautifulSoup(fp, "html.parser")
        p_elements = soup.select('.page > p')
        print(f"{len(p_elements)} paragraphs elements detected")

        p_text = [p.get_text() for p in p_elements]

        first_substance = "abatacept"
        index_first_substance = get_index_first_substance(p_text, first_substance)
        print(f" first substance: {first_substance} detected at index {index_first_substance}")
        p_text = p_text[index_first_substance:]

        index_2_ignore = list(map(is_a_paragraph_2_ignore, p_text))
        print(f"{sum(index_2_ignore)} empty paragraphs or metadata detected and removed")
        p_text = [text for (text, ignored) in zip(p_text, index_2_ignore) if not ignored]

        substances = [SubstanceFamille(text) for text in p_text]
        json_substances = [substance.get_dic_representation() for substance in substances]
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(json_substances, f, ensure_ascii=False, indent=4)
