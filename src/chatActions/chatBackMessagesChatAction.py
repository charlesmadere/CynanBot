from datetime import timedelta
from typing import Final

from .absChatAction import AbsChatAction
from ..misc import utils as utils
from ..misc.timedDict import TimedDict
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchMessage import TwitchMessage
from ..users.userInterface import UserInterface


class ChatBackMessagesChatAction(AbsChatAction):

    def __init__(
        self,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        cooldown: timedelta = timedelta(minutes = 30),
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(cooldown, timedelta):
            raise TypeError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__cooldown: Final[timedelta] = cooldown

        self.__lastMessageTimes: Final[dict[str, TimedDict]] = dict()

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
                self.__twitchChatMessenger.send(
                    text = msg,
                    twitchChannelId = await message.getTwitchChannelId(),
                )

                self.__timber.log('ChatBackMessagesChatAction', f'Handled {msg} message for {message.getAuthorName()}:{message.getAuthorId()} in {user.handle}')
                return True

        return False
