import locale

from ...misc import utils as utils


class TriviaScoreResult:

    def __init__(
        self,
        streak: int,
        superTriviaWins: int,
        triviaLosses: int,
        triviaWins: int,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str
    ):
        if not utils.isValidInt(streak):
            raise TypeError(f'streak argument is malformed: \"{streak}\"')
        elif not utils.isValidInt(superTriviaWins):
            raise TypeError(f'superTriviaWins argument is malformed: \"{superTriviaWins}\"')
        elif superTriviaWins < 0 or superTriviaWins > utils.getIntMaxSafeSize():
            raise ValueError(f'superTriviaWins argument is out of bounds: {superTriviaWins}')
        elif not utils.isValidInt(triviaLosses):
            raise TypeError(f'triviaLosses argument is malformed: \"{triviaLosses}\"')
        elif triviaLosses < 0 or triviaLosses > utils.getIntMaxSafeSize():
            raise ValueError(f'triviaLosses argument is out of bounds: {triviaLosses}')
        elif not utils.isValidInt(triviaWins):
            raise TypeError(f'triviaWins argument is malformed: \"{triviaWins}\"')
        elif triviaWins < 0 or triviaWins > utils.getIntMaxSafeSize():
            raise ValueError(f'triviaWins argument is out of bounds: {triviaWins}')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        self.__streak: int = streak
        self.__superTriviaWins: int = superTriviaWins
        self.__triviaLosses: int = triviaLosses
        self.__triviaWins: int = triviaWins
        self.__twitchChannel: str = twitchChannel
        self.__twitchChannelId: str = twitchChannelId
        self.__userId: str = userId

    def getAbsStreak(self) -> int:
        return abs(self.__streak)

    def getAbsStreakStr(self) -> str:
        return locale.format_string("%d", self.getAbsStreak(), grouping = True)

    def getStreak(self) -> int:
        return self.__streak

    def getStreakStr(self) -> str:
        return locale.format_string("%d", self.__streak, grouping = True)

    def getSuperTriviaWins(self) -> int:
        return self.__superTriviaWins

    def getSuperTriviaWinsStr(self) -> str:
        return locale.format_string("%d", self.__superTriviaWins, grouping = True)

    def getTotal(self) -> int:
        return self.__triviaLosses + self.__triviaWins

    def getTotalStr(self) -> str:
        return locale.format_string("%d", self.getTotal(), grouping = True)

    def getTriviaLosses(self) -> int:
        return self.__triviaLosses

    def getTriviaLossesStr(self) -> str:
        return locale.format_string("%d", self.__triviaLosses, grouping = True)

    def getTriviaWins(self) -> int:
        return self.__triviaWins

    def getTriviaWinsStr(self) -> str:
        return locale.format_string("%d", self.__triviaWins, grouping = True)

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def getTwitchChannelId(self) -> str:
        return self.__twitchChannelId

    def getUserId(self) -> str:
        return self.__userId

    def getWinPercent(self) -> float:
        total = self.getTotal()

        if total == 0:
            return float(0)

        winPercent = float(self.__triviaWins) / float(total)

        if winPercent < 0:
            return float(0)
        elif winPercent > 1:
            return float(1)
        else:
            return winPercent

    def getWinPercentStr(self) -> str:
        winPercent = round(self.getWinPercent() * float(100), 2)
        return f'{winPercent}%'
