from datetime import tzinfo

import misc.utils as utils


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
        elif not utils.isValidNum(longitude):
            raise ValueError(f'longitude argument is malformed: \"{longitude}\"')
        elif not utils.isValidStr(locationId):
            raise ValueError(f'id_ argument is malformed: \"{locationId}\"')
        elif not utils.isValidStr(name):
            raise ValueError(f'name argument is malformed: \"{name}\"')
        elif not isinstance(timeZone, tzinfo):
            raise ValueError(f'timeZone argument is malformed: \"{timeZone}\"')

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
