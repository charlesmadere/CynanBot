import CynanBot.misc.utils as utils
from CynanBot.trivia.events.absTriviaEvent import AbsTriviaEvent
from CynanBot.trivia.events.triviaEventType import TriviaEventType


class FailedToFetchQuestionTriviaEvent(AbsTriviaEvent):

    def __init__(
        self,
        actionId: str,
        eventId: str,
        twitchChannel: str,
        userId: str,
        userName: str
    ):
        super().__init__(
            actionId = actionId,
            eventId = eventId
        )

        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        self.__twitchChannel: str = twitchChannel
        self.__userId: str = userId
        self.__userName: str = userName

    def getTriviaEventType(self) -> TriviaEventType:
        return TriviaEventType.GAME_FAILED_TO_FETCH_QUESTION

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName
