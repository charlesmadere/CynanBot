import CynanBot.misc.utils as utils
from CynanBot.trivia.actions.absTriviaAction import AbsTriviaAction
from CynanBot.trivia.actions.triviaActionType import TriviaActionType


class CheckSuperAnswerTriviaAction(AbsTriviaAction):

    def __init__(
        self,
        actionId: str,
        answer: str | None,
        twitchChannel: str,
        twitchChannelId: str,
        userId: str,
        userName: str
    ):
        super().__init__(actionId = actionId)

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

    def getTriviaActionType(self) -> TriviaActionType:
        return TriviaActionType.CHECK_SUPER_ANSWER

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def getTwitchChannelId(self) -> str:
        return self.__twitchChannelId

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName

    def requireAnswer(self) -> str:
        answer = self.__answer

        if not utils.isValidStr(answer):
            raise ValueError(f'no answer value is available: \"{answer}\"')

        return answer
