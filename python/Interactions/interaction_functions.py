import re
from enum import Enum
import unidecode

from python.Interactions.Exceptions import MainDrugError
from python.Substance.Exceptions import SubstanceNotFound


def get_index_first_entry(all_lines: list, entry: str) -> int:
    """

    :param all_lines: list
    :param entry: string of the first substance
    :return: the index of the string that begins with that substance
    """

    max_index_to_search = 100
    text_start_by_substance = [text.startswith(entry) for text in all_lines[0:max_index_to_search]]
    if not any(text_start_by_substance):
        raise SubstanceNotFound(f"No line starts with {entry}")
    if sum(text_start_by_substance) != 1:
        raise ValueError(f" multiple paragraph elements starts with {entry}, expecting only one occurence")
    index_first_entry = text_start_by_substance.index(True)
    return index_first_entry


def is_a_line_2_ignore(text):
    if _is_metadata(text):
        return True
    return False


def _is_metadata(text) -> bool:
    patterns = ["Page", "ANSM", "Thesaurus", "www", "^[0-9]"]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match is not None:
            return True
    return False


class LineTag(Enum):
    MAIN_DRUG = 1
    PLUS_DRUG = 2
    OTHER = 3


class Patterns:
    pattern_main_drug = "^[A-Z]{2,}"
    re_main_drug = re.compile(pattern_main_drug)

    pattern_lower_case = "[a-z]"
    re_lower_case = re.compile(pattern_lower_case)


def _line_matched_main_drug(line: str) -> bool:
    # a main_drug can't contain any lower_case character
    match_lower_case = Patterns.re_lower_case.search(line)
    if match_lower_case:
        return False

    unaccented_line = unidecode.unidecode(line)
    match = Patterns.re_main_drug.search(unaccented_line)
    if match is None:
        return False
    matched = match.group(0)
    if _is_a_line_to_ignore(matched, unaccented_line):
        return False
    return True


def _is_a_severity_level_line(string: str) -> bool:
    if string in ["CONTRE", "CONTREINDICATION", "CI", "ASDEC", "PE", "ASPEC"]:
        return True
    else:
        return False


def _is_a_line_to_ignore(matched: str, unaccented_line: str) -> bool:
    # in the PDF we have a very special case:
    # ANTIVITAMINES K
    # ANTI-INFECTIEUX ET HEMOSTASE (to talk about ANTIVITAMINES K and ANTI-INFECTIEUX ET HEMOSTASE)
    # AVK et INR (to talk about surveillance of INR when patient takes AVK)
    if unaccented_line.startswith("ANTI-INFECTIEUX ET HEMOSTASE"):
        return True
    if unaccented_line.startswith("AVK et INR"):
        return True
    # in 2016
    if unaccented_line.startswith("ANTI-INFECTIEUX ET INR"):
        return True

    # CYP3A4: interaction description goes to the line and CYP3A4 appears but it's not a main_drug
    if unaccented_line.startswith("CYP3A4"):
        return True

    if _is_a_severity_level_line(matched):
        return True

    return False


def _line_matched_plus_drug(line: str) -> bool:
    return line[0:2] == "+ "


def detect_line_tag(line: str) -> LineTag:
    if _line_matched_main_drug(line):
        return LineTag.MAIN_DRUG
    elif _line_matched_plus_drug(line):
        return LineTag.PLUS_DRUG
    else:
        return LineTag.OTHER


def check_main_drugs_are_ordered(main_drugs: str) -> None:
    """
    In the PDF document, main_drugs are ordered alphabetically.
    We can check main_drugs are ordered to find element in main_drugs that shouldn't be here.
    :param main_drugs: list of ordered drugs (main entry) in the PDF document
    :return: Raise an error if main_drugs are not ordered. Else return None
    """
    # why I take the first 2 characters and not the full chain of characters ??
    # The drugs are ordered alphabetically in the PDF document but the way the sorted function works is different
    # For example, in the PDF: "ANTIARYTHMIQUES" "ANTI-TNF ALPHA" are switched because sorted place "ANTI-TNF ALPHA" before "ANTIARYTHMIQUES"
    # So the creators of the thesaurus didn't make the same order choice
    first_char_main_drug = [main_drug[0:2] for main_drug in main_drugs]
    unaccented_first_char = [unidecode.unidecode(first_char) for first_char in first_char_main_drug]
    unaccented_sorted = sorted(unaccented_first_char)
    # if sorted doesn't change any element then the 2 arrays are equals
    if unaccented_first_char != unaccented_sorted:
        combined = zip(unaccented_first_char, unaccented_sorted)
        messages = [f"{main_drug} != {main_drug_2}" for (main_drug, main_drug_2) in combined
                    if main_drug != main_drug_2]
        raise MainDrugError("Main drugs are not ordered "
                            "possibly because the algorithm failed to remove some irrelevant entries"
                            " The files produced in DEBUG_MODE must be checked"
                            f" An error occured near {messages[0]}")
    else:
        return None


def fix_specific_lines_before_extraction(line: str) -> str:
    fix_lined = _fix_ADSORBANTS(line)
    return fix_lined


def _fix_ADSORBANTS(line: str):
    # There is a Tika extraction error we fix here for this therapeutic class:
    # SUBSTANCES À ABSORPTION RÉDUITE PAR LES TOPIQUES GASTRO-INTESTINAUX, ANTIACIDES ET
    # ADSORBANTS (we shouldn't have a new line here)
    if line.strip().endswith("ANTIACIDES ET"):  # line: ...GASTRO-INTESTINAUX, ANTIACIDES ET \n
        return line.strip() + " ADSORBANTS"
    if line.startswith("ADSORBANTS"):
        return ""
    return line
