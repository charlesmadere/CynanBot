import CynanBot.misc.utils as utils
from CynanBot.trivia.actions.absTriviaAction import AbsTriviaAction
from CynanBot.trivia.actions.triviaActionType import TriviaActionType


class ClearSuperTriviaQueueTriviaAction(AbsTriviaAction):

    def __init__(
        self,
        actionId: str,
        twitchChannel: str,
        twitchChannelId: str
    ):
        super().__init__(actionId = actionId)

        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        self.__twitchChannel: str = twitchChannel
        self.__twitchChannelId: str = twitchChannelId

    @property
    def triviaActionType(self) -> TriviaActionType:
        return TriviaActionType.CLEAR_SUPER_TRIVIA_QUEUE

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def getTwitchChannelId(self) -> str:
        return self.__twitchChannelId
