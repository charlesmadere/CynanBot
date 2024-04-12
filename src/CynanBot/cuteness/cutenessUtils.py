import CynanBot.misc.utils as utils
from CynanBot.cuteness.cutenessChampionsResult import CutenessChampionsResult
from CynanBot.cuteness.cutenessHistoryResult import CutenessHistoryResult
from CynanBot.cuteness.cutenessLeaderboardEntry import CutenessLeaderboardEntry
from CynanBot.cuteness.cutenessLeaderboardHistoryResult import \
    CutenessLeaderboardHistoryResult
from CynanBot.cuteness.cutenessResult import CutenessResult
from CynanBot.cuteness.cutenessUtilsInterface import CutenessUtilsInterface


class CutenessUtils(CutenessUtilsInterface):

    def __init__(self):
        pass

    def getCuteness(self, result: CutenessResult, delimiter: str) -> str:
        if not isinstance(result, CutenessResult):
            raise TypeError(f'result argument is malformed: \"{result}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        cuteness = result.getCuteness()

        if utils.isValidInt(cuteness) and cuteness >= 1:
            return f'@{result.getUserName()}\'s {result.getCutenessDate().getHumanString()} cuteness is {result.getCutenessStr()} ✨'
        else:
            return f'@{result.getUserName()} has no cuteness in {result.getCutenessDate().getHumanString()}'

    def getCutenessChampions(self, result: CutenessChampionsResult, delimiter: str) -> str:
        if not isinstance(result, CutenessChampionsResult):
            raise TypeError(f'result argument is malformed: \"{result}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        champions = result.getChampions()

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

        entries = result.getEntries()

        if entries is None or len(entries) == 0:
            return f'{result.getUserName()} has no cuteness history 😿'

        historyStrs: list[str] = list()

        for entry in entries:
            historyStrs.append(f'{entry.getCutenessDate().getHumanString()} ({entry.getCutenessStr()})')

        historyStr = delimiter.join(historyStrs)
        bestCuteness = result.getBestCuteness()
        totalCuteness = result.getTotalCuteness()

        if bestCuteness is not None and utils.isValidInt(totalCuteness) and totalCuteness >= 1:
            return f'@{result.getUserName()} has a total cuteness of {result.getTotalCutenessStr()} with their best ever cuteness being {bestCuteness.getCutenessStr()} in {bestCuteness.getCutenessDate().getHumanString()}. And here is their recent cuteness history: {historyStr} ✨'
        elif bestCuteness is not None and (not utils.isValidInt(totalCuteness) or totalCuteness == 0):
            return f'@{result.getUserName()}\'s best ever cuteness was {bestCuteness.getCutenessStr()} in {bestCuteness.getCutenessDate().getHumanString()}, with a recent cuteness history of {historyStr} ✨'
        elif bestCuteness is None and utils.isValidInt(totalCuteness) and totalCuteness >= 1:
            return f'@{result.getUserName()} has a total cuteness of {result.getTotalCutenessStr()}, with a recent cuteness history of {historyStr} ✨'
        else:
            return f'@{result.getUserName()}\'s recent cuteness history: {historyStr} ✨'

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

        leaderboards = result.getLeaderboards()

        if leaderboards is None or len(leaderboards) == 0:
            return f'There is no Cuteness Leaderboard History here 😿'

        leaderboardStrings: list[str] = list()

        for leaderboard in leaderboards:
            entries = leaderboard.getEntries()
            if entries is None or len(entries) == 0:
                continue

            entryStrings: list[str] = list()
            for entry in entries:
                entryStrings.append(self.__getLeaderboardPlacementString(entry))

            leaderboardStrings.append(f'{leaderboard.getCutenessDate().getHumanString()} {entryDelimiter.join(entryStrings)}')

        return f'Cuteness Leaderboard History — {leaderboardDelimiter.join(leaderboardStrings)} ✨'

    def __getLeaderboardPlacementString(self, entry: CutenessLeaderboardEntry) -> str:
        if not isinstance(entry, CutenessLeaderboardEntry):
            raise TypeError(f'result argument is malformed: \"{entry}\"')

        rankStr = ''

        if entry.getRank() == 1:
            rankStr = '🥇'
        elif entry.getRank() == 2:
            rankStr = '🥈'
        elif entry.getRank() == 3:
            rankStr = '🥉'
        else:
            rankStr = f'#{entry.getRankStr()}'

        return f'{rankStr} {entry.getUserName()} ({entry.getCutenessStr()})'
