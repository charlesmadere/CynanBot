from typing import Final

from .absChatAction import AbsChatAction
from .chatActionResult import ChatActionResult
from ..chatterInventory.helpers.crowdMicrophoneHelperInterface import CrowdMicrophoneHelperInterface
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..timber.timberInterface import TimberInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class CrowdMicrophoneChatAction(AbsChatAction):

    def __init__(
        self,
        crowdMicrophoneHelper: CrowdMicrophoneHelperInterface,
        timber: TimberInterface,
    ):
        if not isinstance(crowdMicrophoneHelper, CrowdMicrophoneHelperInterface):
            raise TypeError(f'crowdMicrophoneHelper argument is malformed: \"{crowdMicrophoneHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__crowdMicrophoneHelper: Final[CrowdMicrophoneHelperInterface] = crowdMicrophoneHelper
        self.__timber: Final[TimberInterface] = timber

    @property
    def actionName(self) -> str:
        return 'CrowdMicrophoneChatAction'

    async def handleChatAction(
        self,
        mostRecentChat: MostRecentChat | None,
        chatMessage: TwitchChatMessage,
    ) -> ChatActionResult:
        if not await self.__crowdMicrophoneHelper.isCurrentlyEnabled(
            twitchChannelId = chatMessage.twitchChannelId,
        ):
            return ChatActionResult.IGNORED

        # TODO

        self.__timber.log(self.actionName, f'Submitted chat message into the crowd microphone ({chatMessage=})')
        return ChatActionResult.HANDLED
