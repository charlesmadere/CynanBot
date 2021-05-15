from abc import ABC, abstractmethod
from datetime import timedelta

import CynanBotCommon.utils as utils
from CynanBotCommon.analogueStoreRepository import AnalogueStoreRepository
from CynanBotCommon.timedDict import TimedDict
from usersRepository import UsersRepository


class AbsCommand(ABC):

    @abstractmethod
    async def handleCommand(self, ctx):
        pass


class AnalogueCommand(AbsCommand):

    def __init__(
        self,
        analogueStoreRepository: AnalogueStoreRepository,
        usersRepository: UsersRepository
    ):
        if analogueStoreRepository is None:
            raise ValueError(f'analogueStoreRepository argument is malformed: \"{analogueStoreRepository}\"')
        elif usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__analogueStoreRepository = analogueStoreRepository
        self.__usersRepository = usersRepository
        self.__lastAnalogueStockMessageTimes = TimedDict(timedelta(minutes = 2, seconds = 30))

    async def handleCommand(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isAnalogueEnabled():
            return
        elif not self.__lastAnalogueStockMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.message.content)
        includePrices = 'includePrices' in splits

        try:
            result = self.__analogueStoreRepository.fetchStoreStock()
            await ctx.send(result.toStr(includePrices = includePrices))
        except (RuntimeError, ValueError):
            print(f'Error fetching Analogue stock in {user.getHandle()}')
            await ctx.send('⚠ Error fetching Analogue stock')


class RaceCommand(AbsCommand):

    def __init__(
        self,
        usersRepository: UsersRepository
    ):
        if usersRepository is None:
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__usersRepository = usersRepository
        self.__lastRaceMessageTimes = TimedDict(timedelta(minutes = 2))

    async def handleCommand(self, ctx):
        user = self.__usersRepository.getUser(ctx.channel.name)

        if not user.isRaceEnabled() or not ctx.author.is_mod:
            return
        elif not self.__lastRaceMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        await ctx.send('!race')
