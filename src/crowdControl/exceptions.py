class ActionHandlerProcessCantBeConnectedToException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class ActionHandlerProcessNotFoundException(Exception):

    def __init__(self, message: str):
        super().__init__(message)
