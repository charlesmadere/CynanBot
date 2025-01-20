from .absChatSoundAlert import AbsChatSoundAlert
from .chatSoundAlertQualifier import ChatSoundAlertQualifer
from .chatSoundAlertType import ChatSoundAlertType
from ...misc import utils as utils


class FilePathChatSoundAlert(AbsChatSoundAlert):

    def __init__(
        self,
        qualifier: ChatSoundAlertQualifer,
        cooldownSeconds: int | None,
        volume: int | None,
        filePath: str,
        message: str
    ):
        super().__init__(
            qualifier = qualifier,
            cooldownSeconds = cooldownSeconds,
            volume = volume,
            message = message
        )

        if not utils.isValidStr(filePath):
            raise TypeError(f'filePath argument is malformed: \"{filePath}\"')

        self.__filePath: str = filePath

    @property
    def alertType(self) -> ChatSoundAlertType:
        return ChatSoundAlertType.FILE_PATH

    @property
    def filePath(self) -> str:
        return self.__filePath
