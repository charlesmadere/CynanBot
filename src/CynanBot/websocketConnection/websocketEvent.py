from datetime import datetime, timezone
from typing import Any, Dict

import CynanBot.misc.utils as utils


class WebsocketEvent():

    def __init__(
        self,
        eventData: Dict[str, Any],
        timeZone: timezone = timezone.utc
    ):
        if not utils.hasItems(eventData):
            raise ValueError(f'eventData argument is malformed: \"{eventData}\"')
        assert isinstance(timeZone, timezone), f"malformed {timeZone=}"

        self.__eventTime: datetime = datetime.now(timeZone)
        self.__eventData: Dict[str, Any] = eventData

    def getEventData(self) -> Dict[str, Any]:
        return self.__eventData

    def getEventTime(self) -> datetime:
        return self.__eventTime

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'eventData': self.__eventData,
            'eventTime': self.__eventTime
        }
