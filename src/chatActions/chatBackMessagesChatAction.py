from datetime import timedelta

from .absChatAction import AbsChatAction
from ..misc import utils as utils
from ..misc.timedDict import TimedDict
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchMessage import TwitchMessage
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.userInterface import UserInterface


class ChatBackMessagesChatAction(AbsChatAction):

    def __init__(
        self,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        cooldown: timedelta = timedelta(minutes = 20)
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(cooldown, timedelta):
            raise TypeError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__cooldown: timedelta = cooldown

        self.__lastMessageTimes: dict[str, TimedDict] = dict()

    async def handleChat(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface
    ) -> bool:
        chatBackMessages = user.chatBackMessages

        if not user.isChatBackMessagesEnabled:
            return False
        elif chatBackMessages is None or len(chatBackMessages) == 0:
            return False

        splits = utils.getCleanedSplits(message.getContent())

        for msg in chatBackMessages:
            if self.__lastMessageTimes.get(msg) is None:
                self.__lastMessageTimes[msg] = TimedDict(self.__cooldown)

            if (message.getContent() == msg or msg in splits) and self.__lastMessageTimes[msg].isReadyAndUpdate(user.handle):
                await self.__twitchUtils.safeSend(message.getChannel(), msg)
                self.__timber.log('ChatBackMessagesChatAction', f'Handled {msg} message for {message.getAuthorName()}:{message.getAuthorId()} in {user.handle}')
                return True

        return False
