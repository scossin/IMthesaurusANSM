from collections import namedtuple

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


def get_severity_levels_multiple():
    return [severityLevel for severityLevel in SEVERITY_LEVELS
            if severityLevel.number >= 100]
