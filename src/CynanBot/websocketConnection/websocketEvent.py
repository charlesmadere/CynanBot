from datetime import datetime, timezone
from typing import Any, Dict

import CynanBot.misc.utils as utils


class WebsocketEvent():

    def __init__(self, eventData: Dict[str, Any]):
        if not utils.hasItems(eventData):
            raise ValueError(f'eventData argument is malformed: \"{eventData}\"')

        self.__eventTime: datetime = datetime.now(timezone.utc)
        self.__eventData: Dict[str, Any] = eventData

    def getEventData(self) -> Dict[str, Any]:
        return self.__eventData

    def getEventTime(self) -> datetime:
        return self.__eventTime
