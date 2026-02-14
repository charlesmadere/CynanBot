import random
from datetime import datetime, timedelta

from frozendict import frozendict

from .shinyTriviaOccurencesRepositoryInterface import ShinyTriviaOccurencesRepositoryInterface
from ..settings.triviaSettingsInterface import TriviaSettingsInterface
from ...cuteness.cutenessRepositoryInterface import CutenessRepositoryInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class ShinyTriviaHelper:

    def __init__(
        self,
        cutenessRepository: CutenessRepositoryInterface,
        shinyTriviaOccurencesRepository: ShinyTriviaOccurencesRepositoryInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        triviaSettings: TriviaSettingsInterface,
        cooldown: timedelta = timedelta(hours = 3),
    ):
        if not isinstance(cutenessRepository, CutenessRepositoryInterface):
            raise TypeError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif not isinstance(shinyTriviaOccurencesRepository, ShinyTriviaOccurencesRepositoryInterface):
            raise TypeError(f'shinyTriviaOccurencesRepository argument is malformed: \"{shinyTriviaOccurencesRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(triviaSettings, TriviaSettingsInterface):
            raise TypeError(f'triviaSettings argument is malformed: \"{triviaSettings}\"')
        elif not isinstance(cooldown, timedelta):
            raise TypeError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__cutenessRepository: CutenessRepositoryInterface = cutenessRepository
        self.__shinyTriviaOccurencesRepository: ShinyTriviaOccurencesRepositoryInterface = shinyTriviaOccurencesRepository
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__triviaSettings: TriviaSettingsInterface = triviaSettings
        self.__cooldown: timedelta = cooldown

        self.__rankToProbabilityDict: frozendict[int, float] = frozendict({
            1: 0.500,
            2: 0.550,
            3: 0.600,
            4: 0.650,
            5: 0.700,
            6: 0.750,
            7: 0.800,
            8: 0.850,
            9: 0.900,
            10: 0.950,
        })

    async def __getUserPlacementOnLeaderboard(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str,
    ) -> int | None:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        cutenessLeaderboard = await self.__cutenessRepository.fetchCutenessLeaderboard(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
        )

        if cutenessLeaderboard.entries is None or len(cutenessLeaderboard.entries) == 0:
            return None

        for entry in cutenessLeaderboard.entries:
            if entry.userId == userId:
                return entry.rank

        return None

    async def isShinyTriviaQuestion(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str,
        userName: str,
    ) -> bool:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        if not await self.__triviaSettings.areShinyTriviasEnabled():
            return False

        userPlacementOnLeaderboard = await self.__getUserPlacementOnLeaderboard(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            userId = userId,
        )

        probability = await self.__triviaSettings.getShinyProbability()

        if userPlacementOnLeaderboard is not None and userPlacementOnLeaderboard in self.__rankToProbabilityDict:
            probability = probability * self.__rankToProbabilityDict[userPlacementOnLeaderboard]

        if random.uniform(0, 1) > probability:
            return False

        details = await self.__shinyTriviaOccurencesRepository.fetchDetails(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            userId = userId,
        )

        mostRecent = details.mostRecent

        if mostRecent is not None:
            now = datetime.now(self.__timeZoneRepository.getDefault())

            if now - mostRecent < self.__cooldown:
                self.__timber.log('ShinyTriviaHelper', f'{userName}:{details.userId} in {details.twitchChannel} would have encountered a shiny, but it was rejected, as their most recent shiny ({details.mostRecent}) is within the cooldown time')
                return False

        result = await self.__shinyTriviaOccurencesRepository.incrementShinyCount(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            userId = userId,
        )

        self.__timber.log('ShinyTriviaHelper', f'In {twitchChannel}, {userName}:{result.userId} has encountered a shiny trivia question!')

        return True

    async def isShinySuperTriviaQuestion(self, twitchChannelId: str) -> bool:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not await self.__triviaSettings.areShinyTriviasEnabled():
            return False

        probability = await self.__triviaSettings.getShinyProbability()
        randomNumber = random.uniform(0, 1)

        if randomNumber > probability:
            return False

        self.__timber.log('ShinyTriviaHelper', f'A shiny super trivia question was encountered in {twitchChannelId}!')
        return True

    async def shinyTriviaWin(
        self,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str,
        userName: str,
    ):
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        result = await self.__shinyTriviaOccurencesRepository.incrementShinyCount(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            userId = userId,
        )

        self.__timber.log('ShinyTriviaHelper', f'In {twitchChannel}, {userName}:{result.userId} won a shiny trivia! (they have won {result.newShinyCountStr} total)')
