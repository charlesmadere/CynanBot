from datetime import datetime, timedelta

from .absChatAction import AbsChatAction
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..streamAlertsManager.streamAlert import StreamAlert
from ..streamAlertsManager.streamAlertsManagerInterface import \
    StreamAlertsManagerInterface
from ..supStreamer.supStreamerRepositoryInterface import \
    SupStreamerRepositoryInterface
from ..timber.timberInterface import TimberInterface
from ..tts.ttsEvent import TtsEvent
from ..tts.ttsProvider import TtsProvider
from ..twitch.configuration.twitchMessage import TwitchMessage
from ..users.userInterface import UserInterface


class SupStreamerChatAction(AbsChatAction):

    def __init__(
        self,
        streamAlertsManager: StreamAlertsManagerInterface,
        supStreamerRepository: SupStreamerRepositoryInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        cooldown: timedelta = timedelta(hours = 6)
    ):
        if not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(supStreamerRepository, SupStreamerRepositoryInterface):
            raise TypeError(f'supStreamerRepository argument is malformed: \"{supStreamerRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise TypeError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__streamAlertsManager: StreamAlertsManagerInterface = streamAlertsManager
        self.__supStreamerRepository: SupStreamerRepositoryInterface = supStreamerRepository
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__cooldown: timedelta = cooldown

    async def handleChat(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface
    ) -> bool:
        if not user.isSupStreamerEnabled or not user.isTtsEnabled:
            return False

        now = datetime.now(self.__timeZoneRepository.getDefault())

        if mostRecentChat is not None and (mostRecentChat.mostRecentChat + self.__cooldown) > now:
            return False

        chatMessage = message.getContent()
        supStreamerMessage = user.getSupStreamerMessage()

        if not utils.isValidStr(chatMessage) or not utils.isValidStr(supStreamerMessage):
            return False
        elif not await self.__isSupStreamerMessage(
            chatMessage = chatMessage,
            supStreamerMessage = supStreamerMessage
        ):
            return False

        supStreamerChatData = await self.__supStreamerRepository.get(
            chatterUserId = message.getAuthorId(),
            twitchChannelId = await message.getTwitchChannelId()
        )

        if supStreamerChatData is not None and (supStreamerChatData.mostRecentSup + self.__cooldown) > now:
            return False

        await self.__supStreamerRepository.set(
            chatterUserId = message.getAuthorId(),
            twitchChannelId = await message.getTwitchChannelId()
        )

        self.__timber.log('SupStreamerChatAction', f'Encountered sup streamer chat message from {message.getAuthorName()}:{message.getAuthorId()} in {user.getHandle()}')

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = None,
            twitchChannel = user.getHandle(),
            twitchChannelId = await message.getTwitchChannelId(),
            ttsEvent = TtsEvent(
                message = f'{message.getAuthorName()} sup',
                twitchChannel = user.getHandle(),
                twitchChannelId = await message.getTwitchChannelId(),
                userId = message.getAuthorId(),
                userName = message.getAuthorName(),
                donation = None,
                provider = TtsProvider.DEC_TALK,
                raidInfo = None
            )
        ))

        return True

    async def __isSupStreamerMessage(
        self,
        chatMessage: str | None,
        supStreamerMessage: str
    ) -> bool:
        if not utils.isValidStr(chatMessage):
            return False

        # TODO better checks to allow slightly more flexibility
        return chatMessage.casefold() == supStreamerMessage.casefold()
