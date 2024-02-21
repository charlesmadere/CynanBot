import CynanBot.misc.utils as utils
from CynanBot.users.modifyUserActionType import ModifyUserActionType


class ModifyUserData():

    def __init__(
        self,
        actionType: ModifyUserActionType,
        userId: str,
        userName: str
    ):
        assert isinstance(actionType, ModifyUserActionType), f"malformed {actionType=}"
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        if not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        self.__actionType: ModifyUserActionType = actionType
        self.__userId: str = userId
        self.__userName: str = userName

    def getActionType(self) -> ModifyUserActionType:
        return self.__actionType

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName

    def toStr(self) -> str:
        return f'(actionType=\"{self.__actionType}\") (userId=\"{self.__userId}\") (userName=\"{self.__userName}\")'
