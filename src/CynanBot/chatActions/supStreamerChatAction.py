from datetime import datetime, timedelta, timezone

from CynanBot.chatActions.absChatAction import AbsChatAction
from CynanBot.mostRecentChat.mostRecentChatsRepositoryInterface import \
    MostRecentChatsRepositoryInterface
from CynanBot.timber.timberInterface import TimberInterface
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
        # TODO

        pass
