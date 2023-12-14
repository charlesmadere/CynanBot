from datetime import datetime, timedelta, timezone

import CynanBot.misc.utils as utils
from CynanBot.chatActions.absChatAction import AbsChatAction
from CynanBot.mostRecentChat.mostRecentChatsRepositoryInterface import \
    MostRecentChatsRepositoryInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.tts.ttsEvent import TtsEvent
from CynanBot.tts.ttsManagerInterface import TtsManagerInterface
from CynanBot.twitch.configuration.twitchMessage import TwitchMessage
from CynanBot.users.userInterface import UserInterface


class SupStreamerChatAction(AbsChatAction):

    def __init__(
        self,
        mostRecentChatsRepository: MostRecentChatsRepositoryInterface,
        timber: TimberInterface,
        ttsManager: TtsManagerInterface,
        cooldown: timedelta = timedelta(hours = 8),
        timeZone: timezone = timezone.utc
    ):
        if not isinstance(mostRecentChatsRepository, MostRecentChatsRepositoryInterface):
            raise ValueError(f'mostRecentChatsRepository argument is malformed: \"{mostRecentChatsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsManager, TtsManagerInterface):
            raise ValueError(f'ttsManager argument is malformed: \"{ttsManager}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')
        elif not isinstance(timeZone, timezone):
            raise ValueError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__mostRecentChatsRepository: MostRecentChatsRepositoryInterface = mostRecentChatsRepository
        self.__timber: TimberInterface = timber
        self.__ttsManager: TtsManagerInterface = ttsManager
        self.__cooldown: timedelta = cooldown
        self.__timeZone: timezone = timeZone

    async def handleChat(
        self,
        message: TwitchMessage,
        user: UserInterface
    ):
        if not user.isSupStreamerEnabled() and not user.isTtsEnabled():
            return

        mostRecentChat = await self.__mostRecentChatsRepository.get(
            chatterUserId = message.getAuthorId(),
            twitchChannelId = await message.getTwitchChannelId()
        )

        now = datetime.now(self.__timeZone)

        if mostRecentChat is not None and (mostRecentChat.getMostRecentChat() + self.__cooldown) > now:
            return

        chatMessage = message.getContent()
        supStreamerMessage = user.getSupStreamerMessage()

        if not utils.isValidStr(chatMessage) or not utils.isValidStr(supStreamerMessage):
            return
        elif chatMessage.lower() != supStreamerMessage.lower():
            return

        self.__timber.log('SupStreamerChatAction', f'Encountered sup streamer chat message from {message.getAuthorName()}:{message.getAuthorId()} in {user.getHandle()}')

        self.__ttsManager.submitTtsEvent(TtsEvent(
            message = f'{message.getAuthorName()} sup',
            twitchChannel = user.getHandle(),
            userId = message.getAuthorId(),
            userName = message.getAuthorName(),
            donation = None,
            raidInfo = None
        ))
