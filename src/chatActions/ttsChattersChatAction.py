from .absChatAction import AbsChatAction
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
        streamAlertsManager: StreamAlertsManagerInterface | None
    ):
        if streamAlertsManager is not None and not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')

        self.__streamAlertsManager: StreamAlertsManagerInterface | None = streamAlertsManager

    async def handleChat(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface
    ) -> bool:
        if not user.isTtsChattersEnabled or not user.isTtsEnabled():
            return False

        streamAlertsManager = self.__streamAlertsManager
        if streamAlertsManager is None:
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
            case TtsProvider.STREAM_ELEMENTS:
                if isinstance(boosterPack.voice, StreamElementsVoice):
                    voice = f'{boosterPack.voice.humanName}: '
            case TtsProvider.TTS_MONSTER:
                if utils.isValidStr(boosterPack.voice):
                    voice = f'{boosterPack.voice}: '

        streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = None,
            twitchChannel = user.getHandle(),
            twitchChannelId = await message.getTwitchChannelId(),
            ttsEvent = TtsEvent(
                message = f'{voice}{chatMessage}',
                twitchChannel = user.getHandle(),
                twitchChannelId = await message.getTwitchChannelId(),
                userId = message.getAuthorId(),
                userName = message.getAuthorName(),
                donation = None,
                provider = boosterPack.ttsProvider,
                raidInfo = None
            )
        ))

        return True
