class CheerActionAlreadyExistsException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class TimeoutDurationSecondsTooLongException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class TooManyCheerActionsException(Exception):

    def __init__(self, message: str):
        super().__init__(message)
