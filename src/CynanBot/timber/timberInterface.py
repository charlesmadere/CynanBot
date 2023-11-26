from abc import ABC, abstractmethod
from typing import Optional


class TimberInterface(ABC):

    @abstractmethod
    def log(
        self,
        tag: str,
        msg: str,
        exception: Optional[Exception] = None,
        traceback: Optional[str] = None
    ):
        pass
