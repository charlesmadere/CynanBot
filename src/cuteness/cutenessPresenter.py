import locale
from datetime import datetime

from .cutenessPresenterInterface import CutenessPresenterInterface
from .models.preparedCutenessChampionsResult import PreparedCutenessChampionsResult
from .models.preparedCutenessHistoryResult import PreparedCutenessHistoryResult
from .models.preparedCutenessLeaderboardEntry import PreparedCutenessLeaderboardEntry
from .models.preparedCutenessLeaderboardHistoryResult import PreparedCutenessLeaderboardHistoryResult
from .models.preparedCutenessLeaderboardResult import PreparedCutenessLeaderboardResult
from .models.preparedCutenessResult import PreparedCutenessResult
from ..misc import utils as utils


class CutenessPresenter(CutenessPresenterInterface):

    async def printCuteness(
        self,
        result: PreparedCutenessResult,
    ) -> str:
        if not isinstance(result, PreparedCutenessResult):
            raise TypeError(f'result argument is malformed: \"{result}\"')

        if result.cuteness is not None and result.requireCuteness() >= 1:
            return f'✨ {result.chatterUserName}\'s {self.printCutenessDate(result.cutenessDate)} cuteness is {result.cutenessStr}'
        else:
            return f'😿 {result.chatterUserName} has no cuteness in {self.printCutenessDate(result.cutenessDate)}'

    async def printCutenessChampions(
        self,
        result: PreparedCutenessChampionsResult,
        delimiter: str = ', ',
    ) -> str:
        if not isinstance(result, PreparedCutenessChampionsResult):
            raise TypeError(f'result argument is malformed: \"{result}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        if len(result.champions) == 0:
            return f'😿 There are no cuteness champions'

        championsStrings: list[str] = list()

        for champion in result.champions:
            championsStrings.append(self.printLeaderboardPlacement(champion))

        championsString = delimiter.join(championsStrings)
        return f'✨ Cuteness Champions {championsString}'

    def printCutenessDate(self, dateTime: datetime) -> str:
        if not isinstance(dateTime, datetime):
            raise TypeError(f'dateTime argument is malformed: \"{dateTime}\"')

        return dateTime.strftime('%b %Y')

    def printCutenessHistory(
        self,
        result: PreparedCutenessHistoryResult,
        delimiter: str = ', ',
    ) -> str:
        if not isinstance(result, PreparedCutenessHistoryResult):
            raise TypeError(f'result argument is malformed: \"{result}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        if len(result.historyEntries) == 0:
            return f'😿 @{result.chatterUserName} has no cuteness history'

        historyStrs: list[str] = list()

        for historyEntry in result.historyEntries:
            historyStrs.append(f'{self.printCutenessDate(historyEntry.cutenessDate)} ({historyEntry.cutenessStr})')

        historyStr = delimiter.join(historyStrs)
        bestCuteness = result.bestCuteness
        totalCuteness = result.totalCuteness

        if bestCuteness is not None and totalCuteness >= 1:
            return f'✨ @{result.chatterUserName} has a total cuteness of {result.totalCutenessStr} with their best ever cuteness being {bestCuteness.cutenessStr} in {self.printCutenessDate(bestCuteness.cutenessDate)}. And here is their recent cuteness history: {historyStr}'
        elif bestCuteness is not None and (totalCuteness is None or totalCuteness == 0):
            return f'✨ @{result.chatterUserName}\'s best ever cuteness was {bestCuteness.cutenessStr} in {self.printCutenessDate(bestCuteness.cutenessDate)}, with a recent cuteness history of {historyStr}'
        elif bestCuteness is None and utils.isValidInt(totalCuteness) and totalCuteness >= 1:
            return f'✨ @{result.chatterUserName} has a total cuteness of {result.totalCutenessStr}, with a recent cuteness history of {historyStr}'
        else:
            return f'✨ @{result.chatterUserName}\'s recent cuteness history: {historyStr}'

    async def printLeaderboard(
        self,
        result: PreparedCutenessLeaderboardResult,
        delimiter: str = ', ',
    ) -> str:
        if not isinstance(result, PreparedCutenessLeaderboardResult):
            raise TypeError(f'result argument is malformed: \"{result}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        if len(result.entries) == 0:
            return f'😿 {self.printCutenessDate(result.cutenessDate)} leaderboard is empty'

        specificLookupText: str | None = None

        if result.specificLookupCutenessResult is not None:
            cutenessStr: str

            if result.specificLookupCutenessResult.cuteness is None:
                cutenessStr = locale.format_string("%d", 0, grouping = True)
            else:
                cutenessStr = result.specificLookupCutenessResult.cutenessStr

            specificLookupText = f'@{result.specificLookupCutenessResult.chatterUserName} your cuteness is {cutenessStr}'

        entryStrings: list[str] = list()

        for entry in result.entries:
            entryStrings.append(self.printLeaderboardPlacement(entry))

        entriesString = delimiter.join(entryStrings)

        if utils.isValidStr(specificLookupText):
            return f'✨ {specificLookupText}, and the {self.printCutenessDate(result.cutenessDate)} leaderboard is: {entriesString}'
        else:
            return f'✨ {self.printCutenessDate(result.cutenessDate)} leaderboard {entriesString}'

    async def printLeaderboardHistory(
        self,
        result: PreparedCutenessLeaderboardHistoryResult,
        entryDelimiter: str = ', ',
        leaderboardDelimiter: str = ' — ',
    ) -> str:
        if not isinstance(result, PreparedCutenessLeaderboardHistoryResult):
            raise TypeError(f'result argument is malformed: \"{result}\"')
        elif not isinstance(entryDelimiter, str):
            raise TypeError(f'entryDelimiter argument is malformed: \"{entryDelimiter}\"')
        elif not isinstance(leaderboardDelimiter, str):
            raise TypeError(f'leaderboardDelimiter argument is malformed: \"{leaderboardDelimiter}\"')

        if len(result.history) == 0:
            return f'😿 There is no Cuteness leaderboard history here'

        leaderboardStrings: list[str] = list()

        for leaderboard in result.history:
            if len(leaderboard.entries) == 0:
                continue

            entryStrings: list[str] = list()
            for entry in leaderboard.entries:
                entryStrings.append(self.printLeaderboardPlacement(entry))

            leaderboardStrings.append(f'{self.printCutenessDate(leaderboard.cutenessDate)} {entryDelimiter.join(entryStrings)}')

        return f'✨ Cuteness leaderboard history — {leaderboardDelimiter.join(leaderboardStrings)}'

    def printLeaderboardPlacement(
        self,
        entry: PreparedCutenessLeaderboardEntry,
    ) -> str:
        if not isinstance(entry, PreparedCutenessLeaderboardEntry):
            raise TypeError(f'result argument is malformed: \"{entry}\"')

        rankStr: str

        match entry.rank:
            case 1: rankStr = '🥇'
            case 2: rankStr = '🥈'
            case 3: rankStr = '🥉'
            case _: rankStr = f'#{entry.rankStr}'

        return f'{rankStr} {entry.chatterUserName} ({entry.cutenessStr})'
