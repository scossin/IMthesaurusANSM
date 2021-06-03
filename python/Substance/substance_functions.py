import re

from python.Substance.Exceptions import SubstanceNotFound


def get_index_first_substance(p_text, substance):
    """

    :param p_text: a list of string (text of paragraph elements in html)
    :param substance: string of the first substance
    :return: the index of the string that begins with that substance
    """

    text_start_by_substance = [text.startswith(substance) for text in p_text]
    if not any(text_start_by_substance):
        raise SubstanceNotFound(f"No paragraph element starts with {substance}")
    if sum(text_start_by_substance) != 1:
        raise ValueError(f" multiple paragraph elements starts with {substance}, expecting only one occurence")
    index_first_substance = text_start_by_substance.index(True)
    return index_first_substance


def is_a_paragraph_2_ignore(text):
    if __is_empty_paragraph(text):
        return True
    if __is_metadata(text):
        return True
    return False


def __is_metadata(text):
    patterns = ["Page", "ANSM", "Version", "www"]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match is not None:
            return True
    return False


def __is_empty_paragraph(text):
    normalized_text = text.strip()
    if normalized_text == "":
        return True
    return False
