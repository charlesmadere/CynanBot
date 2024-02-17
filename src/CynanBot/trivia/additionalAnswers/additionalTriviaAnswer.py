from typing import Any, Dict

import CynanBot.misc.utils as utils


class AdditionalTriviaAnswer():

    def __init__(self, additionalAnswer: str, userId: str, userName: str):
        if not utils.isValidStr(additionalAnswer):
            raise TypeError(f'additionalAnswer argument is malformed: \"{additionalAnswer}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')

        self.__additionalTriviaAnswer: str = additionalAnswer
        self.__userId: str = userId
        self.__userName: str = userName

    def getAdditionalAnswer(self) -> str:
        return self.__additionalTriviaAnswer

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'additionalAnswer': self.__additionalTriviaAnswer,
            'userId': self.__userId,
            'userName': self.__userName
        }
