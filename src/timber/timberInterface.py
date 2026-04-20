from abc import ABC, abstractmethod

from ..misc.startable import Startable


class TimberInterface(Startable, ABC):

    @abstractmethod
    def log(
        self,
        tag: str,
        msg: str,
        exception: Exception | None = None,
        traceback: str | None = None,
    ):
        pass
