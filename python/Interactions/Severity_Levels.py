from collections import namedtuple

from python.Interactions.Exceptions import SeverityLevelerror

SeverityLevel = namedtuple("SeverityLevel", ["name", "number"])
SEVERITY_LEVELS = [
    SeverityLevel('CONTRE-INDICATION', 1),
    SeverityLevel('Association DECONSEILLEE', 2),
    SeverityLevel("Précaution d'emploi", 3),
    SeverityLevel('A prendre en compte', 4),
    SeverityLevel('Il convient de prendre en compte', 5),

    # SeverityLevel in the PDF document that contains multiple severity levels
    SeverityLevel('CI - ASDEC - APEC', 100),
    SeverityLevel('CI - ASDEC', 101),
    SeverityLevel('CI - PE', 102),
    SeverityLevel('ASDEC - PE', 103),
    SeverityLevel('ASDEC - APEC', 104)
]

Abbreviation = namedtuple("Abbreviations", ["short", "long"])
ABB_SEVERITY_LEVEL = [
    Abbreviation('CI', 'Contre-indication'),
    Abbreviation('ASDEC', 'Association déconseillée'),
    Abbreviation('PE', "Précaution d'emploi"),
    Abbreviation('APEC', "A prendre en compte")
]


def get_severity_levels_multiple():
    return [severity_level for severity_level in SEVERITY_LEVELS
            if _number_indicates_several_levels(severity_level.number)]


def contains_several_severity_levels(severity_level_name) -> bool:
    severity_level = get_severity_level(severity_level_name)
    return _number_indicates_several_levels(severity_level.number)


def get_severity_level(severity_level_name: str) -> SeverityLevel:
    severity_level = [severity_level for severity_level in SEVERITY_LEVELS
                      if severity_level.name == severity_level_name]
    if len(severity_level) == 0:
        raise SeverityLevelerror(f"Unfound severity_level {severity_level_name} in SEVERITY_LEVELS")
    if len(severity_level) != 1:
        raise SeverityLevelerror(f"multiple severity_levels {severity_level_name} in SEVERITY_LEVELS")
    return severity_level[0]


def get_abbreviation(short):
    abbreviation = [abbreviation for abbreviation in ABB_SEVERITY_LEVEL
                    if abbreviation.short == short]
    if len(abbreviation) == 0:
        raise SeverityLevelerror(f"Unfound shortForm {short} in abbreviation list")
    if len(abbreviation) != 1:
        raise SeverityLevelerror(f"multiple shortForm {short} in abbreviation lists")
    return abbreviation[0]


def get_abbreviations(severity_level: SeverityLevel) -> list:
    if not is_a_multiple_severity_level(severity_level):
        raise SeverityLevelerror("get_abbreviations is only used to extract long forms of multiple_severity_level"
                                 f"{severity_level.name} is a single severity level")
    short_forms = severity_level.name
    list_short_forms = short_forms.replace(" ", "").split("-")
    abbreviations = [abbreviation for abbreviation in ABB_SEVERITY_LEVEL
                     if abbreviation.short in list_short_forms]
    __check_all_abbreviations_retrieved(abbreviations, list_short_forms)
    return abbreviations


def __check_all_abbreviations_retrieved(abbreviations, list_short_forms):
    if len(abbreviations) != len(list_short_forms):
        raise SeverityLevelerror("failed to retrieve all abbreviations"
                                 f"shortforms asked: {list_short_forms}"
                                 f"abbreviations retrieved: {abbreviations}")


def is_a_multiple_severity_level(severity_level: SeverityLevel) -> bool:
    return _number_indicates_several_levels(severity_level.number)


def _number_indicates_several_levels(severity_level_number) -> bool:
    return severity_level_number >= 100
