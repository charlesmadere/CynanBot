import json
from location import Location
import os
from timeZoneRepository import TimeZoneRepository

class LocationsRepository():

    def __init__(
        self,
        timeZoneRepository: TimeZoneRepository,
        locationsFile: str = 'locationsRepository.json'
    ):
        if locationsFile == None or len(locationsFile) == 0 or locationsFile.isspace():
            raise ValueError(f'locationsFile argument is malformed: \"{locationsFile}\"')
        elif timeZoneRepository == None:
            raise ValueError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__locationsCache = dict()
        self.__locationsFile = locationsFile
        self.__timeZoneRepository = timeZoneRepository

    def getLocation(self, id_: str):
        if id_ == None or len(id_) == 0 or id_.isspace():
            raise ValueError(f'id_ argument is malformed: \"{id_}\"')

        if id_.lower() in self.__locationsCache:
            return self.__locationsCache[id_.lower()]

        if not os.path.exists(self.__locationsFile):
            raise FileNotFoundError(f'Locations file not found: \"{self.__locationsFile}\"')

        with open(self.__locationsFile, 'r') as file:
            jsonContents = json.load(file)

        if jsonContents == None:
            raise IOError(f'Error reading from locations file: \"{self.__locationsFile}\"')

        for locationId in jsonContents:
            if id_.lower() == locationId.lower():
                timeZoneStr = jsonContents[locationId]['timeZone']
                timeZone = self.__timeZoneRepository.getTimeZone(timeZoneStr)

                location = Location(
                    lat = jsonContents[locationId]['lat'],
                    lon = jsonContents[locationId]['lon'],
                    id_ = locationId,
                    name = jsonContents[locationId]['name'],
                    timeZone = timeZone
                )

                self.__locationsCache[id_.lower()] = location
                return location

        raise RuntimeError(f'Unable to find location with ID \"{id_}\" in locations file: \"{self.__locationsFile}\"')
