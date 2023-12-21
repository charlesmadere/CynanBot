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


class SchubertWalkChatAction(AbsChatAction):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        twitchUtils: TwitchUtils,
        schubertWalkMessage: str = 'SchubertWalk',
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
        self.__schubertWalkMessage: str = schubertWalkMessage
        self.__lastSchubertWalkMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleChat(
        self,
        mostRecentChat: Optional[MostRecentChat],
        message: TwitchMessage,
        user: UserInterface
    ):
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isSchubertWalkMessageEnabled():
            return False
        elif not user.isSchubertWalkMessageEnabled():
            return False

        splits = utils.getCleanedSplits(message.getContent())

        if self.__schubertWalkMessage in splits and self.__lastSchubertWalkMessageTimes.isReadyAndUpdate(user.getHandle()):
            await self.__twitchUtils.safeSend(message.getChannel(), self.__schubertWalkMessage)
            self.__timber.log('SchubertWalkChatAction', f'Handled SchubertWalk message for {message.getAuthorName()}:{message.getAuthorId()} in {user.getHandle()}')
