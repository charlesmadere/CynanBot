from datetime import datetime

import CynanBot.misc.utils as utils


class TtsTempFile():

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

    def getCreationDateTime(self) -> datetime:
        return self.__creationDateTime

    def getFileName(self) -> str:
        return self.__fileName
