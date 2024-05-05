from datetime import datetime, timezone
from typing import Any

import CynanBot.misc.utils as utils


class WebsocketEvent():

    def __init__(
        self,
        eventData: dict[str, Any],
        timeZone: timezone = timezone.utc
    ):
        if not utils.hasItems(eventData):
            raise ValueError(f'eventData argument is malformed: \"{eventData}\"')
        elif not isinstance(timeZone, timezone):
            raise ValueError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__eventTime: datetime = datetime.now(timeZone)
        self.__eventData: dict[str, Any] = eventData

    def getEventData(self) -> dict[str, Any]:
        return self.__eventData

    def getEventTime(self) -> datetime:
        return self.__eventTime

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'eventData': self.__eventData,
            'eventTime': self.__eventTime
        }
