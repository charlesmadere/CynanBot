from abc import ABC, abstractmethod
from typing import Any

from frozenlist import FrozenList

from .absChatSoundAlert import AbsChatSoundAlert
from .chatSoundAlertQualifier import ChatSoundAlertQualifer
from .chatSoundAlertType import ChatSoundAlertType


class ChatSoundAlertJsonParserInterface(ABC):

    @abstractmethod
    def parseAlertQualifier(
        self,
        alertQualifier: str
    ) -> ChatSoundAlertQualifer:
        pass

    @abstractmethod
    def parseAlertType(
        self,
        alertType: str
    ) -> ChatSoundAlertType:
        pass

    @abstractmethod
    def parseChatSoundAlert(
        self,
        jsonContents: dict[str, Any]
    ) -> AbsChatSoundAlert:
        pass

    @abstractmethod
    def parseChatSoundAlerts(
        self,
        jsonContents: list[dict[str, Any]] | Any | None
    ) -> FrozenList[AbsChatSoundAlert] | None:
        pass
