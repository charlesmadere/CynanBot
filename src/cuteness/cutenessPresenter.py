from typing import Final

from .cutenessChampionsResult import CutenessChampionsResult
from .cutenessLeaderboardEntry import CutenessLeaderboardEntry
from .cutenessLeaderboardResult import CutenessLeaderboardResult
from .cutenessPresenterInterface import CutenessPresenterInterface
from .cutenessResult import CutenessResult
from ..misc import utils as utils
from ..twitch.userIds.twitchUserIdsRepositoryInterface import TwitchUserIdsRepositoryInterface


class CutenessPresenter(CutenessPresenterInterface):

    def __init__(
        self,
        twitchUserIdsRepository: TwitchUserIdsRepositoryInterface,
    ):
        if not isinstance(twitchUserIdsRepository, TwitchUserIdsRepositoryInterface):
            raise TypeError(f'twitchUserIdsRepository argument is malformed: \"{twitchUserIdsRepository}\"')

        self.__twitchUserIdsRepository: Final[TwitchUserIdsRepositoryInterface] = twitchUserIdsRepository

    async def printCuteness(
        self,
        result: CutenessResult,
    ) -> str:
        if not isinstance(result, CutenessResult):
            raise TypeError(f'result argument is malformed: \"{result}\"')

        chatterUserData = await self.__twitchUserIdsRepository.requireById(result.userId)

        if utils.isValidInt(result.cuteness) and result.cuteness >= 1:
            return f'{chatterUserData.userName}\'s {result.cutenessDate.getHumanString()} cuteness is {result.cutenessStr} ✨'
        else:
            return f'{chatterUserData.userName} has no cuteness in {result.cutenessDate.getHumanString()}'

    async def printCutenessChampions(
        self,
        result: CutenessChampionsResult,
        delimiter: str = ', ',
    ) -> str:
        if not isinstance(result, CutenessChampionsResult):
            raise TypeError(f'result argument is malformed: \"{result}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        if result.champions is None or len(result.champions) == 0:
            return f'😿 There are no cuteness champions'

        championsStrings: list[str] = list()

        for champion in result.champions:
            championsStrings.append(await self.printLeaderboardPlacement(champion))

        championsString = delimiter.join(championsStrings)
        return f'✨ Cuteness Champions {championsString}'

    async def printLeaderboard(
        self,
        result: CutenessLeaderboardResult,
        delimiter: str = ', ',
    ) -> str:
        if not isinstance(result, CutenessLeaderboardResult):
            raise TypeError(f'result argument is malformed: \"{result}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        if result.entries is None or len(result.entries) == 0:
            return f'😿 {result.cutenessDate.getHumanString()} Leaderboard is empty'

        specificLookupText: str | None = None

        if result.specificLookupCutenessResult is not None:
            lookupUserData = await self.__twitchUserIdsRepository.requireById(
                userId = result.specificLookupCutenessResult.userId,
            )

            cutenessStr = result.specificLookupCutenessResult.cutenessStr
            specificLookupText = f'@{lookupUserData.userName} your cuteness is {cutenessStr}'

        entryStrings: list[str] = list()

        for entry in result.entries:
            entryStrings.append(await self.printLeaderboardPlacement(entry))

        entriesString = delimiter.join(entryStrings)

        if utils.isValidStr(specificLookupText):
            return f'✨ {specificLookupText}, and the {result.cutenessDate.getHumanString()} leaderboard is: {entriesString}'
        else:
            return f'✨ {result.cutenessDate.getHumanString()} leaderboard {entriesString}'

    async def printLeaderboardPlacement(
        self,
        entry: CutenessLeaderboardEntry,
    ) -> str:
        if not isinstance(entry, CutenessLeaderboardEntry):
            raise TypeError(f'result argument is malformed: \"{entry}\"')

        rankStr: str

        match entry.rank:
            case 1: rankStr = '🥇'
            case 2: rankStr = '🥈'
            case 3: rankStr = '🥉'
            case _: rankStr = f'#{entry.rankStr}'

        chatterUserData = await self.__twitchUserIdsRepository.requireById(entry.userId)
        return f'{rankStr} {chatterUserData.userName} ({entry.cutenessStr})'
