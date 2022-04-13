from typing import List

import CynanBotCommon.utils as utils
from cuteness.cutenessEntry import CutenessEntry
from cuteness.cutenessHistoryResult import CutenessHistoryResult
from cuteness.cutenessLeaderboardEntry import CutenessLeaderboardEntry
from cuteness.cutenessResult import CutenessResult


class CutenessUtils():

    def __init__(self):
        pass

    def getCuteness(self, result: CutenessResult) -> str:
        if result is None:
            raise ValueError(f'result argument is malformed: \"{result}\"')

        if result.hasCuteness() and result.getCuteness() >= 1:
            if result.hasLocalLeaderboard():
                localLeaderboard = self.getLocalLeaderboard(result.getLocalLeaderboard())
                return f'{result.getUserName()}\'s {result.getCutenessDate().toStr()} cuteness is {result.getCutenessStr()}, and their local leaderboard is: {localLeaderboard} ✨'
            else:
                return f'{result.getUserName()}\'s {result.getCutenessDate().toStr()} cuteness is {result.getCutenessStr()} ✨'
        else:
            return f'{result.getUserName()} has no cuteness in {result.getCutenessDate().toStr()}'

    def getCutenessHistory(self, result: CutenessHistoryResult, delimiter: str) -> str:
        if result is None:
            raise ValueError(f'result argument is malformed: \"{result}\"')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        if not result.hasEntries():
            return f'{result.getUserName()} has no cuteness history 😿'

        bestCuteness = result.getBestCuteness()

        historyStrs: List[str] = list()
        for entry in result.getEntries():
            historyStrs.append(f'{entry.getCutenessDate().toStr()} ({entry.getCutenessStr()})')
        historyStr = delimiter.join(historyStrs)

        if bestCuteness is not None and result.hasTotalCuteness():
            return f'{result.getUserName()} has a total cuteness of {result.getTotalCutenessStr()} with their best ever cuteness being {bestCuteness.getCutenessStr()} in {bestCuteness.getCutenessDate()}. And here is their cuteness history: {historyStr} ✨'
        elif bestCuteness is not None and not result.hasTotalCuteness():
            return f'{result.getUserName()}\'s best ever cuteness was {bestCuteness.getCutenessStr()} in {bestCuteness.getCutenessDate()}, with a cuteness history of {historyStr} ✨'
        elif bestCuteness is None and result.hasTotalCuteness():
            return f'{result.getUserName()} has a total cuteness of {result.getTotalCutenessStr()}, with a cuteness history of {historyStr} ✨'
        else:
            return f'{result.getUserName()}\'s cuteness history: {historyStr} ✨'

    def getLeaderboard(self, entries: List[CutenessLeaderboardEntry], delimiter: str) -> str:
        if not utils.hasItems(entries):
            raise ValueError(f'entries argument is malformed: \"{entries}\"')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        entryStrings: List[str] = list()

        for entry in entries:
            entryStrings.append(self.getLeaderboardPlacement(entry))

        return delimiter.join(entryStrings)

    def getLeaderboardPlacement(self, entry: CutenessLeaderboardEntry) -> str:
        if entry is None:
            raise ValueError(f'result argument is malformed: \"{entry}\"')

        return f'#{entry.getRankStr()} {entry.getUserName()} ({entry.getCutenessStr()})'

    def getLocalLeaderboard(self, entries: List[CutenessEntry], delimiter: str) -> str:
        if not utils.hasItems(entries):
            raise ValueError(f'entries argument is malformed: \"{entries}\"')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        entryStrings: List[str] = list()

        for entry in entries:
            entryStrings.append(self.getLocalLeaderboardPlacement(entry))

        return delimiter.join(entryStrings)

    def getLocalLeaderboardPlacement(self, entry: CutenessEntry) -> str:
        if entry is None:
            raise ValueError(f'entry argument is malformed: \"{entry}\"')

        return f'{entry.getUserName()} ({entry.getCutenessStr()})'
