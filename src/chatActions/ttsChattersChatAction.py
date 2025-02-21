from .absChatAction import AbsChatAction
from ..accessLevelChecking.accessLevelCheckingHelperInterface import AccessLevelCheckingHelperInterface
from ..halfLife.models.halfLifeVoice import HalfLifeVoice
from ..microsoftSam.models.microsoftSamVoice import MicrosoftSamVoice
from ..misc import utils as utils
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..streamAlertsManager.streamAlert import StreamAlert
from ..streamAlertsManager.streamAlertsManagerInterface import \
    StreamAlertsManagerInterface
from ..streamElements.models.streamElementsVoice import StreamElementsVoice
from ..tts.ttsEvent import TtsEvent
from ..tts.ttsProvider import TtsProvider
from ..tts.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ..twitch.configuration.twitchMessage import TwitchMessage
from ..users.userInterface import UserInterface


class TtsChattersChatAction(AbsChatAction):

    def __init__(
        self,
        accessLevelCheckingHelper: AccessLevelCheckingHelperInterface,
        streamAlertsManager: StreamAlertsManagerInterface
    ):
        if not isinstance(accessLevelCheckingHelper, AccessLevelCheckingHelperInterface):
            raise TypeError(f'accessLevelCheckingHelper argument is malformed: \"{accessLevelCheckingHelper}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')

        self.__accessLevelCheckingHelper: AccessLevelCheckingHelperInterface = accessLevelCheckingHelper
        self.__streamAlertsManager: StreamAlertsManagerInterface = streamAlertsManager

    async def handleChat(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface
    ) -> bool:
        if not user.isTtsChattersEnabled or not user.isTtsEnabled:
            return False

        chatMessage = utils.cleanStr(message.getContent())
        if not utils.isValidStr(chatMessage):
            return False

        boosterPacks = user.ttsChatterBoosterPacks
        if boosterPacks is None or len(boosterPacks) == 0:
            return False

        boosterPack = boosterPacks.get(message.getAuthorName().lower(), None)
        if boosterPack is None:
            return False

        if not await self.__accessLevelCheckingHelper.checkStatus(boosterPack.accessLevel, message):
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
                provider = boosterPack.ttsProvider,
                providerOverridableStatus = providerOverridableStatus,
                raidInfo = None
            )
        ))

        return True
