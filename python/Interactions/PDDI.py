from collections import namedtuple
from python.Interactions.Exceptions import PDDIerror
from python.Interactions.Severity_Levels import SEVERITY_LEVELS


class PDDI:

    def __init__(self, main_drug: str, plus_drug: str, description: list):
        self.main_drug = self.normalize_string(main_drug)
        self.plus_drug = self.normalize_string(plus_drug)
        self.severity_level = ""
        self.interaction_mechanism = ""
        self.course_of_action = ""
        self.extract_interaction_information(description)

    def get_dict_representation(self):
        return {
            "main_drug": self.main_drug,
            "plus_drug": self.plus_drug,
            "severity_level": self.severity_level,
            "course_of_action": self.course_of_action,
            "interaction_mechanism": self.interaction_mechanism
        }

    def __str__(self):
        return f"{self.main_drug} can interact with {self.plus_drug}" \
               f"The severity level is {self.severity_level}" \
               f"The mechanism of the interaction is {self.interaction_mechanism}" \
               f"The course of action is {self.course_of_action}"

    @staticmethod
    def normalize_string(string: str):
        return string.strip().replace("+ ", "")

    def extract_interaction_information(self, description: list):
        SeverityInfo = namedtuple("SeverityInfo", ["num_line", "severity_line", "severity_level"])

        for num_line, line in enumerate(description):
            severity_info = [SeverityInfo(num_line, line, severity_level.name)
                             for severity_level in SEVERITY_LEVELS
                             if line.startswith(severity_level.name)]
            if len(severity_info) != 0:
                break  # why to break here? There is only one severity level description per PDDI
                # although the description "CI - ASDEC - PEC" refers to several severity level
                # the class considers "CI - ASDEC - PEC" to be only one severity level
                # the several levels in "CI - ASDEC - PEC" will be extracted later

        if len(severity_info) == 0:  # there is only one severity level and it MUST exist (or I didn't detected it)
            raise PDDIerror(f"no severity level detected in this description: "
                            f"{description}")

        severity_info = severity_info[0]
        self.severity_level = severity_info.severity_level
        severity_line = severity_info.severity_line

        if self.__description_begins_right_2_severity_level(severity_line, self.severity_level):
            # in this case course_of_action is empty, it's empty and the remaining information is about the interaction_description
            self.course_of_action = ""
            normalized_description = list(filter(self.line_is_not_empty, description))
            interaction_mechanism = "".join(normalized_description)
            interaction_mechanism = PDDI.__remove_severity_level(interaction_mechanism,
                                                                 self.severity_level)
            self.interaction_mechanism = interaction_mechanism

        else:
            # in this case course_of_action is next_line and mechanism follows
            num_line_begins_course_of_action = severity_info.num_line + 1
            course_of_action_lines = self.__extract_course_of_action_lines(description,
                                                                           num_line_begins_course_of_action)
            self.course_of_action = "".join(course_of_action_lines)

            lines_below_course_of_action = description[(num_line_begins_course_of_action +
                                                        len(course_of_action_lines)):]
            self.interaction_mechanism = self.__extract_interaction_mechanism(lines_below_course_of_action)

    @staticmethod
    def __extract_interaction_mechanism(lines: list):
        # lines_not_empty = list(filter(PDDI.line_is_not_empty, lines))
        # normalized_lines_not_empty = [line.strip() for line in lines_not_empty]
        return "".join(lines).strip()

    @staticmethod
    def __extract_course_of_action_lines(description: list, next_line: int) -> list:
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

    @classmethod
    def line_is_not_empty(cls, line: str) -> None:
        return line.strip() != ""

    @staticmethod
    def __description_begins_right_2_severity_level(severity_line, severity_level):
        """
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
    def __remove_severity_level(string, severity_level):
        return string.replace(severity_level, " ").strip()
