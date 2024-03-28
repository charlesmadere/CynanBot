from CynanBot.timber.timberInterface import TimberInterface


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
        print(f'{tag} — {msg}')
