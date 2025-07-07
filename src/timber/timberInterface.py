from abc import ABC, abstractmethod


class TimberInterface(ABC):

    @abstractmethod
    def log(
        self,
        tag: str,
        msg: str,
        exception: Exception | None = None,
        traceback: str | None = None,
    ):
        pass

    @abstractmethod
    def start(self):
        pass
