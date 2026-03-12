from .cutenessChampionsResult import CutenessChampionsResult
from .cutenessLeaderboardEntry import CutenessLeaderboardEntry
from .cutenessLeaderboardResult import CutenessLeaderboardResult
from .cutenessPresenterInterface import CutenessPresenterInterface
from .cutenessResult import CutenessResult
from ..misc import utils as utils


class CutenessPresenter(CutenessPresenterInterface):

    async def printCuteness(self, result: CutenessResult) -> str:
        if not isinstance(result, CutenessResult):
            raise TypeError(f'result argument is malformed: \"{result}\"')

        if utils.isValidInt(result.cuteness) and result.cuteness >= 1:
            return f'{result.userName}\'s {result.cutenessDate.getHumanString()} cuteness is {result.cutenessStr} ✨'
        else:
            return f'{result.userName} has no cuteness in {result.cutenessDate.getHumanString()}'

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

        championsStrs: list[str] = list()

        for champion in result.champions:
            championsStrs.append(await self.printLeaderboardPlacement(champion))

        championsStr = delimiter.join(championsStrs)
        return f'✨ Cuteness Champions {championsStr}'

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
            userName = result.specificLookupCutenessResult.userName
            cutenessStr = result.specificLookupCutenessResult.cutenessStr
            specificLookupText = f'@{userName} your cuteness is {cutenessStr}'

        entryStrings: list[str] = list()

        for entry in result.entries:
            entryStrings.append(await self.printLeaderboardPlacement(entry))

        entriesString = delimiter.join(entryStrings)

        if utils.isValidStr(specificLookupText):
            return f'✨ {specificLookupText}, and the {result.cutenessDate.getHumanString()} Leaderboard is: {entriesString}'
        else:
            return f'✨ {result.cutenessDate.getHumanString()} Leaderboard {entriesString}'

    async def printLeaderboardPlacement(self, entry: CutenessLeaderboardEntry) -> str:
        if not isinstance(entry, CutenessLeaderboardEntry):
            raise TypeError(f'result argument is malformed: \"{entry}\"')

        rankStr: str

        match entry.rank:
            case 1: rankStr = '🥇'
            case 2: rankStr = '🥈'
            case 3: rankStr = '🥉'
            case _: rankStr = f'#{entry.rankStr}'

        return f'{rankStr} {entry.userName} ({entry.cutenessStr})'
