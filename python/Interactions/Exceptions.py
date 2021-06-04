class MainDrugError(Exception):
    pass


class PDDIerror(Exception):
    pass


class PlusDrugUnfounderror(PDDIerror):
    pass


class PDDIdescriptionError(PDDIerror):
    pass


class SeverityLevelerror(Exception):
    pass
