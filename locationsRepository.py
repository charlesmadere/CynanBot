import json
import math
from datetime import tzinfo
from os import path

from timeZoneRepository import TimeZoneRepository


class LocationsRepository():

    def __init__(
        self,
        timeZoneRepository: TimeZoneRepository,
        locationsFile: str = 'locationsRepository.json'
    ):
        if locationsFile is None or len(locationsFile) == 0 or locationsFile.isspace():
            raise ValueError(f'locationsFile argument is malformed: \"{locationsFile}\"')
        elif timeZoneRepository is None:
            raise ValueError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__locationsCache = dict()
        self.__locationsFile = locationsFile
        self.__timeZoneRepository = timeZoneRepository

    def getLocation(self, id_: str):
        if id_ is None or len(id_) == 0 or id_.isspace():
            raise ValueError(f'id_ argument is malformed: \"{id_}\"')

        if id_.lower() in self.__locationsCache:
            return self.__locationsCache[id_.lower()]

        if not path.exists(self.__locationsFile):
            raise FileNotFoundError(f'Locations file not found: \"{self.__locationsFile}\"')

        with open(self.__locationsFile, 'r') as file:
            jsonContents = json.load(file)

        if jsonContents is None:
            raise IOError(f'Error reading from locations file: \"{self.__locationsFile}\"')

        for locationId in jsonContents:
            if id_.lower() == locationId.lower():
                timeZoneStr = jsonContents[locationId]['timeZone']
                timeZone = self.__timeZoneRepository.getTimeZone(timeZoneStr)

                location = Location(
                    lat=jsonContents[locationId]['lat'],
                    lon=jsonContents[locationId]['lon'],
                    id_=locationId,
                    name=jsonContents[locationId]['name'],
                    timeZone=timeZone
                )

                self.__locationsCache[id_.lower()] = location
                return location

        raise RuntimeError(f'Unable to find location with ID \"{id_}\" in locations file: \"{self.__locationsFile}\"')


class Location():

    def __init__(self, lat: float, lon: float, id_: str, name: str, timeZone: tzinfo):
        if lat is None or not math.isfinite(lat):
            raise ValueError(f'lat argument is malformed: \"{lat}\"')
        elif lon is None or not math.isfinite(lon):
            raise ValueError(f'lon argument is malformed: \"{lon}\"')
        elif id_ is None or len(id_) == 0 or id_.isspace():
            raise ValueError(f'id_ argument is malformed: \"{id_}\"')
        elif name is None or len(name) == 0 or name.isspace():
            raise ValueError(f'name argument is malformed: \"{name}\"')
        elif timeZone is None:
            raise ValueError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__id_ = id_
        self.__latitude = lat
        self.__longitude = lon
        self.__name = name
        self.__timeZone = timeZone

    def getId(self):
        return self.__id_

    def getLatitude(self):
        return self.__latitude

    def getLongitude(self):
        return self.__longitude

    def getName(self):
        return self.__name

    def getTimeZone(self):
        return self.__timeZone
