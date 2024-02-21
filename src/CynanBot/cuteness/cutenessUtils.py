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
        assert isinstance(result, CutenessResult), f"malformed {result=}"
        assert isinstance(delimiter, str), f"malformed {delimiter=}"

        cuteness = result.getCuteness()

        if utils.isValidInt(cuteness) and cuteness >= 1:
            return f'@{result.getUserName()}\'s {result.getCutenessDate().getHumanString()} cuteness is {result.getCutenessStr()} ✨'
        else:
            return f'@{result.getUserName()} has no cuteness in {result.getCutenessDate().getHumanString()}'

    def getCutenessChampions(self, result: CutenessChampionsResult, delimiter: str) -> str:
        assert isinstance(result, CutenessChampionsResult), f"malformed {result=}"
        assert isinstance(delimiter, str), f"malformed {delimiter=}"

        champions = result.getChampions()

        if champions is None or len(champions) == 0:
            return f'There are no cuteness champions 😿'

        championsStrs: List[str] = list()

        for champion in champions:
            championsStrs.append(self.__getLeaderboardPlacementString(champion))

        championsStr = delimiter.join(championsStrs)
        return f'Cuteness Champions {championsStr} ✨'

    def getCutenessHistory(self, result: CutenessHistoryResult, delimiter: str) -> str:
        assert isinstance(result, CutenessHistoryResult), f"malformed {result=}"
        assert isinstance(delimiter, str), f"malformed {delimiter=}"

        entries = result.getEntries()

        if entries is None or len(entries) == 0:
            return f'{result.getUserName()} has no cuteness history 😿'

        historyStrs: List[str] = list()

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

    def getLeaderboard(self, entries: List[CutenessLeaderboardEntry], delimiter: str) -> str:
        if not isinstance(entries, List) or len(entries) == 0:
            raise ValueError(f'entries argument is malformed: \"{entries}\"')
        assert isinstance(delimiter, str), f"malformed {delimiter=}"

        entryStrings: List[str] = list()

        for entry in entries:
            entryStrings.append(self.__getLeaderboardPlacementString(entry))

        return delimiter.join(entryStrings)

    def getCutenessLeaderboardHistory(
        self,
        result: CutenessLeaderboardHistoryResult,
        entryDelimiter: str,
        leaderboardDelimiter: str
    ) -> str:
        assert isinstance(result, CutenessLeaderboardHistoryResult), f"malformed {result=}"
        assert isinstance(entryDelimiter, str), f"malformed {entryDelimiter=}"
        assert isinstance(leaderboardDelimiter, str), f"malformed {leaderboardDelimiter=}"

        leaderboards = result.getLeaderboards()

        if leaderboards is None or len(leaderboards) == 0:
            return f'There is no Cuteness Leaderboard History here 😿'

        leaderboardStrings: List[str] = list()

        for leaderboard in leaderboards:
            entries = leaderboard.getEntries()
            if entries is None or len(entries) == 0:
                continue

            entryStrings: List[str] = list()
            for entry in entries:
                entryStrings.append(self.__getLeaderboardPlacementString(entry))

            leaderboardStrings.append(f'{leaderboard.getCutenessDate().getHumanString()} {entryDelimiter.join(entryStrings)}')

        return f'Cuteness Leaderboard History — {leaderboardDelimiter.join(leaderboardStrings)} ✨'

    def __getLeaderboardPlacementString(self, entry: CutenessLeaderboardEntry) -> str:
        assert isinstance(entry, CutenessLeaderboardEntry), f"malformed {entry=}"

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
