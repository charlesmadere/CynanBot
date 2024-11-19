from .absChatAction import AbsChatAction
from ..misc import utils as utils
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..streamAlertsManager.streamAlert import StreamAlert
from ..streamAlertsManager.streamAlertsManagerInterface import \
    StreamAlertsManagerInterface
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
        if not user.isTtsChattersEnabled() or not user.isTtsEnabled():
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

        boosterPack = boosterPacks.get(message.getTwitchChannelName(), None)
        if boosterPack is None:
            return False

        streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = None,
            twitchChannel = user.getHandle(),
            twitchChannelId = await message.getTwitchChannelId(),
            ttsEvent = TtsEvent(
                message = f'{boosterPack.voice.humanName}: {chatMessage}',
                twitchChannel = user.getHandle(),
                twitchChannelId = await message.getTwitchChannelId(),
                userId = message.getAuthorId(),
                userName = message.getAuthorName(),
                donation = None,
                provider = TtsProvider.STREAM_ELEMENTS,
                raidInfo = None
            )
        ))

        return True
