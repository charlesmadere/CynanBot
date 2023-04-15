from typing import List

import CynanBotCommon.utils as utils
from CynanBotCommon.cuteness.cutenessChampionsResult import \
    CutenessChampionsResult
from CynanBotCommon.cuteness.cutenessHistoryResult import CutenessHistoryResult
from CynanBotCommon.cuteness.cutenessLeaderboardEntry import \
    CutenessLeaderboardEntry
from CynanBotCommon.cuteness.cutenessLeaderboardHistoryResult import \
    CutenessLeaderboardHistoryResult
from CynanBotCommon.cuteness.cutenessResult import CutenessResult


class CutenessUtils():

    def __init__(self):
        pass

    def getCuteness(self, result: CutenessResult, delimiter: str) -> str:
        if not isinstance(result, CutenessResult):
            raise ValueError(f'result argument is malformed: \"{result}\"')
        elif not isinstance(delimiter, str):
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        if result.hasCuteness() and result.getCuteness() >= 1:
            return f'@{result.getUserName()}\'s {result.getCutenessDate().toStr()} cuteness is {result.getCutenessStr()} ✨'
        else:
            return f'@{result.getUserName()} has no cuteness in {result.getCutenessDate().toStr()}'

    def getCutenessChampions(self, result: CutenessChampionsResult, delimiter: str) -> str:
        if not isinstance(result, CutenessChampionsResult):
            raise ValueError(f'result argument is malformed: \"{result}\"')
        elif not isinstance(delimiter, str):
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        if not result.hasChampions():
            return f'There are no cuteness champions 😿'

        championsStrs: List[str] = list()
        for entry in result.getChampions():
            championsStrs.append(self.getLeaderboardPlacement(entry))

        championsStr = delimiter.join(championsStrs)
        return f'Cuteness Champions ✨ {championsStr} ✨'

    def getCutenessHistory(self, result: CutenessHistoryResult, delimiter: str) -> str:
        if not isinstance(result, CutenessHistoryResult):
            raise ValueError(f'result argument is malformed: \"{result}\"')
        elif not isinstance(delimiter, str):
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        if not result.hasEntries():
            return f'{result.getUserName()} has no cuteness history 😿'

        historyStrs: List[str] = list()

        for entry in result.getEntries():
            historyStrs.append(f'{entry.getCutenessDate().toStr()} ({entry.getCutenessStr()})')

        historyStr = delimiter.join(historyStrs)

        if result.hasBestCuteness() and result.hasTotalCuteness():
            return f'@{result.getUserName()} has a total cuteness of {result.getTotalCutenessStr()} with their best ever cuteness being {result.getBestCuteness().getCutenessStr()} in {result.getBestCuteness().getCutenessDate().toStr()}. And here is their recent cuteness history: {historyStr} ✨'
        elif result.hasBestCuteness() and not result.hasTotalCuteness():
            return f'@{result.getUserName()}\'s best ever cuteness was {result.getBestCuteness().getCutenessStr()} in {result.getBestCuteness().getCutenessDate().toStr()}, with a recent cuteness history of {historyStr} ✨'
        elif not result.hasBestCuteness() and result.hasTotalCuteness():
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

        if not result.hasLeaderboards():
            return f'@{result.getTwitchChannel()} has no cuteness leaderboard history 😿'

        leaderboardStrings: List[str] = list()

        for leaderboard in result.getLeaderboards():
            if not leaderboard.hasEntries():
                continue

            entryStrings: List[str] = list()
            for entry in leaderboard.getEntries():
                entryStrings.append(self.getLeaderboardPlacement(entry))

            leaderboardStrings.append(f'{leaderboard.getCutenessDate().toStr()} {entryDelimiter.join(entryStrings)}')

        return f'Cuteness leaderboard history — {leaderboardDelimiter.join(leaderboardStrings)}'

    def getLeaderboardPlacement(self, entry: CutenessLeaderboardEntry) -> str:
        if not isinstance(entry, CutenessLeaderboardEntry):
            raise ValueError(f'result argument is malformed: \"{entry}\"')

        rankStr: str = ''
        if entry.getRank() == 1:
            rankStr = '🥇'
        elif entry.getRank() == 2:
            rankStr = '🥈'
        elif entry.getRank() == 3:
            rankStr = '🥉'
        else:
            rankStr = f'#{entry.getRankStr()}'

        return f'{rankStr} {entry.getUserName()} ({entry.getCutenessStr()})'
