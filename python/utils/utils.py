from text_unidecode import unidecode


class Utils:
    @classmethod
    def remove_accents_and_lower_case(cls, string: str) -> str:
        lower_string = string.lower()
        unaccented_lower_string = cls.remove_accents(lower_string)
        return unaccented_lower_string

    @classmethod
    def remove_accents(cls, string):
        unaccented_string = unidecode(string)
        return unaccented_string
