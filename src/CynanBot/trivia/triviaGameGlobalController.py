import misc.utils as utils


class TriviaGameGlobalController():

    def __init__(self, userId: str, userName: str):
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        self.__userId: str = userId
        self.__userName: str = userName

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName

    def __str__(self) -> str:
        return f'userId=\"{self.__userId}\", userName=\"{self.__userName}\"'
