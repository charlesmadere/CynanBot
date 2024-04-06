import CynanBot.misc.utils as utils
from CynanBot.trivia.events.absTriviaEvent import AbsTriviaEvent
from CynanBot.trivia.events.triviaEventType import TriviaEventType


class SuperGameNotReadyCheckAnswerTriviaEvent(AbsTriviaEvent):

    def __init__(
        self,
        actionId: str,
        answer: str | None,
        eventId: str,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str,
        userName: str
    ):
        super().__init__(
            actionId = actionId,
            eventId = eventId
        )

        if answer is not None and not isinstance(answer, str):
            raise TypeError(f'answer argument is malformed: \"{answer}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        self.__answer: str | None = answer
        self.__twitchChannel: str = twitchChannel
        self.__twitchChannelId: str = twitchChannelId
        self.__userId: str = userId
        self.__userName: str = userName

    def getAnswer(self) -> str | None:
        return self.__answer

    def getTriviaEventType(self) -> TriviaEventType:
        return TriviaEventType.SUPER_GAME_NOT_READY

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def getTwitchChannelId(self) -> str:
        return self.__twitchChannelId

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName
