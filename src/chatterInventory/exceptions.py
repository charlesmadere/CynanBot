class ChatterInventoryIsDisabledException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class UnknownChatterItemTypeException(Exception):

    def __init__(self, message: str):
        super().__init__(message)
