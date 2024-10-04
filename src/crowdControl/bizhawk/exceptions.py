from ..exceptions import ActionHandlerProcessNotFoundException


class BizhawkProcessNotFoundException(ActionHandlerProcessNotFoundException):

    def __init__(self, message: str):
        super().__init__(message)
