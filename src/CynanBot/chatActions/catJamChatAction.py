from datetime import timedelta
from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.chatActions.absChatAction import AbsChatAction
from CynanBot.generalSettingsRepository import GeneralSettingsRepository
from CynanBot.misc.timedDict import TimedDict
from CynanBot.mostRecentChat.mostRecentChat import MostRecentChat
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.configuration.twitchMessage import TwitchMessage
from CynanBot.twitch.twitchUtils import TwitchUtils
from CynanBot.users.userInterface import UserInterface


class CatJamChatAction(AbsChatAction):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        twitchUtils: TwitchUtils,
        catJamMessage: str = 'catJAM',
        cooldown: timedelta = timedelta(minutes = 20)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__catJamMessage: str = catJamMessage
        self.__lastCatJamMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleChat(
        self,
        mostRecentChat: Optional[MostRecentChat],
        message: TwitchMessage,
        user: UserInterface
    ):
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isCatJamMessageEnabled():
            return False
        elif not user.isCatJamMessageEnabled():
            return False

        splits = utils.getCleanedSplits(message.getContent())

        if self.__catJamMessage in splits and self.__lastCatJamMessageTimes.isReadyAndUpdate(user.getHandle()):
            await self.__twitchUtils.safeSend(message.getChannel(), self.__catJamMessage)
            self.__timber.log('CatJamMessage', f'Handled catJAM message for {message.getAuthorName()}:{message.getAuthorId()} in {user.getHandle()}')
