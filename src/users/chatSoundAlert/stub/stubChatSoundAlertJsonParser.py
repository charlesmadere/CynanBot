from typing import Any

from frozenlist import FrozenList

from ..absChatSoundAlert import AbsChatSoundAlert
from ..chatSoundAlertJsonParserInterface import ChatSoundAlertJsonParserInterface
from ..chatSoundAlertQualifier import ChatSoundAlertQualifer
from ..chatSoundAlertType import ChatSoundAlertType


class StubChatSoundAlertJsonParser(ChatSoundAlertJsonParserInterface):

    def parseAlertQualifier(
        self,
        alertQualifier: str
    ) -> ChatSoundAlertQualifer:
        # this method is intentionally empty
        raise RuntimeError('Not implemented')

    def parseAlertType(
        self,
        alertType: str
    ) -> ChatSoundAlertType:
        # this method is intentionally empty
        raise RuntimeError('Not implemented')

    def parseChatSoundAlert(
        self,
        jsonContents: dict[str, Any]
    ) -> AbsChatSoundAlert:
        # this method is intentionally empty
        raise RuntimeError('Not implemented')

    def parseChatSoundAlerts(
        self,
        jsonContents: list[dict[str, Any]] | Any | None
    ) -> FrozenList[AbsChatSoundAlert] | None:
        # this method is intentionally empty
        return None
