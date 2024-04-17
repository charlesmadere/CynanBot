from datetime import datetime
from typing import Any


class MostRecentAnivMessage():

    def __init__(
        self,
        dateTime: datetime,
        message: str | None
    ):
        if not isinstance(dateTime, datetime):
            raise TypeError(f'dateTime argument is malformed: \"{dateTime}\"')
        elif message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        self.__dateTime: datetime = dateTime
        self.__message: str | None = message

    def getDateTime(self) -> datetime:
        return self.__dateTime

    def getMessage(self) -> str | None:
        return self.__message

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'dateTime': self.__dateTime,
            'message': self.__message
        }
