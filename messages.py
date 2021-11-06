from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from twitchio import Message

import CynanBotCommon.utils as utils
import twitchUtils
from CynanBotCommon.chatBand.chatBandManager import ChatBandManager
from CynanBotCommon.timedDict import TimedDict
from generalSettingsRepository import GeneralSettingsRepository
from users.user import User


class AbsMessage(ABC):

    @abstractmethod
    async def handleMessage(
        self,
        twitchUser: User,
        message: Message
    ) -> bool:
        pass


class CatJamMessage(AbsMessage):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        catJamMessage: str = 'catJAM',
        cooldown: timedelta = timedelta(minutes = 20)
    ):
        if generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not utils.isValidStr(catJamMessage):
            raise ValueError(f'catJamMessage argument is malformed: \"{catJamMessage}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__catJamMessage: str = catJamMessage
        self.__lastCatJamMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleMessage(
        self,
        twitchUser: User,
        message: Message
    ) -> bool:
        if twitchUser is None:
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif message is None:
            raise ValueError(f'message argument is malformed: \"{message}\"')

        if not self.__generalSettingsRepository.isCatJamMessageEnabled():
            return False
        elif not twitchUser.isCatJamEnabled():
            return False

        splits = utils.getCleanedSplits(message.content)

        if self.__catJamMessage in splits and self.__lastCatJamMessageTimes.isReadyAndUpdate(twitchUser.getHandle()):
            await twitchUtils.safeSend(message.channel, self.__catJamMessage)
            return True
        else:
            return False


class ChatBandMessage(AbsMessage):

    def __init__(
        self,
        chatBandManager: ChatBandManager,
        generalSettingsRepository: GeneralSettingsRepository
    ):
        if chatBandManager is None:
            raise ValueError(f'chatBandManager argument is malformed: \"{chatBandManager}\"')
        elif generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')

        self.__chatBandManager: ChatBandManager = chatBandManager
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository

    async def handleMessage(
        self,
        twitchUser: User,
        message: Message
    ) -> bool:
        if twitchUser is None:
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif message is None:
            raise ValueError(f'message argument is malformed: \"{message}\"')

        if not self.__generalSettingsRepository.isChatBandEnabled():
            return False
        elif not twitchUser.isChatBandEnabled():
            return False

        return await self.__chatBandManager.playInstrumentForMessage(
            twitchChannel = twitchUser.getHandle(),
            author = message.author.name,
            message = utils.cleanStr(message.content)
        )


class CynanMessage(AbsMessage):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        cynanUserName: str = 'CynanMachae',
        cooldown: timedelta = timedelta(days = 3)
    ):
        if generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not utils.isValidStr(cynanUserName):
            raise ValueError(f'cynanUserName argument is malformed: \"{cynanUserName}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__cynanUserName: str = cynanUserName
        self.__cooldown: timedelta = cooldown
        self.__lastCynanMessageTime = datetime.utcnow() - cooldown

    async def handleMessage(
        self,
        twitchUser: User,
        message: Message
    ) -> bool:
        if twitchUser is None:
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif message is None:
            raise ValueError(f'message argument is malformed: \"{message}\"')

        if not self.__generalSettingsRepository.isCynanMessageEnabled():
            return False
        elif not twitchUser.isCynanMessageEnabled():
            return False
        elif message.author.name.lower() != self.__cynanUserName.lower():
            return False

        now = datetime.utcnow()

        if now > self.__lastCynanMessageTime + self.__cooldown:
            self.__lastCynanMessageTime = now
            await message.channel.send(f'/me waves to @{self.__cynanUserName} 👋')
            return True
        else:
            return False


class DeerForceMessage(AbsMessage):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        deerForceMessage: str = 'D e e R F o r C e',
        cooldown: timedelta = timedelta(minutes = 30)
    ):
        if generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not utils.isValidStr(deerForceMessage):
            raise ValueError(f'deerForceMessage argument is malformed: \"{deerForceMessage}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__deerForceMessage: str = deerForceMessage
        self.__lastDeerForceMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleMessage(
        self,
        twitchUser: User,
        message: Message
    ) -> bool:
        if twitchUser is None:
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif message is None:
            raise ValueError(f'message argument is malformed: \"{message}\"')

        if not self.__generalSettingsRepository.isDeerForceMessageEnabled():
            return False
        elif not twitchUser.isDeerForceMessageEnabled():
            return False

        text = utils.cleanStr(message.content)

        if text.lower() == self.__deerForceMessage.lower() and self.__lastDeerForceMessageTimes.isReadyAndUpdate(twitchUser.getHandle()):
            await twitchUtils.safeSend(message.channel, self.__deerForceMessage)
            return True
        else:
            return False


class JamCatMessage(AbsMessage):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        jamCatMessage: str = 'jamCAT',
        cooldown: timedelta = timedelta(minutes = 20)
    ):
        if generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not utils.isValidStr(jamCatMessage):
            raise ValueError(f'jamCatMessage argument is malformed: \"{jamCatMessage}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__jamCatMessage: str = jamCatMessage
        self.__lastCatJamMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleMessage(
        self,
        twitchUser: User,
        message: Message
    ) -> bool:
        if twitchUser is None:
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif message is None:
            raise ValueError(f'message argument is malformed: \"{message}\"')

        if not self.__generalSettingsRepository.isJamCatMessageEnabled():
            return False
        elif not twitchUser.isJamCatEnabled():
            return False

        splits = utils.getCleanedSplits(message.content)

        if self.__jamCatMessage in splits and self.__lastCatJamMessageTimes.isReadyAndUpdate(twitchUser.getHandle()):
            await twitchUtils.safeSend(message.channel, self.__jamCatMessage)
            return True
        else:
            return False


class RatJamMessage(AbsMessage):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        ratJamMessage: str = 'ratJAM',
        cooldown: timedelta = timedelta(minutes = 20)
    ):
        if generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not utils.isValidStr(ratJamMessage):
            raise ValueError(f'ratJamMessage argument is malformed: \"{ratJamMessage}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__ratJamMessage: str = ratJamMessage
        self.__lastRatJamMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleMessage(
        self,
        twitchUser: User,
        message: Message
    ) -> bool:
        if twitchUser is None:
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif message is None:
            raise ValueError(f'message argument is malformed: \"{message}\"')

        if not self.__generalSettingsRepository.isRatJamMessageEnabled():
            return False
        elif not twitchUser.isRatJamEnabled():
            return False

        splits = utils.getCleanedSplits(message.content)

        if self.__ratJamMessage in splits and self.__lastRatJamMessageTimes.isReadyAndUpdate(twitchUser.getHandle()):
            await twitchUtils.safeSend(message.channel, self.__ratJamMessage)
            return True
        else:
            return False


class StubMessage(AbsMessage):

    def __init__(self):
        pass

    async def handleMessage(
        self,
        twitchUser: User,
        message: Message
    ) -> bool:
        return False
