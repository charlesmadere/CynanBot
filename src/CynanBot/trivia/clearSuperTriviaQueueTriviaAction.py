import CynanBot.misc.utils as utils
from CynanBot.trivia.absTriviaAction import AbsTriviaAction
from CynanBot.trivia.triviaActionType import TriviaActionType


class ClearSuperTriviaQueueTriviaAction(AbsTriviaAction):

    def __init__(self, twitchChannel: str):
        super().__init__(triviaActionType = TriviaActionType.CLEAR_SUPER_TRIVIA_QUEUE)

        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        self.__twitchChannel: str = twitchChannel

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel
