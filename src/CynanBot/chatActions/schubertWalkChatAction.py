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


class SchubertWalkChatAction(AbsChatAction):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        schubertWalkMessage: str = 'SchubertWalk',
        cooldown: timedelta = timedelta(minutes = 20)
    ):
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        if not utils.isValidStr(schubertWalkMessage):
            raise ValueError(f'schubertWalkMessage argument is malformed: \"{schubertWalkMessage}\"')
        assert isinstance(cooldown, timedelta), f"malformed {cooldown=}"

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__schubertWalkMessage: str = schubertWalkMessage
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleChat(
        self,
        mostRecentChat: Optional[MostRecentChat],
        message: TwitchMessage,
        user: UserInterface
    ) -> bool:
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isSchubertWalkMessageEnabled():
            return False
        elif not user.isSchubertWalkMessageEnabled():
            return False

        splits = utils.getCleanedSplits(message.getContent())

        if self.__schubertWalkMessage in splits and self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            await self.__twitchUtils.safeSend(message.getChannel(), self.__schubertWalkMessage)
            self.__timber.log('SchubertWalkChatAction', f'Handled {self.__schubertWalkMessage} message for {message.getAuthorName()}:{message.getAuthorId()} in {user.getHandle()}')
            return True
        else:
            return False
