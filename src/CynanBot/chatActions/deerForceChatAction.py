from datetime import timedelta

import CynanBot.misc.utils as utils
from CynanBot.chatActions.absChatAction import AbsChatAction
from CynanBot.generalSettingsRepository import GeneralSettingsRepository
from CynanBot.misc.timedDict import TimedDict
from CynanBot.mostRecentChat.mostRecentChat import MostRecentChat
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.configuration.twitchMessage import TwitchMessage
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.users.userInterface import UserInterface


class DeerForceChatAction(AbsChatAction):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        deerForceMessage: str = 'D e e R F o r C e',
        cooldown: timedelta = timedelta(minutes = 20)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not utils.isValidStr(deerForceMessage):
            raise TypeError(f'deerForceMessage argument is malformed: \"{deerForceMessage}\"')
        elif not isinstance(cooldown, timedelta):
            raise TypeError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__deerForceMessage: str = deerForceMessage
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleChat(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface
    ):
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isDeerForceMessageEnabled():
            return False
        elif not user.isDeerForceMessageEnabled():
            return False

        splits = utils.getCleanedSplits(message.getContent())

        if self.__deerForceMessage in splits and self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            await self.__twitchUtils.safeSend(message.getChannel(), self.__deerForceMessage)
            self.__timber.log('DeerForceChatAction', f'Handled {self.__deerForceMessage} message for {message.getAuthorName()}:{message.getAuthorId()} in {user.getHandle()}')
            return True
        else:
            return False
