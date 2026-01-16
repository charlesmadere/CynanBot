from abc import ABC, abstractmethod

from typing import Any


class TwitchUserInterface(ABC):

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TwitchUserInterface):
            return False

        return self.getUserId() == other.getUserId()

    @abstractmethod
    def getUserId(self) -> str:
        pass

    @abstractmethod
    def getUserLogin(self) -> str:
        pass

    @abstractmethod
    def getUserName(self) -> str:
        pass

    def __hash__(self) -> int:
        return hash(self.getUserId())
