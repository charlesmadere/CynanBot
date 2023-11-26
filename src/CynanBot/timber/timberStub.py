from typing import Optional

from CynanBot.timber.timberInterface import TimberInterface


class TimberStub(TimberInterface):

    def __init__(self):
        pass

    def log(
        self,
        tag: str,
        msg: str,
        exception: Optional[Exception] = None,
        traceback: Optional[str] = None
    ):
        pass
