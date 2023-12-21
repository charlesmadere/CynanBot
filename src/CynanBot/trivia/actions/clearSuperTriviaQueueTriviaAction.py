import CynanBot.misc.utils as utils
from CynanBot.trivia.actions.absTriviaAction import AbsTriviaAction
from CynanBot.trivia.actions.triviaActionType import TriviaActionType


class ClearSuperTriviaQueueTriviaAction(AbsTriviaAction):

    def __init__(
        self,
        actionId: str,
        twitchChannel: str
    ):
        super().__init__(actionId = actionId)

        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        self.__twitchChannel: str = twitchChannel

    def getTriviaActionType(self) -> TriviaActionType:
        return TriviaActionType.CLEAR_SUPER_TRIVIA_QUEUE

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel
