from ..absChatAction2 import AbsChatAction2
from ..chatActionResult import ChatActionResult
from ...mostRecentChat.mostRecentChat import MostRecentChat
from ...twitch.localModels.twitchChatMessage import TwitchChatMessage


class StubChatAction2(AbsChatAction2):

    @property
    def actionName(self) -> str:
        return "StubChatAction2"

    async def handleChatAction(
        self,
        mostRecentChat: MostRecentChat | None,
        chatMessage: TwitchChatMessage,
    ) -> ChatActionResult:
        # this method is intentionally empty
        return ChatActionResult.IGNORED
