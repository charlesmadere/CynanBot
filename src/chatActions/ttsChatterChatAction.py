from .absChatAction import AbsChatAction
from ..accessLevelChecking.accessLevelCheckingHelperInterface import AccessLevelCheckingHelperInterface
from ..misc import utils as utils
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..streamAlertsManager.streamAlert import StreamAlert
from ..streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ..tts.models.ttsEvent import TtsEvent
from ..tts.models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ..tts.provider.compositeTtsManagerProviderInterface import CompositeTtsManagerProviderInterface
from ..ttsChatter.repository.ttsChatterRepositoryInterface import TtsChatterRepositoryInterface
from ..ttsChatter.settings.ttsChatterSettingsRepositoryInterface import TtsChatterSettingsRepositoryInterface
from ..twitch.configuration.twitchMessage import TwitchMessage
from ..users.accessLevel.accessLevel import AccessLevel
from ..users.userInterface import UserInterface


class TtsChatterChatAction(AbsChatAction):

    def __init__(
        self,
        accessLevelCheckingHelper: AccessLevelCheckingHelperInterface,
        compositeTtsManagerProvider: CompositeTtsManagerProviderInterface,
        streamAlertsManager: StreamAlertsManagerInterface,
        ttsChatterRepository: TtsChatterRepositoryInterface,
        ttsChatterSettingsRepository: TtsChatterSettingsRepositoryInterface
    ):
        if not isinstance(accessLevelCheckingHelper, AccessLevelCheckingHelperInterface):
            raise TypeError(f'accessLevelCheckingHelper argument is malformed: \"{accessLevelCheckingHelper}\"')
        elif not isinstance(compositeTtsManagerProvider, CompositeTtsManagerProviderInterface):
            raise TypeError(f'compositeTtsManagerProvider argument is malformed: \"{compositeTtsManagerProvider}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(ttsChatterRepository, TtsChatterRepositoryInterface):
            raise TypeError(f'ttsChatterRepository argument is malformed: \"{ttsChatterRepository}\"')
        elif not isinstance(ttsChatterSettingsRepository, TtsChatterSettingsRepositoryInterface):
            raise TypeError(f'ttsChatterSettingsRepository argument is malformed: \"{ttsChatterSettingsRepository}\"')

        self.__accessLevelCheckingHelper: AccessLevelCheckingHelperInterface = accessLevelCheckingHelper
        self.__compositeTtsManagerProvider: CompositeTtsManagerProviderInterface = compositeTtsManagerProvider
        self.__streamAlertsManager: StreamAlertsManagerInterface = streamAlertsManager
        self.__ttsChatterRepository: TtsChatterRepositoryInterface = ttsChatterRepository
        self.__ttsChatterSettingsRepository: TtsChatterSettingsRepositoryInterface = ttsChatterSettingsRepository

    async def handleChat(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface
    ) -> bool:
        if not user.areTtsChattersEnabled or not user.isTtsEnabled:
            return False

        if not await self.__ttsChatterRepository.isTtsChatter(
            chatterUserId = message.getAuthorId(),
            twitchChannelId = await message.getTwitchChannelId()
        ):
            return False

        chatMessage = utils.cleanStr(message.getContent())
        if not utils.isValidStr(chatMessage):
            return False

        if chatMessage.startswith('!'):
            return False

        # don't commit
        chatMessage = chatMessage.replace("lucentw", "lucy")
        chatMessage = chatMessage.replace("LucentW", "lucy")
        chatMessage = chatMessage.replace("@lucentw", "lucy")
        chatMessage = chatMessage.replace("@LucentW", "lucy")

        if await self.__ttsChatterSettingsRepository.subscriberOnly() and not await self.__accessLevelCheckingHelper.checkStatus(AccessLevel.SUBSCRIBER, message):
            return False

        providerOverridableStatus: TtsProviderOverridableStatus

        if user.isChatterPreferredTtsEnabled:
            providerOverridableStatus = TtsProviderOverridableStatus.CHATTER_OVERRIDABLE
        else:
            providerOverridableStatus = TtsProviderOverridableStatus.TWITCH_CHANNEL_DISABLED

        ttsEvent = TtsEvent(
            message = chatMessage,
            twitchChannel = user.handle,
            twitchChannelId = await message.getTwitchChannelId(),
            userId = message.getAuthorId(),
            userName = message.getAuthorName(),
            donation = None,
            provider = user.defaultTtsProvider,
            providerOverridableStatus = providerOverridableStatus,
            raidInfo = None
        )

        if await self.__ttsChatterSettingsRepository.useMessageQueueing():
            self.__streamAlertsManager.submitAlert(StreamAlert(
                soundAlert = None,
                twitchChannel = user.handle,
                twitchChannelId = await message.getTwitchChannelId(),
                ttsEvent = ttsEvent
            ))

            return True
        else:
            compositeTtsManager = self.__compositeTtsManagerProvider.constructNewInstance(
                useSharedSoundPlayerManager = False
            )

            return await compositeTtsManager.playTtsEvent(ttsEvent)
