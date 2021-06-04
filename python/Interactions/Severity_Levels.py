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

Abbreviations = namedtuple("Abbreviations", ["short", "long"])
ABB_SEVERITY_LEVEL = [
    Abbreviations('CI', 'Contre-indication'),
    Abbreviations('ASDEC', 'Association déconseillée'),
    Abbreviations('PE', "Précaution d'emploi"),
    Abbreviations('APEC', "A prendre en compte")
]


def get_severity_levels_multiple():
    return [severityLevel for severityLevel in SEVERITY_LEVELS
            if severityLevel.number >= 100]


def get_long_forms(short):
    abbreviation = [abbreviation for abbreviation in ABB_SEVERITY_LEVEL
                    if abbreviation.short == short]
    if len(abbreviation) == 0:
        raise SeverityLevelerror(f"Unfound shortForm {short} in abbreviation list")
    if len(abbreviation) != 1:
        raise SeverityLevelerror(f"multiple shortForm {short} in abbreviation lists")
    return abbreviation[0].long


