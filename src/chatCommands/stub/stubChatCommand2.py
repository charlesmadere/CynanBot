from typing import Collection, Pattern

from ..absChatCommand2 import AbsChatCommand2
from ..chatCommandResult import ChatCommandResult
from ...twitch.localModels.twitchChatMessage import TwitchChatMessage


class StubChatCommand2(AbsChatCommand2):

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return frozenset()

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        # this method is intentionally empty
        return ChatCommandResult.IGNORED
