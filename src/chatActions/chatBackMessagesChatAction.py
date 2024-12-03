from datetime import timedelta

from .absChatAction import AbsChatAction
from ..misc import utils as utils
from ..misc.generalSettingsRepository import GeneralSettingsRepository
from ..misc.timedDict import TimedDict
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchMessage import TwitchMessage
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.userInterface import UserInterface


class ChatBackMessagesChatAction(AbsChatAction):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        cooldown: timedelta = timedelta(minutes = 20)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(cooldown, timedelta):
            raise TypeError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__lastMessageTimes: dict[str, TimedDict] = dict()
        self.__cooldown: timedelta = cooldown

    async def handleChat(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface
    ) -> bool:
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        messageList = user.getChatBackMessages()

        if not generalSettings.isChatBacksMessageEnabled():
            return False
        elif not user.isChatBackMessagesEnabled:
            return False
        elif messageList is None or len(messageList) == 0:
            return False

        splits = utils.getCleanedSplits(message.getContent())

        for msg in messageList:
            if self.__lastMessageTimes.get(msg) is None:
                self.__lastMessageTimes[msg] = TimedDict(self.__cooldown)

            if msg in splits and self.__lastMessageTimes[msg].isReadyAndUpdate(user.getHandle()):
                await self.__twitchUtils.safeSend(message.getChannel(), msg)
                self.__timber.log('ChatBackMessagesChatAction', f'Handled {msg} message for {message.getAuthorName()}:{message.getAuthorId()} in {user.getHandle()}')
                return True

        return False
