from collections import namedtuple

from python.Interactions.Exceptions import PDDIerror
from python.Interactions.interaction_functions import get_index_first_entry, is_a_line_2_ignore, detect_line_tag, \
    LineTag, check_main_drugs_are_ordered


def writeDebugFile(input_file, lines, step_number):
    debug_filename = __get_debug_file_name(input_file, step_number)
    with open(debug_filename, 'w') as f:
        for line in lines:
            f.write(line)


def __get_debug_file_name(intput_file, step_number):
    debug_filename = intput_file.replace(".txt", "") + "__" + str(step_number) + ".txt"
    return debug_filename


class DrugPDDIs:
    """
    Potential Drug-Drug Interactions (PDDI) of a drug.
    Example:

    ABATACEPT (main_drug)
    + ANTI-TNF ALPHA (plus_drug)
        Association DECONSEILLEEMajoration de l’immunodépression.

    + VACCINS VIVANTS ATTÉNUÉS (plus_drug)
        Association DECONSEILLEE
        ainsi que pendant les 3 mois suivant l'arrêt du traitement.

    The goal of this class is to extract each PDDI (ex: ABATACEPT + ANTI-TNF ALPHA)
    """

    def __init__(self, pddi_text: list):
        """

        :param pddi_text: a section containing a main_drug and the descriptions of potential drug interaction
        """
        self.__check_pddi_text(pddi_text)
        self.main_drug = pddi_text[0]
        self.interact_with = pddi_text[1:]
        self.pddis = []
        self.extract_each_pddi(pddi_text)

    @staticmethod
    def __check_pddi_text(pddi_text) -> None:
        if not isinstance(pddi_text, list):
            raise TypeError("pddi_text is not a list")
        if len(pddi_text) == 0:
            raise PDDIerror("PDDI text content is empty")
        main_drug = pddi_text[0]
        if len(pddi_text) == 1:
            raise PDDIerror(f"PDDI text content contains only main_drug {main_drug}, "
                            f"nothig else")
        return None

    def extract_each_pddi(self, pddi_text):
        tags = [detect_line_tag(line) for line in pddi_text]
        indices_plus_drug = [index for (index, tag) in enumerate(tags)
                             if tag == LineTag.PLUS_DRUG]
        self.__check_index_plus_drug(indices_plus_drug)

        self.pddis = [None] * len(indices_plus_drug)
        for i, index in enumerate(indices_plus_drug[1:]):
            previous_index = indices_plus_drug[i]
            pddi_description = pddi_text[previous_index:index]
            self.__check_pddi_description(pddi_description)
            plus_drug = pddi_description[0]
            description = pddi_description[1:]
            self.pddis[i] = PDDI(self.main_drug,
                                 plus_drug,
                                 description)

    def __check_index_plus_drug(self, index_plus_drug):
        if len(index_plus_drug) == 0:
            raise PDDIerror(f"no PDDI found for drug {self.main_drug}")

    def __check_pddi_description(self, pddi_description):
        if len(pddi_description) == 0:
            raise PDDIerror(f"no PDDI found for drug {self.main_drug}")
        if len(pddi_description) == 1:
            raise PDDIerror(f"no PDDI description found for drug {self.main_drug}"
                            f" that can interact with {pddi_description}")

    def __str__(self) -> str:
        interact_with_text = "".join(self.interact_with)
        return f"PDDI: {self.main_drug} can interact with: {interact_with_text}"


class PDDI:
    SEVERITY_LEVELS = ["CONTRE-INDICATION",
                       "Association DECONSEILLEE",
                       "Précaution d'emploi",
                       "A prendre en compte",
                       "CI"
                       "ASDEC",
                       "APEC"
                       ]

    def __init__(self, main_drug: str, plus_drug: str, description: list):
        self.main_drug = self.normalize_string(main_drug)
        self.plus_drug = self.normalize_string(plus_drug)
        self.severity_level = ""
        self.interaction_mechanism = ""
        self.course_of_action = ""
        self.extract_interaction_information(description)

    def __str__(self):
        return f"{self.main_drug} can interact with {self.plus_drug}" \
               f"The severity level is {self.severity_level}" \
               f"The mechanism of the interaction is {self.interaction_mechanism}" \
               f"The course of action is {self.course_of_action}"

    @staticmethod
    def normalize_string(string: str):
        return string.strip().replace("+ ", "")

    def extract_interaction_information(self, description: list):
        SeverityInfo = namedtuple("SeverityInfo", ["i", "severity_line", "severity_level"])

        for i, line in enumerate(description):
            severity_info = [SeverityInfo(i, line, severity_level)
                             for severity_level in PDDI.SEVERITY_LEVELS
                             if line.startswith(severity_level)]
            if len(severity_info) != 0:
                break  # why to break here? There is only one severity level description per PDDI
                # although the description "CI - ASDEC - PEC" refers to several severity level
                # the class considers "CI - ASDEC - PEC" to be only one severity level
                # the several levels in "CI - ASDEC - PEC" will be extracted later

        if len(severity_info) == 0:  # there is only one severity level and it MUST exist (or I didn't detected it)
            raise PDDIerror(f"no severity level detected in this description: "
                            f"{description}")

        self.severity_level = severity_info[0].severity_level
        severity_line = severity_info[0].severity_line
        i = severity_info[0].i

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
            next_line = i + 1
            course_of_action_lines = PDDI.__extract_course_of_action_lines[description, next_line]
            self.course_of_action = "".join(course_of_action_lines)

            below_course_of_action = description[(i + len(course_of_action_lines)):]
            self.interaction_mechanism = PDDI.__extract_mechanism_of_interaction(below_course_of_action)

    @staticmethod
    def __extract_mechanism_of_interaction(lines: list):
        lines_not_empty = list(filter(PDDI.line_is_not_empty, lines))
        return "".join(lines_not_empty)

    @staticmethod
    def __extract_course_of_action_lines(description, next_line):
        PDDI.__check_next_line_exists(next_line, description)
        course_of_action_line = []
        for line in description[next_line:]:
            if line == "\n":  # next in the mechanism of action
                break
            course_of_action_line.append(line)
        return course_of_action_line

    @staticmethod
    def __check_next_line_exists(next_line: int, description: str) -> None:
        if next_line > (len(description) - 1):  # -1 because of 0 index
            raise PDDIerror(f"expecting to find course_of_action next line ({next_line})"
                            "in description: {description}"
                            "but this line doesn't exist !")

    @staticmethod
    def line_is_not_empty(line: str) -> None:
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


if __name__ == "__main__":
    input_file = "R/092019/TXT/thesaurus_092019.txt"
    with open(input_file) as fp:
        DEBUG_MODE = True
        all_lines = fp.readlines()
        index_first_entry = get_index_first_entry(all_lines, "ABATACEPT")
        all_lines = all_lines[index_first_entry:]

        if DEBUG_MODE:
            writeDebugFile(input_file, all_lines, 1)

        lines_filtered = filter(lambda x: not is_a_line_2_ignore(x), all_lines)
        lines_filtered = list(lines_filtered)

        if DEBUG_MODE:
            writeDebugFile(input_file, lines_filtered, 2)

        tags = [detect_line_tag(line) for line in lines_filtered]
        tagged_lines = zip(tags, lines_filtered)
        main_drugs = [line for (tag, line) in tagged_lines
                      if tag == LineTag.MAIN_DRUG]
        if DEBUG_MODE:
            writeDebugFile(input_file, list(main_drugs), 3)
        print(f"checking main_drugs are ordered...")
        check_main_drugs_are_ordered(main_drugs)

        indices_main_drugs = [index for (index, tag) in enumerate(tags)
                              if tag == LineTag.MAIN_DRUG]

        pddis = [None] * len(indices_main_drugs)
        for i, index in enumerate(indices_main_drugs[1:]):
            previous_index = indices_main_drugs[i]
            pddi_text = lines_filtered[previous_index:index]
            pddis[i] = DrugPDDIs(pddi_text)
