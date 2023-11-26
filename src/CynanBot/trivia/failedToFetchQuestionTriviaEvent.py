import CynanBot.misc.utils as utils
from CynanBot.trivia.absTriviaEvent import AbsTriviaEvent
from CynanBot.trivia.triviaEventType import TriviaEventType


class FailedToFetchQuestionTriviaEvent(AbsTriviaEvent):

    def __init__(
        self,
        actionId: str,
        twitchChannel: str,
        userId: str,
        userName: str
    ):
        super().__init__(
            actionId = actionId,
            triviaEventType = TriviaEventType.GAME_FAILED_TO_FETCH_QUESTION
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

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName
