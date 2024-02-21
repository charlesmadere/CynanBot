from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.location.location import Location
from CynanBot.location.locationsRepositoryInterface import \
    LocationsRepositoryInterface
from CynanBot.location.timeZoneRepositoryInterface import \
    TimeZoneRepositoryInterface
from CynanBot.storage.jsonReaderInterface import JsonReaderInterface
from CynanBot.timber.timberInterface import TimberInterface


class LocationsRepository(LocationsRepositoryInterface):

    def __init__(
        self,
        locationsJsonReader: JsonReaderInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface
    ):
        assert isinstance(locationsJsonReader, JsonReaderInterface), f"malformed {locationsJsonReader=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(timeZoneRepository, TimeZoneRepositoryInterface), f"malformed {timeZoneRepository=}"

        self.__locationsJsonReader: JsonReaderInterface = locationsJsonReader
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository

        self.__cache: Dict[str, Optional[Location]] = dict()

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('LocationsRepository', 'Caches cleared')

    async def getLocation(self, locationId: str) -> Location:
        if not utils.isValidStr(locationId):
            raise ValueError(f'locationId argument is malformed: \"{locationId}\"')

        locationId = locationId.lower()
        location = self.__cache.get(locationId, None)

        if location is not None:
            return location

        jsonContents = await self.__readAllJson()

        for jsonLocationId, jsonLocationContents in jsonContents.items():
            if jsonLocationId.lower() == locationId:
                timeZoneStr = utils.getStrFromDict(jsonLocationContents, 'timeZone')
                timeZone = self.__timeZoneRepository.getTimeZone(timeZoneStr)

                location = Location(
                    latitude = utils.getFloatFromDict(jsonLocationContents, 'lat'),
                    longitude = utils.getFloatFromDict(jsonLocationContents, 'lon'),
                    locationId = jsonLocationId,
                    name = utils.getStrFromDict(jsonLocationContents, 'name'),
                    timeZone = timeZone
                )

                self.__cache[jsonLocationId.lower()] = location
                return location

        raise RuntimeError(f'Unable to find location with ID \"{locationId}\" in locations file: {self.__locationsJsonReader}')

    async def __readAllJson(self) -> Dict[str, Dict[str, Any]]:
        jsonContents: Optional[Dict[str, Dict[str, Any]]] = await self.__locationsJsonReader.readJsonAsync()

        if jsonContents is None:
            raise IOError(f'Error reading from locations file: {self.__locationsJsonReader}')
        if len(jsonContents) == 0:
            raise ValueError(f'JSON contents of locations file {self.__locationsJsonReader} is empty')

        return jsonContents
