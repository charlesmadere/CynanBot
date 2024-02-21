from datetime import tzinfo
from typing import Any, Dict

import CynanBot.misc.utils as utils


class Location():

    def __init__(
        self,
        latitude: float,
        longitude: float,
        locationId: str,
        name: str,
        timeZone: tzinfo
    ):
        if not utils.isValidNum(latitude):
            raise ValueError(f'latitude argument is malformed: \"{latitude}\"')
        if not utils.isValidNum(longitude):
            raise ValueError(f'longitude argument is malformed: \"{longitude}\"')
        if not utils.isValidStr(locationId):
            raise ValueError(f'locationId argument is malformed: \"{locationId}\"')
        if not utils.isValidStr(name):
            raise ValueError(f'name argument is malformed: \"{name}\"')
        assert isinstance(timeZone, tzinfo), f"malformed {timeZone=}"

        self.__latitude: float = latitude
        self.__longitude: float = longitude
        self.__locationId: str = locationId
        self.__name: str = name
        self.__timeZone: tzinfo = timeZone

    def getLatitude(self) -> float:
        return self.__latitude

    def getLocationId(self) -> str:
        return self.__locationId

    def getLongitude(self) -> float:
        return self.__longitude

    def getName(self) -> str:
        return self.__name

    def getTimeZone(self) -> tzinfo:
        return self.__timeZone

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'latitude': self.__latitude,
            'locationId': self.__locationId,
            'longitude': self.__longitude,
            'name': self.__name,
            'timeZone': self.__timeZone
        }
