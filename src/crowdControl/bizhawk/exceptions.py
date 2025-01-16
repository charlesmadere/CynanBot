from ..exceptions import ActionHandlerProcessCantBeConnectedToException, ActionHandlerProcessNotFoundException


class BizhawkProcessCantBeConnectedTo(ActionHandlerProcessCantBeConnectedToException):

    def __init__(self, message: str):
        super().__init__(message)


class BizhawkProcessNotFoundException(ActionHandlerProcessNotFoundException):

    def __init__(self, message: str):
        super().__init__(message)
