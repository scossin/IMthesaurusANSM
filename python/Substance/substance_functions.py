import re


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
