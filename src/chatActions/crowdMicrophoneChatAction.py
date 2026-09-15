from typing import Final

from .absChatAction import AbsChatAction
from .chatActionResult import ChatActionResult
from ..chatterInventory.helpers.crowdMicrophoneStatusProviderInterface import CrowdMicrophoneStatusProviderInterface
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..timber.timberInterface import TimberInterface
from ..tts.models.ttsEvent import TtsEvent
from ..tts.models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ..tts.provider.compositeTtsManagerProviderInterface import CompositeTtsManagerProviderInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..twitch.officialAccounts.officialTwitchAccountUserIdProviderInterface import \
    OfficialTwitchAccountUserIdProviderInterface


class CrowdMicrophoneChatAction(AbsChatAction):

    def __init__(
        self,
        compositeTtsManagerProvider: CompositeTtsManagerProviderInterface,
        crowdMicrophoneStatusProvider: CrowdMicrophoneStatusProviderInterface,
        officialTwitchAccountUserIdProvider: OfficialTwitchAccountUserIdProviderInterface,
        timber: TimberInterface,
    ):
        if not isinstance(compositeTtsManagerProvider, CompositeTtsManagerProviderInterface):
            raise TypeError(f'compositeTtsManagerProvider argument is malformed: \"{compositeTtsManagerProvider}\"')
        elif not isinstance(crowdMicrophoneStatusProvider, CrowdMicrophoneStatusProviderInterface):
            raise TypeError(f'crowdMicrophoneStatusProvider argument is malformed: \"{crowdMicrophoneStatusProvider}\"')
        elif not isinstance(officialTwitchAccountUserIdProvider, OfficialTwitchAccountUserIdProviderInterface):
            raise TypeError(f'officialTwitchAccountUserIdProvider argument is malformed: \"{officialTwitchAccountUserIdProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__compositeTtsManagerProvider: Final[CompositeTtsManagerProviderInterface] = compositeTtsManagerProvider
        self.__crowdMicrophoneStatusProvider: Final[CrowdMicrophoneStatusProviderInterface] = crowdMicrophoneStatusProvider
        self.__officialTwitchAccountUserIdProvider: Final[OfficialTwitchAccountUserIdProviderInterface] = officialTwitchAccountUserIdProvider
        self.__timber: Final[TimberInterface] = timber

    @property
    def actionName(self) -> str:
        return 'CrowdMicrophoneChatAction'

    async def handleChatAction(
        self,
        mostRecentChat: MostRecentChat | None,
        chatMessage: TwitchChatMessage,
    ) -> ChatActionResult:
        status = await self.__crowdMicrophoneStatusProvider.getMicrophone(
            twitchChannelId = chatMessage.twitchChannelId,
        )

        if status is None:
            return ChatActionResult.IGNORED
        elif chatMessage.chatterUserId == chatMessage.twitchChannelId:
            return ChatActionResult.IGNORED
        elif chatMessage.chatterUserId in await self.__officialTwitchAccountUserIdProvider.getAllUserIds():
            return ChatActionResult.IGNORED

        compositeTtsManager = self.__compositeTtsManagerProvider.constructNewInstance(
            useSharedSoundPlayerManager = False,
        )

        providerOverridableStatus: TtsProviderOverridableStatus

        if chatMessage.twitchUser.isChatterPreferredTtsEnabled:
            providerOverridableStatus = TtsProviderOverridableStatus.CHATTER_OVERRIDABLE
        else:
            providerOverridableStatus = TtsProviderOverridableStatus.TWITCH_CHANNEL_DISABLED

        await compositeTtsManager.playTtsEvent(TtsEvent(
            message = chatMessage.text,
            twitchChannel = chatMessage.twitchChannel,
            twitchChannelId = chatMessage.twitchChannelId,
            userId = chatMessage.chatterUserId,
            userName = chatMessage.chatterUserLogin,
            donation = None,
            provider = chatMessage.twitchUser.defaultTtsProvider,
            providerOverridableStatus = providerOverridableStatus,
            raidInfo = None,
        ))

        self.__timber.log(self.actionName, f'Submitted chat message into the crowd microphone ({chatMessage=})')
        return ChatActionResult.HANDLED
