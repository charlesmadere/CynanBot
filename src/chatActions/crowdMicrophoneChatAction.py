from typing import Final

from .absChatAction import AbsChatAction
from .chatActionResult import ChatActionResult
from ..chatterInventory.helpers.crowdMicrophoneStatusProviderInterface import CrowdMicrophoneStatusProviderInterface
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..timber.timberInterface import TimberInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class CrowdMicrophoneChatAction(AbsChatAction):

    def __init__(
        self,
        crowdMicrophoneStatusProvider: CrowdMicrophoneStatusProviderInterface,
        timber: TimberInterface,
    ):
        if not isinstance(crowdMicrophoneStatusProvider, CrowdMicrophoneStatusProviderInterface):
            raise TypeError(f'crowdMicrophoneStatusProvider argument is malformed: \"{crowdMicrophoneStatusProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__crowdMicrophoneStatusProvider: Final[CrowdMicrophoneStatusProviderInterface] = crowdMicrophoneStatusProvider
        self.__timber: Final[TimberInterface] = timber

    @property
    def actionName(self) -> str:
        return 'CrowdMicrophoneChatAction'

    async def handleChatAction(
        self,
        mostRecentChat: MostRecentChat | None,
        chatMessage: TwitchChatMessage,
    ) -> ChatActionResult:
        status = not await self.__crowdMicrophoneStatusProvider.get(
            twitchChannelId = chatMessage.twitchChannelId,
        )

        if status is None:
            return ChatActionResult.IGNORED

        # TODO

        self.__timber.log(self.actionName, f'Submitted chat message into the crowd microphone ({chatMessage=})')
        return ChatActionResult.HANDLED
