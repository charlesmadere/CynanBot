from .cutenessChampionsResult import CutenessChampionsResult
from .cutenessHistoryResult import CutenessHistoryResult
from .cutenessLeaderboardEntry import CutenessLeaderboardEntry
from .cutenessLeaderboardHistoryResult import \
    CutenessLeaderboardHistoryResult
from .cutenessResult import CutenessResult
from .cutenessUtilsInterface import CutenessUtilsInterface
from ..misc import utils as utils


class CutenessUtils(CutenessUtilsInterface):

    def __init__(self):
        pass

    def getCuteness(self, result: CutenessResult, delimiter: str) -> str:
        if not isinstance(result, CutenessResult):
            raise TypeError(f'result argument is malformed: \"{result}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        cuteness = result.cuteness

        if utils.isValidInt(cuteness) and cuteness >= 1:
            return f'@{result.userName}\'s {result.cutenessDate.getHumanString()} cuteness is {result.cutenessStr} ✨'
        else:
            return f'@{result.userName} has no cuteness in {result.cutenessDate.getHumanString()}'

    def getCutenessChampions(self, result: CutenessChampionsResult, delimiter: str) -> str:
        if not isinstance(result, CutenessChampionsResult):
            raise TypeError(f'result argument is malformed: \"{result}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        champions = result.champions

        if champions is None or len(champions) == 0:
            return f'There are no cuteness champions 😿'

        championsStrs: list[str] = list()

        for champion in champions:
            championsStrs.append(self.__getLeaderboardPlacementString(champion))

        championsStr = delimiter.join(championsStrs)
        return f'Cuteness Champions {championsStr} ✨'

    def getCutenessHistory(self, result: CutenessHistoryResult, delimiter: str) -> str:
        if not isinstance(result, CutenessHistoryResult):
            raise TypeError(f'result argument is malformed: \"{result}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        if result.entries is None or len(result.entries) == 0:
            return f'{result.userName} has no cuteness history 😿'

        historyStrs: list[str] = list()

        for entry in result.entries:
            historyStrs.append(f'{entry.cutenessDate.getHumanString()} ({entry.cutenessStr})')

        historyStr = delimiter.join(historyStrs)
        bestCuteness = result.bestCuteness
        totalCuteness = result.totalCuteness

        if bestCuteness is not None and utils.isValidInt(totalCuteness) and totalCuteness >= 1:
            return f'@{result.userName} has a total cuteness of {result.totalCutenessStr} with their best ever cuteness being {bestCuteness.cutenessStr} in {bestCuteness.cutenessDate.getHumanString()}. And here is their recent cuteness history: {historyStr} ✨'
        elif bestCuteness is not None and (not utils.isValidInt(totalCuteness) or totalCuteness == 0):
            return f'@{result.userName}\'s best ever cuteness was {bestCuteness.cutenessStr} in {bestCuteness.cutenessDate.getHumanString()}, with a recent cuteness history of {historyStr} ✨'
        elif bestCuteness is None and utils.isValidInt(totalCuteness) and totalCuteness >= 1:
            return f'@{result.userName} has a total cuteness of {result.totalCutenessStr}, with a recent cuteness history of {historyStr} ✨'
        else:
            return f'@{result.userName}\'s recent cuteness history: {historyStr} ✨'

    def getLeaderboard(self, entries: list[CutenessLeaderboardEntry], delimiter: str) -> str:
        if not isinstance(entries, list) or len(entries) == 0:
            raise TypeError(f'entries argument is malformed: \"{entries}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        entryStrings: list[str] = list()

        for entry in entries:
            entryStrings.append(self.__getLeaderboardPlacementString(entry))

        return delimiter.join(entryStrings)

    def getCutenessLeaderboardHistory(
        self,
        result: CutenessLeaderboardHistoryResult,
        entryDelimiter: str,
        leaderboardDelimiter: str
    ) -> str:
        if not isinstance(result, CutenessLeaderboardHistoryResult):
            raise TypeError(f'result argument is malformed: \"{result}\"')
        elif not isinstance(entryDelimiter, str):
            raise TypeError(f'entryDelimiter argument is malformed: \"{entryDelimiter}\"')
        elif not isinstance(leaderboardDelimiter, str):
            raise TypeError(f'leaderboardDelimiter argument is malformed: \"{leaderboardDelimiter}\"')

        leaderboards = result.leaderboards

        if leaderboards is None or len(leaderboards) == 0:
            return f'There is no Cuteness Leaderboard History here 😿'

        leaderboardStrings: list[str] = list()

        for leaderboard in leaderboards:
            if leaderboard.entries is None or len(leaderboard.entries) == 0:
                continue

            entryStrings: list[str] = list()
            for entry in leaderboard.entries:
                entryStrings.append(self.__getLeaderboardPlacementString(entry))

            leaderboardStrings.append(f'{leaderboard.cutenessDate.getHumanString()} {entryDelimiter.join(entryStrings)}')

        return f'Cuteness Leaderboard History — {leaderboardDelimiter.join(leaderboardStrings)} ✨'

    def __getLeaderboardPlacementString(self, entry: CutenessLeaderboardEntry) -> str:
        if not isinstance(entry, CutenessLeaderboardEntry):
            raise TypeError(f'result argument is malformed: \"{entry}\"')

        rankStr = ''

        if entry.rank == 1:
            rankStr = '🥇'
        elif entry.rank == 2:
            rankStr = '🥈'
        elif entry.rank == 3:
            rankStr = '🥉'
        else:
            rankStr = f'#{entry.rankStr}'

        return f'{rankStr} {entry.userName} ({entry.cutenessStr})'
