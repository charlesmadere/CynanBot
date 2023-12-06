import CynanBot.misc.utils as utils
from CynanBot.trivia.absTriviaEvent import AbsTriviaEvent
from CynanBot.trivia.triviaEventType import TriviaEventType


class FailedToFetchQuestionSuperTriviaEvent(AbsTriviaEvent):

    def __init__(
        self,
        actionId: str,
        eventId: str,
        twitchChannel: str
    ):
        super().__init__(
            actionId = actionId,
            eventId = eventId
        )

        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        self.__twitchChannel: str = twitchChannel

    def getTriviaEventType(self) -> TriviaEventType:
        return TriviaEventType.SUPER_GAME_FAILED_TO_FETCH_QUESTION

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel
