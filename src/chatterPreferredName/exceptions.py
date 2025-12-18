class ChatterPreferredNameFeatureIsDisabledException(Exception):

    pass


class ChatterPreferredNameIsInvalidException(Exception):

    def __init__(self, message: str):
        super().__init__(message)
