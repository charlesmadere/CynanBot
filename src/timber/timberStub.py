from .timberInterface import TimberInterface


class TimberStub(TimberInterface):

    def __init__(self):
        pass

    def log(
        self,
        tag: str,
        msg: str,
        exception: Exception | None = None,
        traceback: str | None = None
    ):
        if exception is None:
            print(f'{tag} — {msg}')
        else:
            print(f'{tag} — {msg} — {exception}')

    def start(self):
        pass
