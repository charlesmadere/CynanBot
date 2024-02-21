import CynanBot.misc.utils as utils
from CynanBot.trivia.questions.triviaSource import TriviaSource


class BannedTriviaQuestion():

    def __init__(
        self,
        triviaId: str,
        userId: str,
        userName: str,
        triviaSource: TriviaSource
    ):
        if not utils.isValidStr(triviaId):
            raise ValueError(f'triviaId argument is malformed: \"{triviaId}\"')
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        if not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')
        assert isinstance(triviaSource, TriviaSource), f"malformed {triviaSource=}"

        self.__triviaId: str = triviaId
        self.__userId: str = userId
        self.__userName: str = userName
        self.__triviaSource: TriviaSource = triviaSource

    def getTriviaId(self) -> str:
        return self.__triviaId

    def getTriviaSource(self) -> TriviaSource:
        return self.__triviaSource

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName

    def __str__(self) -> str:
        return f'triviaId=\"{self.__triviaId}\", triviaSource=\"{self.__triviaSource}\", userId=\"{self.__userId}\", userName=\"{self.__userName}\"'
