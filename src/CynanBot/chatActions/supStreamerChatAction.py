from datetime import datetime, timedelta

import CynanBot.misc.utils as utils
from CynanBot.chatActions.absChatAction import AbsChatAction
from CynanBot.location.timeZoneRepositoryInterface import \
    TimeZoneRepositoryInterface
from CynanBot.mostRecentChat.mostRecentChat import MostRecentChat
from CynanBot.streamAlertsManager.streamAlert import StreamAlert
from CynanBot.streamAlertsManager.streamAlertsManagerInterface import \
    StreamAlertsManagerInterface
from CynanBot.supStreamer.supStreamerRepositoryInterface import \
    SupStreamerRepositoryInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.tts.ttsEvent import TtsEvent
from CynanBot.tts.ttsProvider import TtsProvider
from CynanBot.twitch.configuration.twitchMessage import TwitchMessage
from CynanBot.users.userInterface import UserInterface


class SupStreamerChatAction(AbsChatAction):

    def __init__(
        self,
        streamAlertsManager: StreamAlertsManagerInterface | None,
        supStreamerRepository: SupStreamerRepositoryInterface | None,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        cooldown: timedelta = timedelta(hours = 6)
    ):
        if streamAlertsManager is not None and not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif supStreamerRepository is not None and not isinstance(supStreamerRepository, SupStreamerRepositoryInterface):
            raise TypeError(f'supStreamerRepository argument is malformed: \"{supStreamerRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise TypeError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__streamAlertsManager: StreamAlertsManagerInterface | None = streamAlertsManager
        self.__supStreamerRepository: SupStreamerRepositoryInterface | None = supStreamerRepository
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__cooldown: timedelta = cooldown

    async def handleChat(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface
    ) -> bool:
        if not user.isSupStreamerEnabled() or not user.isTtsEnabled():
            return False

        streamAlertsManager = self.__streamAlertsManager
        supStreamerRepository = self.__supStreamerRepository

        if streamAlertsManager is None or supStreamerRepository is None:
            return False

        now = datetime.now(self.__timeZoneRepository.getDefault())

        if mostRecentChat is not None and (mostRecentChat.mostRecentChat + self.__cooldown) > now:
            return False

        chatMessage = message.getContent()
        supStreamerMessage = user.getSupStreamerMessage()

        if not utils.isValidStr(chatMessage) or not utils.isValidStr(supStreamerMessage):
            return False
        elif chatMessage.casefold() != supStreamerMessage.casefold():
            return False

        supStreamerChatData = await supStreamerRepository.get(
            chatterUserId = message.getAuthorId(),
            twitchChannelId = await message.getTwitchChannelId()
        )

        if supStreamerChatData is not None and (supStreamerChatData.mostRecentSup + self.__cooldown) > now:
            return False

        await supStreamerRepository.set(
            chatterUserId = message.getAuthorId(),
            twitchChannelId = await message.getTwitchChannelId()
        )

        self.__timber.log('SupStreamerChatAction', f'Encountered sup streamer chat message from {message.getAuthorName()}:{message.getAuthorId()} in {user.getHandle()}')

        streamAlertsManager.submitAlert(StreamAlert(
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
