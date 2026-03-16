from typing import Collection, Final, Pattern

from ..absChatCommand2 import AbsChatCommand2
from ..chatCommandResult import ChatCommandResult
from ...twitch.localModels.twitchChatMessage import TwitchChatMessage


class StubChatCommand2(AbsChatCommand2):

    def __init__(self):
        self.__commandPatterns: Final[Collection[Pattern]] = frozenset()

    @property
    def commandName(self) -> str:
        return 'StubChatCommand2'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        # this method is intentionally empty
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        # this method is intentionally empty
        return ChatCommandResult.IGNORED
