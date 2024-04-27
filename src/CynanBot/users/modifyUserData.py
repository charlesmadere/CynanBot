from dataclasses import dataclass

from CynanBot.users.modifyUserActionType import ModifyUserActionType


@dataclass(frozen = True)
class ModifyUserData():
    actionType: ModifyUserActionType
    userId: str
    userName: str
