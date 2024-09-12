from datetime import datetime

from ...misc import utils as utils


class TtsTempFile:

    def __init__(
        self,
        creationDateTime: datetime,
        fileName: str
    ):
        if not isinstance(creationDateTime, datetime):
            raise TypeError(f'creationDateTime argument is malformed: \"{creationDateTime}\"')
        elif not utils.isValidStr(fileName):
            raise TypeError(f'fileName argument is malformed: \"{fileName}\"')

        self.__creationDateTime: datetime = creationDateTime
        self.__fileName: str = fileName

        self.__deletionAttempts: int = 0

    @property
    def creationDateTime(self) -> datetime:
        return self.__creationDateTime

    @property
    def deletionAttempts(self) -> int:
        return self.__deletionAttempts

    @property
    def fileName(self) -> str:
        return self.__fileName

    def incrementDeletionAttempts(self):
        self.__deletionAttempts = self.__deletionAttempts + 1
