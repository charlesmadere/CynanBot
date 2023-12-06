from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.trivia.absTriviaEvent import AbsTriviaEvent
from CynanBot.trivia.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.triviaEventType import TriviaEventType


class WrongUserCheckAnswerTriviaEvent(AbsTriviaEvent):

    def __init__(
        self,
        triviaQuestion: AbsTriviaQuestion,
        actionId: str,
        answer: Optional[str],
        emote: str,
        eventId: str,
        gameId: str,
        twitchChannel: str,
        userId: str,
        userName: str
    ):
        super().__init__(
            actionId = actionId,
            eventId = eventId
        )

        if not isinstance(triviaQuestion, AbsTriviaQuestion):
            raise ValueError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')
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

        self.__triviaQuestion: AbsTriviaQuestion = triviaQuestion
        self.__answer: Optional[str] = answer
        self.__emote: str = emote
        self.__gameId: str = gameId
        self.__twitchChannel: str = twitchChannel
        self.__userId: str = userId
        self.__userName: str = userName

    def getAnswer(self) -> Optional[str]:
        return self.__answer

    def getEmote(self) -> str:
        return self.__emote

    def getGameId(self) -> str:
        return self.__gameId

    def getTriviaEventType(self) -> TriviaEventType:
        return TriviaEventType.WRONG_USER

    def getTriviaQuestion(self) -> AbsTriviaQuestion:
        return self.__triviaQuestion

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName
