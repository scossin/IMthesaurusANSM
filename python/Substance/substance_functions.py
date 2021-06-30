import re
from typing import List


def remove_wrong_p_tag(all_lines: List[str]) -> None:
    line_has_wrong_type = list(map(_line_start_by_wrong_tag, all_lines))
    wrong_lines_number = _get_wrong_lines_number(line_has_wrong_type)
    for i in wrong_lines_number:
        _remove_tag_previous_line(all_lines, i)
        _remove_tag_current_line(all_lines, i)


def _line_start_by_wrong_tag(line) -> bool:
    return _line_starts_by_Interaction(line) or _line_starts_by_Voir(line)


def _remove_tag_previous_line(all_lines, i) -> None:
    previous_line_number = i - 1
    line = all_lines[previous_line_number]
    line = line.replace("</p>", "")  # closing tag of a paragraph containing a molecule name
    all_lines[previous_line_number] = line
    return


def _remove_tag_current_line(all_lines, i) -> None:
    line = all_lines[i]
    line = line.replace("<p>", "")  # closing tag of a paragraph containing a molecule name
    all_lines[i] = line
    return


def _get_wrong_lines_number(line_has_wrong_type: List[bool]) -> List[int]:
    wrong_lines_number = []
    for i, true_or_false in enumerate(line_has_wrong_type):
        if true_or_false:
            wrong_lines_number.append(i)
    return wrong_lines_number


def _line_starts_by_Interaction(line: str) -> bool:
    return line.startswith("<p>Interactions en propre")


def _line_starts_by_Voir(line: str) -> bool:
    return line.startswith("<p>Voir :")


def is_a_paragraph_2_ignore(text: str) -> bool:
    if __is_empty_paragraph(text):
        return True
    if __is_metadata(text):
        return True
    return False


def __is_metadata(text: str) -> bool:
    patterns = ["[^a-z]?page[^a-z]", "ANSM", "[^a-z]Version[^a-z]", "www"]
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


def fix_specific_lines_before_extraction(line: str) -> str:
    fix_lined = _fix_RACECADOTRIL(line)
    return fix_lined


def _fix_RACECADOTRIL(line: str):
    # there is a typo in thesaurus version 2015_06
    if line.strip().endswith("cadodril"):
        line = line.replace("cadodril", "cadotril")
    return line
