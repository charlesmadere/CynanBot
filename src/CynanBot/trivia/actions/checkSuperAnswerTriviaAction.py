from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.trivia.actions.absTriviaAction import AbsTriviaAction
from CynanBot.trivia.actions.triviaActionType import TriviaActionType


class CheckSuperAnswerTriviaAction(AbsTriviaAction):

    def __init__(
        self,
        actionId: str,
        answer: Optional[str],
        twitchChannel: str,
        userId: str,
        userName: str
    ):
        super().__init__(actionId = actionId)

        if answer is not None and not isinstance(answer, str):
            raise ValueError(f'answer argument is malformed: \"{answer}\"')
        elif not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        self.__answer: Optional[str] = answer
        self.__twitchChannel: str = twitchChannel
        self.__userId: str = userId
        self.__userName: str = userName

    def getAnswer(self) -> Optional[str]:
        return self.__answer

    def getTriviaActionType(self) -> TriviaActionType:
        return TriviaActionType.CHECK_SUPER_ANSWER

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName
