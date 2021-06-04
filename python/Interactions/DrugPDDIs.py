from python.Interactions.Exceptions import PDDIerror, PDDIdescriptionError, PlusDrugUnfounderror
from python.Interactions.PDDI import PDDI
from python.Interactions.interaction_functions import detect_line_tag, LineTag


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
        # the last "plus_drug" information is located from the last indice_plus_drug to the end of pddi_text
        indices_2_iterate_to = indices_plus_drug + [len(pddi_text)]
        for i, index in enumerate(indices_2_iterate_to[1:]):
            previous_index = indices_2_iterate_to[i]
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
            raise PlusDrugUnfounderror(f"no plus_drug found to interact with {self.main_drug}")
        if len(pddi_description) == 1:
            raise PDDIdescriptionError(f"no PDDI description found for drug {self.main_drug}"
                                       f" that can interact with {pddi_description}")

    def __str__(self) -> str:
        interact_with_text = "".join(self.interact_with)
        return f"PDDI: {self.main_drug} can interact with: {interact_with_text}"
