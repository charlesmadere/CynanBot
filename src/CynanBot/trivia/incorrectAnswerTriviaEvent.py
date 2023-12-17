from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.trivia.absTriviaEvent import AbsTriviaEvent
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.specialTriviaStatus import SpecialTriviaStatus
from CynanBot.trivia.triviaEventType import TriviaEventType
from CynanBot.trivia.triviaScoreResult import TriviaScoreResult


class IncorrectAnswerTriviaEvent(AbsTriviaEvent):

    def __init__(
        self,
        triviaQuestion: AbsTriviaQuestion,
        specialTriviaStatus: Optional[SpecialTriviaStatus],
        actionId: str,
        answer: Optional[str],
        emote: str,
        eventId: str,
        gameId: str,
        twitchChannel: str,
        userId: str,
        userName: str,
        triviaScoreResult: TriviaScoreResult
    ):
        super().__init__(
            actionId = actionId,
            eventId = eventId
        )

        if not isinstance(triviaQuestion, AbsTriviaQuestion):
            raise ValueError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')
        elif specialTriviaStatus is not None and not isinstance(specialTriviaStatus, SpecialTriviaStatus):
            raise ValueError(f'specialTriviaStatus argument is malformed: \"{specialTriviaStatus}\"')
        elif answer is not None and not isinstance(answer, str):
            raise ValueError(f'answer argument is malformed: \"{answer}\"')
        elif not utils.isValidStr(emote):
            raise ValueError(f'emote argument is malformed: \"{emote}\"')
        elif not utils.isValidStr(gameId):
            raise ValueError(f'gameId argument is malformed: \"{gameId}\"')
        elif not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')
        elif not isinstance(triviaScoreResult, TriviaScoreResult):
            raise ValueError(f'triviaScoreResult argument is malformed: \"{triviaScoreResult}\"')

        self.__triviaQuestion: AbsTriviaQuestion = triviaQuestion
        self.__specialTriviaStatus: Optional[SpecialTriviaStatus] = specialTriviaStatus
        self.__answer: Optional[str] = answer
        self.__emote: str = emote
        self.__gameId: str = gameId
        self.__twitchChannel: str = twitchChannel
        self.__userId: str = userId
        self.__userName: str = userName
        self.__triviaScoreResult: TriviaScoreResult = triviaScoreResult

    def getAnswer(self) -> Optional[str]:
        return self.__answer

    def getEmote(self) -> str:
        return self.__emote

    def getGameId(self) -> str:
        return self.__gameId

    def getSpecialTriviaStatus(self) -> Optional[SpecialTriviaStatus]:
        return self.__specialTriviaStatus

    def getTriviaEventType(self) -> TriviaEventType:
        return TriviaEventType.INCORRECT_ANSWER

    def getTriviaQuestion(self) -> AbsTriviaQuestion:
        return self.__triviaQuestion

    def getTriviaScoreResult(self) -> TriviaScoreResult:
        return self.__triviaScoreResult

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName

    def isShiny(self) -> bool:
        return self.__specialTriviaStatus is SpecialTriviaStatus.SHINY

    def isToxic(self) -> bool:
        return self.__specialTriviaStatus is SpecialTriviaStatus.TOXIC
