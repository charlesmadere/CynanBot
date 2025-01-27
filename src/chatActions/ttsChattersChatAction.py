from .absChatAction import AbsChatAction
from ..accessLevelChecking.accessLevelCheckingRepositoryInterface import AccessLevelCheckingRepositoryInterface
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
from ..twitch.configuration.twitchMessage import TwitchMessage
from ..users.userInterface import UserInterface


class TtsChattersChatAction(AbsChatAction):

    def __init__(
        self,
        accessLevelCheckingRepository: AccessLevelCheckingRepositoryInterface,
        streamAlertsManager: StreamAlertsManagerInterface
    ):
        if not isinstance(accessLevelCheckingRepository, AccessLevelCheckingRepositoryInterface):
            raise TypeError(f'accessLevelCheckingRepository argument is malformed: \"{accessLevelCheckingRepository}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')

        self.__accessLevelCheckingRepository: AccessLevelCheckingRepositoryInterface = accessLevelCheckingRepository
        self.__streamAlertsManager: StreamAlertsManagerInterface = streamAlertsManager

    async def handleChat(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface
    ) -> bool:
        if not user.isTtsChattersEnabled or not user.isTtsEnabled:
            return False

        chatMessage = message.getContent()
        if not utils.isValidStr(chatMessage):
            return False

        boosterPacks = user.ttsChatterBoosterPacks
        if boosterPacks is None or len(boosterPacks) == 0:
            return False

        boosterPack = boosterPacks.get(message.getAuthorName().lower(), None)
        if boosterPack is None:
            return False

        voice: str = ''

        match boosterPack.ttsProvider:
            case TtsProvider.HALF_LIFE:
                if isinstance(boosterPack.voice, HalfLifeVoice):
                    voice = f'{boosterPack.voice.value}: '
            case TtsProvider.MICROSOFT_SAM:
                if isinstance(boosterPack.voice, MicrosoftSamVoice):
                    voice = f'{boosterPack.voice.value}: '
            case TtsProvider.STREAM_ELEMENTS:
                if isinstance(boosterPack.voice, StreamElementsVoice):
                    voice = f'{boosterPack.voice.humanName}: '
            case TtsProvider.TTS_MONSTER:
                if utils.isValidStr(boosterPack.voice):
                    voice = f'{boosterPack.voice}: '

        if not await self.__accessLevelCheckingRepository.checkStatus(boosterPack.accessLevel, message):
            return False

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = None,
            twitchChannel = user.handle,
            twitchChannelId = await message.getTwitchChannelId(),
            ttsEvent = TtsEvent(
                message = f'{voice}{chatMessage}',
                twitchChannel = user.handle,
                twitchChannelId = await message.getTwitchChannelId(),
                userId = message.getAuthorId(),
                userName = message.getAuthorName(),
                donation = None,
                provider = boosterPack.ttsProvider,
                raidInfo = None
            )
        ))

        return True
