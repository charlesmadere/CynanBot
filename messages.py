from abc import ABC, abstractmethod
from datetime import datetime, timedelta

import CynanBotCommon.utils as utils
import twitchUtils
from CynanBotCommon.chatBandManager import ChatBandManager
from CynanBotCommon.timedDict import TimedDict
from generalSettingsRepository import GeneralSettingsRepository
from TwitchIO.twitchio import Message
from usersRepository import UsersRepository


class AbsMessage(ABC):

    @abstractmethod
    async def handleMessage(self, message: Message) -> bool:
        pass


class CatJamMessage(AbsMessage):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        usersRepository: UsersRepository,
        catJamMessage: str = 'catJAM',
        cooldown: timedelta = timedelta(minutes = 20)
    ):
        if generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not utils.isValidStr(catJamMessage):
            raise ValueError(f'catJamMessage argument is malformed: \"{catJamMessage}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__usersRepository: UsersRepository = usersRepository
        self.__catJamMessage: str = catJamMessage
        self.__lastCatJamMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleMessage(self, message: Message) -> bool:
        if message is None:
            raise ValueError(f'message argument is malformed: \"{message}\"')

        if not self.__generalSettingsRepository.isCatJamMessageEnabled():
            return False

        user = self.__usersRepository.getUser(message.channel.name)

        if not user.isCatJamEnabled():
            return False

        splits = utils.getCleanedSplits(message.content)

        if self.__catJamMessage in splits and self.__lastCatJamMessageTimes.isReadyAndUpdate(user.getHandle()):
            await twitchUtils.safeSend(message.channel, self.__catJamMessage)
            return True
        else:
            return False


class ChatBandMessage(AbsMessage):

    def __init__(
        self,
        chatBandManager: ChatBandManager,
        usersRepository: UsersRepository
    ):
        if chatBandManager is None:
            raise ValueError(f'chatBandManager argument is malformed: \"{chatBandManager}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__chatBandManager: ChatBandManager = chatBandManager
        self.__usersRepository: UsersRepository = usersRepository

    async def handleMessage(self, message: Message) -> bool:
        if message is None:
            raise ValueError(f'message argument is malformed: \"{message}\"')

        user = self.__usersRepository.getUser(message.channel.name)

        if not user.isChatBandEnabled():
            return False

        return await self.__chatBandManager.playInstrumentForMessage(
            twitchChannel = user.getHandle(),
            author = message.author.name,
            message = utils.cleanStr(message.content)
        )


class CynanMessage(AbsMessage):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        usersRepository: UsersRepository,
        cynanUserName: str = 'CynanMachae',
        cooldown: timedelta = timedelta(days = 3)
    ):
        if generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not utils.isValidStr(cynanUserName):
            raise ValueError(f'cynanUserName argument is malformed: \"{cynanUserName}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__usersRepository: UsersRepository = usersRepository
        self.__cynanUserName: str = cynanUserName
        self.__cooldown: timedelta = cooldown
        self.__lastCynanMessageTime = datetime.utcnow() - cooldown

    async def handleMessage(self, message: Message) -> bool:
        if message is None:
            raise ValueError(f'message argument is malformed: \"{message}\"')

        if not self.__generalSettingsRepository.isCynanMessageEnabled():
            return False
        elif message.author.name.lower() != self.__cynanUserName.lower():
            return False

        user = self.__usersRepository.getUser(message.channel.name)

        if not user.isCynanMessageEnabled():
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
        usersRepository: UsersRepository,
        deerForceMessage: str = 'D e e R F o r C e',
        cooldown: timedelta = timedelta(minutes = 30)
    ):
        if generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not utils.isValidStr(deerForceMessage):
            raise ValueError(f'deerForceMessage argument is malformed: \"{deerForceMessage}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__usersRepository: UsersRepository = usersRepository
        self.__deerForceMessage: str = deerForceMessage
        self.__lastDeerForceMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleMessage(self, message: Message) -> bool:
        if message is None:
            raise ValueError(f'message argument is malformed: \"{message}\"')

        if not self.__generalSettingsRepository.isDeerForceMessageEnabled():
            return False

        user = self.__usersRepository.getUser(message.channel.name)
        text = utils.cleanStr(message.content)

        if text.lower() == self.__deerForceMessage.lower() and self.__lastDeerForceMessageTimes.isReadyAndUpdate(user.getHandle()):
            await twitchUtils.safeSend(message.channel, self.__deerForceMessage)
            return True
        else:
            return False


class JamCatMessage(AbsMessage):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        usersRepository: UsersRepository,
        jamCatMessage: str = 'jamCAT',
        cooldown: timedelta = timedelta(minutes = 20)
    ):
        if generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not utils.isValidStr(jamCatMessage):
            raise ValueError(f'jamCatMessage argument is malformed: \"{jamCatMessage}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__usersRepository: UsersRepository = usersRepository
        self.__jamCatMessage: str = jamCatMessage
        self.__lastCatJamMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleMessage(self, message: Message) -> bool:
        if message is None:
            raise ValueError(f'message argument is malformed: \"{message}\"')

        if not self.__generalSettingsRepository.isJamCatMessageEnabled():
            return False

        user = self.__usersRepository.getUser(message.channel.name)

        if not user.isJamCatEnabled():
            return False

        splits = utils.getCleanedSplits(message.content)

        if self.__jamCatMessage in splits and self.__lastCatJamMessageTimes.isReadyAndUpdate(user.getHandle()):
            await twitchUtils.safeSend(message.channel, self.__jamCatMessage)
            return True
        else:
            return False


class RatJamMessage(AbsMessage):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        usersRepository: UsersRepository,
        ratJamMessage: str = 'ratJAM',
        cooldown: timedelta = timedelta(minutes = 20)
    ):
        if generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not utils.isValidStr(ratJamMessage):
            raise ValueError(f'ratJamMessage argument is malformed: \"{ratJamMessage}\"')
        elif cooldown is None:
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__usersRepository: UsersRepository = usersRepository
        self.__ratJamMessage: str = ratJamMessage
        self.__lastRatJamMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleMessage(self, message: Message) -> bool:
        if message is None:
            raise ValueError(f'message argument is malformed: \"{message}\"')

        if not self.__generalSettingsRepository.isRatJamMessageEnabled():
            return False

        user = self.__usersRepository.getUser(message.channel.name)

        if not user.isRatJamEnabled():
            return False

        splits = utils.getCleanedSplits(message.content)

        if self.__ratJamMessage in splits and self.__lastRatJamMessageTimes.isReadyAndUpdate(user.getHandle()):
            await twitchUtils.safeSend(message.channel, self.__ratJamMessage)
            return True
        else:
            return False


class StubMessage(AbsMessage):

    def __init__(self):
        pass

    async def handleMessage(self, message: Message) -> bool:
        return False
