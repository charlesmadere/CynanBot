from datetime import timedelta
from typing import Optional

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
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        if not utils.isValidStr(deerForceMessage):
            raise ValueError(f'deerForceMessage argument is malformed: \"{deerForceMessage}\"')
        assert isinstance(cooldown, timedelta), f"malformed {cooldown=}"

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__deerForceMessage: str = deerForceMessage
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleChat(
        self,
        mostRecentChat: Optional[MostRecentChat],
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
