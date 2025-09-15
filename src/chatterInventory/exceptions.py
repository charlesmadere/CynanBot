from typing import Final

from .models.useChatterItemAction import UseChatterItemAction


class CassetteTapeFeatureIsDisabledException(Exception):

    def __init__(self):
        super().__init__()


class CassetteTapeMessageHasNoTargetException(Exception):

    def __init__(
        self,
        cleanedMessage: str,
        originatingAction: UseChatterItemAction,
    ):
        super().__init__(cleanedMessage, originatingAction)

        self.__cleanedMessage: Final[str] = cleanedMessage
        self.__originatingAction: Final[UseChatterItemAction] = originatingAction

    @property
    def cleanedMessage(self) -> str:
        return self.__cleanedMessage

    @property
    def originatingAction(self) -> UseChatterItemAction:
        return self.__originatingAction


class CassetteTapeTargetIsNotFollowingException(Exception):

    def __init__(
        self,
        targetUserId: str,
        targetUserName: str,
        originatingAction: UseChatterItemAction,
    ):
        super().__init__(targetUserId, targetUserName, originatingAction)

        self.__targetUserId: Final[str] = targetUserId
        self.__targetUserName: Final[str] = targetUserName
        self.__originatingAction: Final[UseChatterItemAction] = originatingAction

    @property
    def targetUserId(self) -> str:
        return self.__targetUserId

    @property
    def targetUserName(self) -> str:
        return self.__targetUserName

    @property
    def originatingAction(self) -> UseChatterItemAction:
        return self.__originatingAction


class ChatterInventoryIsDisabledException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class UnknownChatterItemTypeException(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class UserTwitchAccessTokenIsMissing(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class VoicemailMessageIsEmptyException(Exception):

    def __init__(
        self,
        message: str | None,
        originatingAction: UseChatterItemAction,
    ):
        super().__init__(message, originatingAction)

        self.__message: Final[str | None] = message
        self.__originatingAction: Final[UseChatterItemAction] = originatingAction

    @property
    def message(self) -> str | None:
        return self.__message

    @property
    def originatingAction(self) -> UseChatterItemAction:
        return self.__originatingAction


class VoicemailTargetInboxIsFullException(Exception):

    def __init__(
        self,
        targetUserId: str,
        targetUserName: str,
    ):
        super().__init__(targetUserId, targetUserName)

        self.__targetUserId: Final[str] = targetUserId
        self.__targetUserName: Final[str] = targetUserName

    @property
    def targetUserId(self) -> str:
        return self.__targetUserId

    @property
    def targetUserName(self) -> str:
        return self.__targetUserName


class VoicemailTargetIsOriginatingUserException(Exception):

    def __init__(self):
        super().__init__()


class VoicemailTargetIsStreamerException(Exception):

    def __init__(self):
        super().__init__()
