from abc import ABC, abstractmethod
from datetime import datetime, timedelta

import CynanBotCommon.utils as utils
import twitchUtils
from CynanBotCommon.chatBandManager import ChatBandManager
from CynanBotCommon.timedDict import TimedDict
from TwitchIO.twitchio import Message
from usersRepository import UsersRepository


class AbsMessage(ABC):

    @abstractmethod
    async def handleMessage(self, message: Message) -> bool:
        pass


class CatJamMessage(AbsMessage):

    def __init__(
        self,
        usersRepository: UsersRepository
    ):
        if usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__usersRepository: UsersRepository = usersRepository
        self.__lastCatJamMessageTimes: TimedDict = TimedDict(timedelta(minutes = 20))

    async def handleMessage(self, message: Message):
        if message is None:
            raise ValueError(f'message argument is malformed: \"{message}\"')

        user = self.__usersRepository.getUser(message.channel.name)

        if not user.isCatJamEnabled():
            return False

        splits = utils.getCleanedSplits(message.content)

        if 'catJAM' in splits and self.__lastCatJamMessageTimes.isReadyAndUpdate(user.getHandle()):
            await twitchUtils.safeSend(message.channel, 'catJAM')
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


class StubMessage(AbsMessage):

    def __init__(self):
        pass

    async def handleMessage(self, message: Message) -> bool:
        return False
