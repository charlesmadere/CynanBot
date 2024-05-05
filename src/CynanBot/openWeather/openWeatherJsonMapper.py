from datetime import datetime
from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.location.timeZoneRepositoryInterface import \
    TimeZoneRepositoryInterface
from CynanBot.openWeather.openWeatherAirPollutionIndex import \
    OpenWeatherAirPollutionIndex
from CynanBot.openWeather.openWeatherAirPollutionReport import \
    OpenWeatherAirPollutionReport
from CynanBot.openWeather.openWeatherJsonMapperInterface import \
    OpenWeatherJsonMapperInterface
from CynanBot.openWeather.openWeatherMomentReport import \
    OpenWeatherMomentReport
from CynanBot.openWeather.openWeatherReport import OpenWeatherReport
from CynanBot.timber.timberInterface import TimberInterface


class OpenWeatherJsonMapper(OpenWeatherJsonMapperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository

    async def parseAirPollutionIndex(
        self,
        index: int | None
    ) -> OpenWeatherAirPollutionIndex | None:
        if not utils.isValidInt(index):
            return None

        if index <= 1:
            return OpenWeatherAirPollutionIndex.GOOD
        elif index <= 2:
            return OpenWeatherAirPollutionIndex.FAIR
        elif index <= 3:
            return OpenWeatherAirPollutionIndex.MODERATE
        elif index <= 4:
            return OpenWeatherAirPollutionIndex.POOR
        else:
            return OpenWeatherAirPollutionIndex.VERY_POOR

    async def parseAirPollutionReport(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenWeatherAirPollutionReport | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        coordJson: dict[str, Any] | None = jsonContents.get('coord')
        if not isinstance(coordJson, dict) or len(coordJson) == 0:
            self.__timber.log('OpenWeatherJsonMapper', f'Encountered missing/invalid \"coord\" field in JSON data: ({jsonContents=})')
            return None

        latitude = utils.getFloatFromDict(coordJson, 'lat')
        longitude = utils.getFloatFromDict(coordJson, 'lon')

        listArray: list[dict[str, Any] | None] | None = jsonContents.get('list')
        if not isinstance(listArray, list) or len(listArray) == 0:
            self.__timber.log('OpenWeatherJsonMapper', f'Encountered missing/invalid \"list\" field in JSON data: ({jsonContents=})')
            return None

        listEntryJson = listArray[0]
        if not isinstance(listEntryJson, dict) or len(listEntryJson) == 0:
            self.__timber.log('OpenWeatherJsonMapper', f'Encountered missing/invalid entry in \"list\" JSON data: ({jsonContents=})')
            return None

        dateTime = datetime.fromtimestamp(utils.getIntFromDict(listEntryJson, 'dt'))

        mainJson: dict[str, Any] | None = listEntryJson.get('main')
        if not isinstance(mainJson, dict) or len(mainJson) == 0:
            self.__timber.log('OpenWeatherJsonMapper', f'Encountered missing/invalid \"main\" field in JSON data: ({jsonContents=})')
            return None

        airPollutionIndex = await self.parseAirPollutionIndex(mainJson.get('aqi'))
        if airPollutionIndex is None:
            self.__timber.log('OpenWeatherJsonMapper', f'Encountered missing/invalid OpenWeatherAirPollutionIndex in \"main\" JSON data: ({jsonContents=})')
            return None

        return OpenWeatherAirPollutionReport(
            dateTime = dateTime,
            latitude = latitude,
            longitude = longitude,
            airPollutionIndex = airPollutionIndex
        )

    async def parseWeatherMomentReport(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenWeatherMomentReport | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        dateTime = datetime.fromtimestamp(utils.getIntFromDict(jsonContents, 'dt'))
        feelsLikeTemperature = utils.getFloatFromDict(jsonContents, 'feels_like')
        temperature = utils.getFloatFromDict(jsonContents, 'temp')
        uvIndex = utils.getFloatFromDict(jsonContents, 'uvi')
        windSpeed = utils.getFloatFromDict(jsonContents, 'wind_speed')
        humidity = utils.getIntFromDict(jsonContents, 'humidity')
        pressure = utils.getIntFromDict(jsonContents, 'pressure')
        sunrise = utils.getIntFromDict(jsonContents, 'sunrise')
        sunset = utils.getIntFromDict(jsonContents, 'sunset')

        return OpenWeatherMomentReport(
            dateTime = dateTime,
            feelsLikeTemperature = feelsLikeTemperature,
            temperature = temperature,
            uvIndex = uvIndex,
            windSpeed = windSpeed,
            humidity = humidity,
            pressure = pressure,
            sunrise = sunrise,
            sunset = sunset
        )

    async def parseWeatherReport(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenWeatherReport | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        latitude = utils.getFloatFromDict(jsonContents, 'lat')
        longitude = utils.getFloatFromDict(jsonContents, 'lon')

        current = await self.parseWeatherMomentReport(jsonContents.get('current'))
        if current is None:
            self.__timber.log('OpenWeatherJsonMapper', f'Unable to parse value for \"current\" data: ({jsonContents=})')
            return None

        timeZoneStr = utils.getStrFromDict(jsonContents, 'timezone')
        timeZone = self.__timeZoneRepository.getTimeZone(timeZoneStr)

        return OpenWeatherReport(
            latitude = latitude,
            longitude = longitude,
            current = current,
            timeZone = timeZone
        )
