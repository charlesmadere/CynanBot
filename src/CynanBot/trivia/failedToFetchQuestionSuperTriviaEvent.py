import misc.utils as utils
from trivia.absTriviaEvent import AbsTriviaEvent
from trivia.triviaEventType import TriviaEventType


class FailedToFetchQuestionSuperTriviaEvent(AbsTriviaEvent):

    def __init__(
        self,
        actionId: str,
        twitchChannel: str
    ):
        super().__init__(
            actionId = actionId,
            triviaEventType = TriviaEventType.SUPER_GAME_FAILED_TO_FETCH_QUESTION
        )

        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        self.__twitchChannel: str = twitchChannel

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel
