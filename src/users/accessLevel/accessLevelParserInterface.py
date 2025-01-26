from abc import ABC, abstractmethod
from typing import Any

from .accessLevel import AccessLevel


class AccessLevelJsonParserInterface(ABC):

    @abstractmethod
    def parseAccessLevel(
        self,
        defaultAccessLevel: AccessLevel,
        jsonContents: str | Any | None
    ) -> AccessLevel:
        pass