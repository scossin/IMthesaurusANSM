import re
from collections import namedtuple
from python.Interactions.Exceptions import PDDIerror, PDDIdescriptionError, SeverityLevelerror
from python.Interactions.Severity_Levels import SEVERITY_LEVELS, SeverityLevel, is_a_multiple_severity_level, \
    get_abbreviations, Abbreviation

SeverityInformation = namedtuple("SeverityInformation", ["level", "info"])
SeverityLevelFinding = namedtuple("SeverityLevelFinding", ["num_line", "severity_line", "severity_level"])


class PDDI:

    def __init__(self, main_drug: str, plus_drug: str, between_main_and_plus_drug: str, description: list):
        self.main_drug = self._normalize_string(main_drug)
        self.plus_drug = self._normalize_string(plus_drug)
        self.between_main_and_plus_drug = between_main_and_plus_drug
        self.severity_levels: list
        self.interaction_mechanism: str
        self.description_string = "".join(description).strip()
        try:
            self._extract_interaction_information(description)
        except Exception as e:
            self.__handle_error(e)

    def __handle_error(self, e: Exception):
        print(f"{type(e).__name__} while extraction PDDI between {self.main_drug} and {self.plus_drug}")
        self.interaction_mechanism = str(e)
        self.severity_levels = []

    def get_dict_representation(self):
        severity_levels = [{"level": severity_info.level,
                            "info": severity_info.info}
                           for severity_info in self.severity_levels]
        return {
            "main_drug": self.main_drug,
            "between_main_and_plus_drug": self.between_main_and_plus_drug,
            "plus_drug": self.plus_drug,
            "severity_levels": severity_levels,
            "interaction_mechanism": self.interaction_mechanism,
            "description": self.description_string
        }

    def __str__(self):
        return f"{self.main_drug} can interact with {self.plus_drug}" \
               f"The severity levels are {self.severity_levels}" \
               f"The mechanism of the interaction is {self.interaction_mechanism}"

    def _extract_interaction_information(self, description: list):
        for num_line, line in enumerate(description):
            severity_level_found = [SeverityLevelFinding(num_line, line, severity_level)
                                    for severity_level in SEVERITY_LEVELS
                                    if line.startswith(severity_level.name)]
            if len(severity_level_found) != 0:
                break  # why to break here? There is only one severity level description per PDDI
                # although the description "CI - ASDEC - PEC" refers to several severity levels
                # the class considers "CI - ASDEC - PEC" to be only one severity level here
                # the several levels in "CI - ASDEC - PEC" will be extracted below

        if len(severity_level_found) == 0:  # there is only one severity level and it MUST exist (or I didn't detected it)
            raise PDDIdescriptionError(f"no severity level detected in this description: "
                                       f"{description}")

        severity_level_found = severity_level_found[0]

        if is_a_multiple_severity_level(severity_level_found.severity_level):
            self.__several_severity_levels_info_extract(severity_level_found, description)
        else:
            self.__single_severity_level_info_extract(severity_level_found, description)

    def __several_severity_levels_info_extract(self, severity_level_found, description):
        description_string = "SEP".join(description)
        abbreviations = get_abbreviations(severity_level_found.severity_level)
        previous_end_at = None
        severity_infos = []
        match_results = [self.__search_long_form(abbreviation, description_string) for abbreviation in
                         abbreviations]
        for match in match_results:
            if previous_end_at is not None:
                severity_infos.append(description_string[previous_end_at:match.start(0)])
            previous_end_at = match.end(0)
        last_part = description_string[previous_end_at:len(description_string)]
        tuple_last_part = tuple(last_part.split("\nSEP\nSEP"))
        if len(tuple_last_part) < 2:
            raise PDDIdescriptionError(f"can't find last course of action and mechanism of interaction in {last_part}"
                                       f"extracted from this pddi description: {description}")
        last_course_of_action = tuple_last_part[0]  # avec :\n- le vérapamil per os\nSurveillance clinique et ECG.'
        interaction_mechanism = "".join(tuple_last_part[1:])  # one or multiple lines
        severity_infos.append(last_course_of_action)
        self.interaction_mechanism = interaction_mechanism.replace("SEP", "").strip()
        severity_infos = [severity_info.replace("SEP", "").strip() for severity_info in severity_infos]
        self.severity_levels = [self.__get_dict_severity_level(abbreviation.severity_level, severity_info)
                                for (abbreviation, severity_info) in zip(abbreviations, severity_infos)]

    @staticmethod
    def __search_long_form(abbreviation: Abbreviation, description_string):
        match_results = list(re.finditer(abbreviation.long, description_string, re.IGNORECASE))
        if len(match_results) == 0:
            raise SeverityLevelerror(f"failed to find severity level {abbreviation} in this description content:"
                                     f"{description_string}")
        if len(match_results) > 1:
            raise SeverityLevelerror(f"several severity level of {abbreviation} found in this description content:"
                                     f"{description_string}")
        return match_results[0]

    @staticmethod
    def __get_dict_severity_level(severity_level: SeverityLevel, severity_info: str) -> SeverityInformation:
        return SeverityInformation(severity_level.name, severity_info)

    def __single_severity_level_info_extract(self, severity_level_found, description) -> None:
        severity_line = severity_level_found.severity_line
        severity_level = severity_level_found.severity_level
        if self.__description_begins_right_2_severity_level(severity_line, severity_level):
            # in this case severity_info is empty and the remaining information is about the interaction_mechanism
            severity_info = ""
            self.severity_levels = [self.__get_dict_severity_level(severity_level, severity_info)]
            normalized_description = list(filter(self.line_is_not_empty, description))
            interaction_mechanism = "".join(normalized_description)
            interaction_mechanism = PDDI.__remove_severity_level(interaction_mechanism,
                                                                 severity_level)
            self.interaction_mechanism = interaction_mechanism

        else:
            # in this case severity_info is next_line and mechanism follows
            num_line_begins_severity_info = severity_level_found.num_line + 1
            severity_info_lines = self.__extract_severity_info_lines(description, num_line_begins_severity_info)
            severity_info = "".join(severity_info_lines)
            self.severity_levels = [self.__get_dict_severity_level(severity_level, severity_info)]
            lines_below_course_of_action = description[(num_line_begins_severity_info + len(severity_info_lines)):]
            self.interaction_mechanism = "".join(lines_below_course_of_action).strip()

    @classmethod
    def line_is_not_empty(cls, line: str) -> None:
        return line.strip() != ""

    @staticmethod
    def _normalize_string(string: str):
        return string.strip().replace("+ ", "").strip()

    @staticmethod
    def __extract_severity_info_lines(description: list, next_line: int) -> list:
        PDDI.__check_next_line_exists(next_line, description)
        course_of_action_lines = []
        for line in description[next_line:]:
            if line == "\n":  # next in the mechanism of action
                break
            normalized_line = line.strip()
            course_of_action_lines.append(normalized_line)
        return course_of_action_lines

    @staticmethod
    def __check_next_line_exists(next_line: int, description: str) -> None:
        if next_line > (len(description) - 1):  # -1 because of 0 index
            raise PDDIerror(f"expecting to find course_of_action next line ({next_line})"
                            "in description: {description}"
                            "but this line doesn't exist !")

    @staticmethod
    def __description_begins_right_2_severity_level(severity_line: str, severity_level: SeverityLevel) -> bool:
        """
        Examples:
        :param severity_line: Association DECONSEILLEEMajoration des effets indésirables, et notamment de l'acidose
        :param severity_level: Association DECONSEILLEE
        :return: True if, when we remove severity level in severity_line, something remains
        """
        what_remain = PDDI.__remove_severity_level(severity_line, severity_level)
        if what_remain == "":
            return False
        else:
            return True

    @staticmethod
    def __remove_severity_level(string: str, severity_level: SeverityLevel) -> str:
        return string.replace(severity_level.name, " ").strip()
