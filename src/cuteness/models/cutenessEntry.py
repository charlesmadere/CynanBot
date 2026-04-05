import locale
from abc import ABC, abstractmethod


class CutenessEntry(ABC):

    @property
    def cutenessStr(self) -> str:
        return locale.format_string("%d", self.getCuteness(), grouping = True)

    @abstractmethod
    def getChatterUserId(self) -> str:
        pass

    @abstractmethod
    def getCuteness(self) -> int:
        pass
