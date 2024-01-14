from typing import List

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
            raise ValueError(f'result argument is malformed: \"{result}\"')
        elif not isinstance(delimiter, str):
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        cuteness = result.getCuteness()

        if utils.isValidInt(cuteness) and cuteness >= 1:
            return f'@{result.getUserName()}\'s {result.getCutenessDate().toStr()} cuteness is {result.getCutenessStr()} ✨'
        else:
            return f'@{result.getUserName()} has no cuteness in {result.getCutenessDate().toStr()}'

    def getCutenessChampions(self, result: CutenessChampionsResult, delimiter: str) -> str:
        if not isinstance(result, CutenessChampionsResult):
            raise ValueError(f'result argument is malformed: \"{result}\"')
        elif not isinstance(delimiter, str):
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        champions = result.getChampions()

        if champions is None or len(champions) == 0:
            return f'There are no cuteness champions 😿'

        championsStrs: List[str] = list()

        for champion in champions:
            championsStrs.append(self.getLeaderboardPlacement(champion))

        championsStr = delimiter.join(championsStrs)
        return f'Cuteness Champions {championsStr} ✨'

    def getCutenessHistory(self, result: CutenessHistoryResult, delimiter: str) -> str:
        if not isinstance(result, CutenessHistoryResult):
            raise ValueError(f'result argument is malformed: \"{result}\"')
        elif not isinstance(delimiter, str):
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        entries = result.getEntries()

        if entries is None or len(entries) == 0:
            return f'{result.getUserName()} has no cuteness history 😿'

        historyStrs: List[str] = list()

        for entry in entries:
            historyStrs.append(f'{entry.getCutenessDate().toStr()} ({entry.getCutenessStr()})')

        historyStr = delimiter.join(historyStrs)
        bestCuteness = result.getBestCuteness()
        totalCuteness = result.getTotalCuteness()

        if bestCuteness is not None and utils.isValidInt(totalCuteness) and totalCuteness >= 1:
            return f'@{result.getUserName()} has a total cuteness of {result.getTotalCutenessStr()} with their best ever cuteness being {bestCuteness.getCutenessStr()} in {bestCuteness.getCutenessDate().toStr()}. And here is their recent cuteness history: {historyStr} ✨'
        elif bestCuteness is not None and (not utils.isValidInt(totalCuteness) or totalCuteness == 0):
            return f'@{result.getUserName()}\'s best ever cuteness was {bestCuteness.getCutenessStr()} in {bestCuteness.getCutenessDate().toStr()}, with a recent cuteness history of {historyStr} ✨'
        elif bestCuteness is None and utils.isValidInt(totalCuteness) and totalCuteness >= 1:
            return f'@{result.getUserName()} has a total cuteness of {result.getTotalCutenessStr()}, with a recent cuteness history of {historyStr} ✨'
        else:
            return f'@{result.getUserName()}\'s recent cuteness history: {historyStr} ✨'

    def getLeaderboard(self, entries: List[CutenessLeaderboardEntry], delimiter: str) -> str:
        if not utils.hasItems(entries):
            raise ValueError(f'entries argument is malformed: \"{entries}\"')
        elif not isinstance(delimiter, str):
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        entryStrings: List[str] = list()

        for entry in entries:
            entryStrings.append(self.getLeaderboardPlacement(entry))

        return delimiter.join(entryStrings)

    def getCutenessLeaderboardHistory(
        self,
        result: CutenessLeaderboardHistoryResult,
        entryDelimiter: str,
        leaderboardDelimiter: str
    ) -> str:
        if not isinstance(result, CutenessLeaderboardHistoryResult):
            raise ValueError(f'result argument is malformed: \"{result}\"')
        elif not isinstance(entryDelimiter, str):
            raise ValueError(f'entryDelimiter argument is malformed: \"{entryDelimiter}\"')
        elif not isinstance(leaderboardDelimiter, str):
            raise ValueError(f'leaderboardDelimiter argument is malformed: \"{leaderboardDelimiter}\"')

        leaderboards = result.getLeaderboards()

        if leaderboards is None or len(leaderboards) == 0:
            return f'There is no cuteness leaderboard history here 😿'

        leaderboardStrings: List[str] = list()

        for leaderboard in leaderboards:
            entries = leaderboard.getEntries()
            if entries is None or len(entries) == 0:
                continue

            entryStrings: List[str] = list()
            for entry in entries:
                entryStrings.append(self.getLeaderboardPlacement(entry))

            leaderboardStrings.append(f'{leaderboard.getCutenessDate().toStr()} {entryDelimiter.join(entryStrings)}')

        return f'Cuteness leaderboard history — {leaderboardDelimiter.join(leaderboardStrings)}'

    def getLeaderboardPlacement(self, entry: CutenessLeaderboardEntry) -> str:
        if not isinstance(entry, CutenessLeaderboardEntry):
            raise ValueError(f'result argument is malformed: \"{entry}\"')

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
