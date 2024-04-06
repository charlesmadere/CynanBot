import CynanBot.misc.utils as utils
from CynanBot.trivia.events.absTriviaEvent import AbsTriviaEvent
from CynanBot.trivia.events.triviaEventType import TriviaEventType


class FailedToFetchQuestionSuperTriviaEvent(AbsTriviaEvent):

    def __init__(
        self,
        actionId: str,
        eventId: str,
        twitchChannel: str,
        twitchChannelId: str
    ):
        super().__init__(
            actionId = actionId,
            eventId = eventId
        )

        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        self.__twitchChannel: str = twitchChannel
        self.__twitchChannelId: str = twitchChannelId

    def getTriviaEventType(self) -> TriviaEventType:
        return TriviaEventType.SUPER_GAME_FAILED_TO_FETCH_QUESTION

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def getTwitchChannelId(self) -> str:
        return self.__twitchChannelId
