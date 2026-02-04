from typing import Any

from .exceptions import NoSuchLocationException
from .location import Location
from .locationsRepositoryInterface import LocationsRepositoryInterface
from .timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..storage.jsonReaderInterface import JsonReaderInterface
from ..timber.timberInterface import TimberInterface


class LocationsRepository(LocationsRepositoryInterface):

    def __init__(
        self,
        locationsJsonReader: JsonReaderInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
    ):
        if not isinstance(locationsJsonReader, JsonReaderInterface):
            raise TypeError(f'locationsJsonReader argument is malformed: \"{locationsJsonReader}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__locationsJsonReader: JsonReaderInterface = locationsJsonReader
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository

        self.__cache: dict[str, Location | None] = dict()

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('LocationsRepository', 'Caches cleared')

    async def getLocation(self, locationId: str) -> Location:
        if not utils.isValidStr(locationId):
            raise TypeError(f'locationId argument is malformed: \"{locationId}\"')

        locationId = locationId.casefold()
        location = self.__cache.get(locationId, None)

        if location is not None:
            return location

        jsonContents = await self.__readAllJson()

        for jsonLocationId, jsonLocationContents in jsonContents.items():
            if jsonLocationId.casefold() == locationId:
                timeZoneStr = utils.getStrFromDict(jsonLocationContents, 'timeZone')
                timeZone = self.__timeZoneRepository.getTimeZone(timeZoneStr)

                location = Location(
                    latitude = utils.getFloatFromDict(jsonLocationContents, 'lat'),
                    longitude = utils.getFloatFromDict(jsonLocationContents, 'lon'),
                    locationId = jsonLocationId,
                    name = utils.getStrFromDict(jsonLocationContents, 'name'),
                    timeZone = timeZone,
                )

                self.__cache[jsonLocationId.casefold()] = location
                return location

        raise NoSuchLocationException(f'Unable to find location with ID \"{locationId}\" in locations file: {self.__locationsJsonReader}')

    async def __readAllJson(self) -> dict[str, dict[str, Any]]:
        jsonContents: dict[str, dict[str, Any]] | None = await self.__locationsJsonReader.readJsonAsync()

        if not isinstance(jsonContents, dict):
            raise IOError(f'Error reading from locations file: {self.__locationsJsonReader}')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of locations file {self.__locationsJsonReader} is empty')

        return jsonContents
