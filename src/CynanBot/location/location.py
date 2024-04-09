from datetime import tzinfo
from typing import Any

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
            raise TypeError(f'latitude argument is malformed: \"{latitude}\"')
        elif not utils.isValidNum(longitude):
            raise TypeError(f'longitude argument is malformed: \"{longitude}\"')
        elif not utils.isValidStr(locationId):
            raise TypeError(f'locationId argument is malformed: \"{locationId}\"')
        elif not utils.isValidStr(name):
            raise TypeError(f'name argument is malformed: \"{name}\"')
        elif not isinstance(timeZone, tzinfo):
            raise TypeError(f'timeZone argument is malformed: \"{timeZone}\"')

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

    def toDictionary(self) -> dict[str, Any]:
        return {
            'latitude': self.__latitude,
            'locationId': self.__locationId,
            'longitude': self.__longitude,
            'name': self.__name,
            'timeZone': self.__timeZone
        }
