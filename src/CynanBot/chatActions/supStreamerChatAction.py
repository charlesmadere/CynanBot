from datetime import datetime, timedelta, timezone, tzinfo

import CynanBot.misc.utils as utils
from CynanBot.chatActions.absChatAction import AbsChatAction
from CynanBot.mostRecentChat.mostRecentChat import MostRecentChat
from CynanBot.streamAlertsManager.streamAlert import StreamAlert
from CynanBot.streamAlertsManager.streamAlertsManagerInterface import \
    StreamAlertsManagerInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.tts.ttsEvent import TtsEvent
from CynanBot.tts.ttsProvider import TtsProvider
from CynanBot.twitch.configuration.twitchMessage import TwitchMessage
from CynanBot.users.userInterface import UserInterface


class SupStreamerChatAction(AbsChatAction):

    def __init__(
        self,
        streamAlertsManager: StreamAlertsManagerInterface | None,
        timber: TimberInterface,
        cooldown: timedelta = timedelta(hours = 6),
        timeZone: tzinfo = timezone.utc
    ):
        if streamAlertsManager is not None and not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(cooldown, timedelta):
            raise TypeError(f'cooldown argument is malformed: \"{cooldown}\"')
        elif not isinstance(timeZone, tzinfo):
            raise TypeError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__streamAlertsManager: StreamAlertsManagerInterface | None = streamAlertsManager
        self.__timber: TimberInterface = timber
        self.__cooldown: timedelta = cooldown
        self.__timeZone: tzinfo = timeZone

    async def handleChat(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface
    ) -> bool:
        if not user.isSupStreamerEnabled() and not user.isTtsEnabled():
            return False

        now = datetime.now(self.__timeZone)

        if mostRecentChat is not None and (mostRecentChat.getMostRecentChat() + self.__cooldown) > now:
            return False

        chatMessage = message.getContent()
        supStreamerMessage = user.getSupStreamerMessage()

        if not utils.isValidStr(chatMessage) or not utils.isValidStr(supStreamerMessage):
            return False
        elif chatMessage.lower() != supStreamerMessage.lower():
            return False

        self.__timber.log('SupStreamerChatAction', f'Encountered sup streamer chat message from {message.getAuthorName()}:{message.getAuthorId()} in {user.getHandle()}')

        if self.__streamAlertsManager is not None:
            self.__streamAlertsManager.submitAlert(StreamAlert(
                soundAlert = None,
                twitchChannel = user.getHandle(),
                twitchChannelId = await message.getTwitchChannelId(),
                ttsEvent = TtsEvent(
                    message = f'{message.getAuthorName()} sup',
                    twitchChannel = user.getHandle(),
                    userId = message.getAuthorId(),
                    userName = message.getAuthorName(),
                    donation = None,
                    provider = TtsProvider.DEC_TALK,
                    raidInfo = None
                )
            ))

        return True
