from typing import Final

from .absChatAction import AbsChatAction
from .chatActionResult import ChatActionResult
from ..chatterInventory.helpers.crowdMicrophoneProviderInterface import CrowdMicrophoneProviderInterface
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
        crowdMicrophoneProvider: CrowdMicrophoneProviderInterface,
        officialTwitchAccountUserIdProvider: OfficialTwitchAccountUserIdProviderInterface,
        timber: TimberInterface,
    ):
        if not isinstance(compositeTtsManagerProvider, CompositeTtsManagerProviderInterface):
            raise TypeError(f'compositeTtsManagerProvider argument is malformed: \"{compositeTtsManagerProvider}\"')
        elif not isinstance(crowdMicrophoneProvider, CrowdMicrophoneProviderInterface):
            raise TypeError(f' argument is malformed: \"{crowdMicrophoneProvider}\"')
        elif not isinstance(officialTwitchAccountUserIdProvider, OfficialTwitchAccountUserIdProviderInterface):
            raise TypeError(f'officialTwitchAccountUserIdProvider argument is malformed: \"{officialTwitchAccountUserIdProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__compositeTtsManagerProvider: Final[CompositeTtsManagerProviderInterface] = compositeTtsManagerProvider
        self.__crowdMicrophoneProvider: Final[CrowdMicrophoneProviderInterface] = crowdMicrophoneProvider
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
        microphone = await self.__crowdMicrophoneProvider.getMicrophone(
            twitchChannelId = chatMessage.twitchChannelId,
        )

        if microphone is None:
            return ChatActionResult.IGNORED
        elif chatMessage.chatterUserId == chatMessage.twitchChannelId:
            return ChatActionResult.IGNORED
        elif chatMessage.chatterUserId in await self.__officialTwitchAccountUserIdProvider.getAllUserIds():
            return ChatActionResult.IGNORED

        compositeTtsManager = self.__compositeTtsManagerProvider.constructNewInstance(
            useSharedSoundPlayerManager = False,
        )

        await self.__crowdMicrophoneProvider.addAssociatedTtsManager(
            compositeTtsManager = compositeTtsManager,
            twitchChannelId = chatMessage.twitchChannelId,
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

        self.__timber.log(self.actionName, f'Submitted chat message into the crowd microphone ({microphone=}) ({chatMessage=})')
        return ChatActionResult.HANDLED
