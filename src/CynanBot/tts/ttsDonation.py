from abc import ABC, abstractmethod
from typing import Any

from CynanBot.tts.ttsDonationType import TtsDonationType


class TtsDonation(ABC):

    @abstractmethod
    def getType(self) -> TtsDonationType:
        pass

    @abstractmethod
    def toDictionary(self) -> dict[str, Any]:
        pass
