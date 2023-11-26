import misc.utils as utils


class AdditionalTriviaAnswer():

    def __init__(self, additionalAnswer: str, userId: str, userName: str):
        if not utils.isValidStr(additionalAnswer):
            raise ValueError(f'additionalAnswer argument is malformed: \"{additionalAnswer}\"')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        self.__additionalTriviaAnswer: str = additionalAnswer
        self.__userId: str = userId
        self.__userName: str = userName

    def getAdditionalAnswer(self) -> str:
        return self.__additionalTriviaAnswer

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName

    def __str__(self) -> str:
        return f'additionalAnswer=\"{self.__additionalTriviaAnswer}\", userId=\"{self.__userId}\", userName=\"{self.__userName}\"'
