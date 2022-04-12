from typing import List

import CynanBotCommon.utils as utils
from cuteness.cutenessEntry import CutenessEntry
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
