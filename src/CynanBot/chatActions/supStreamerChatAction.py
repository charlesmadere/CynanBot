from datetime import datetime, timedelta, timezone
from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.chatActions.absChatAction import AbsChatAction
from CynanBot.mostRecentChat.mostRecentChat import MostRecentChat
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.tts.ttsEvent import TtsEvent
from CynanBot.tts.ttsManagerInterface import TtsManagerInterface
from CynanBot.twitch.configuration.twitchMessage import TwitchMessage
from CynanBot.users.userInterface import UserInterface


class SupStreamerChatAction(AbsChatAction):

    def __init__(
        self,
        timber: TimberInterface,
        ttsManager: TtsManagerInterface,
        cooldown: timedelta = timedelta(hours = 6),
        timeZone: timezone = timezone.utc
    ):
        if not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsManager, TtsManagerInterface):
            raise ValueError(f'ttsManager argument is malformed: \"{ttsManager}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')
        elif not isinstance(timeZone, timezone):
            raise ValueError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__timber: TimberInterface = timber
        self.__ttsManager: TtsManagerInterface = ttsManager
        self.__cooldown: timedelta = cooldown
        self.__timeZone: timezone = timeZone

    async def handleChat(
        self,
        mostRecentChat: Optional[MostRecentChat],
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

        self.__ttsManager.submitTtsEvent(TtsEvent(
            message = f'{message.getAuthorName()} sup',
            twitchChannel = user.getHandle(),
            userId = message.getAuthorId(),
            userName = message.getAuthorName(),
            donation = None,
            raidInfo = None
        ))

        return True
