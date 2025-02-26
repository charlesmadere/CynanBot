from .absChatAction import AbsChatAction
from ..accessLevelChecking.accessLevelCheckingHelperInterface import AccessLevelCheckingHelperInterface
from ..misc import utils as utils
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..streamAlertsManager.streamAlert import StreamAlert
from ..streamAlertsManager.streamAlertsManagerInterface import \
    StreamAlertsManagerInterface
from ..tts.models.ttsEvent import TtsEvent
from ..tts.models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ..ttsChatter.repository.ttsChatterRepositoryInterface import TtsChatterRepositoryInterface
from ..twitch.configuration.twitchMessage import TwitchMessage
from ..users.accessLevel.accessLevel import AccessLevel
from ..users.userInterface import UserInterface


class TtsChatterChatAction(AbsChatAction):

    def __init__(
        self,
        accessLevelCheckingHelper: AccessLevelCheckingHelperInterface,
        streamAlertsManager: StreamAlertsManagerInterface,
        ttsChatterRepository: TtsChatterRepositoryInterface
    ):
        if not isinstance(accessLevelCheckingHelper, AccessLevelCheckingHelperInterface):
            raise TypeError(f'accessLevelCheckingHelper argument is malformed: \"{accessLevelCheckingHelper}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(ttsChatterRepository, TtsChatterRepositoryInterface):
            raise TypeError(f'ttsChatterRepository argument is malformed: \"{ttsChatterRepository}\"')

        self.__accessLevelCheckingHelper: AccessLevelCheckingHelperInterface = accessLevelCheckingHelper
        self.__streamAlertsManager: StreamAlertsManagerInterface = streamAlertsManager
        self.__ttsChatterRepository: TtsChatterRepositoryInterface = ttsChatterRepository

    async def handleChat(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface
    ) -> bool:
        if not user.areTtsChattersEnabled or not user.isTtsEnabled:
            return False

        if await self.__ttsChatterRepository.get(message.getAuthorId(), await message.getTwitchChannelId()) is None:
            return False

        chatMessage = utils.cleanStr(message.getContent())
        if not utils.isValidStr(chatMessage):
            return False

        if chatMessage.startswith('!'):
            return False

        if not await self.__accessLevelCheckingHelper.checkStatus(AccessLevel.SUBSCRIBER, message):
            return False

        providerOverridableStatus: TtsProviderOverridableStatus

        if user.isChatterPreferredTtsEnabled:
            providerOverridableStatus = TtsProviderOverridableStatus.CHATTER_OVERRIDABLE
        else:
            providerOverridableStatus = TtsProviderOverridableStatus.TWITCH_CHANNEL_DISABLED

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = None,
            twitchChannel = user.handle,
            twitchChannelId = await message.getTwitchChannelId(),
            ttsEvent = TtsEvent(
                message = f'{chatMessage}',
                twitchChannel = user.handle,
                twitchChannelId = await message.getTwitchChannelId(),
                userId = message.getAuthorId(),
                userName = message.getAuthorName(),
                donation = None,
                provider = user.defaultTtsProvider,
                providerOverridableStatus = providerOverridableStatus,
                raidInfo = None
            )
        ))

        return True
