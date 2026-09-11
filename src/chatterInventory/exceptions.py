from typing import Final

from .models.useChatterItemAction import UseChatterItemAction
from ..twitch.localModels.twitchUserInterface import TwitchUserInterface


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
        targetUserData: TwitchUserInterface,
        originatingAction: UseChatterItemAction,
    ):
        super().__init__(targetUserData, originatingAction)

        self.__targetUserData: Final[TwitchUserInterface] = targetUserData
        self.__originatingAction: Final[UseChatterItemAction] = originatingAction

    @property
    def targetUserData(self) -> TwitchUserInterface:
        return self.__targetUserData

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
        targetUserData: TwitchUserInterface,
    ):
        super().__init__(targetUserData)

        self.__targetUserData: Final[TwitchUserInterface] = targetUserData

    @property
    def targetUserData(self) -> TwitchUserInterface:
        return self.__targetUserData


class VoicemailTargetIsOriginatingUserException(Exception):

    def __init__(self):
        super().__init__()


class VoicemailTargetIsStreamerException(Exception):

    def __init__(self):
        super().__init__()
