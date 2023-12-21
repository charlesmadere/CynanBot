import CynanBot.misc.utils as utils
from CynanBot.trivia.events.absTriviaEvent import AbsTriviaEvent
from CynanBot.trivia.events.triviaEventType import TriviaEventType


class SuperGameAlreadyInProgressTriviaEvent(AbsTriviaEvent):

    def __init__(
        self,
        actionId: str,
        eventId: str,
        gameId: str,
        twitchChannel: str
    ):
        super().__init__(
            actionId = actionId,
            eventId = eventId
        )

        if not utils.isValidStr(gameId):
            raise ValueError(f'gameId argument is malformed: \"{gameId}\"')
        elif not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        self.__gameId: str = gameId
        self.__twitchChannel: str = twitchChannel

    def getGameId(self) -> str:
        return self.__gameId

    def getTriviaEventType(self) -> TriviaEventType:
        return TriviaEventType.SUPER_GAME_ALREADY_IN_PROGRESS

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel
