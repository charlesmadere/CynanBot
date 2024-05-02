from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from CynanBot.openWeather.openWeatherJsonMapperInterface import OpenWeatherJsonMapperInterface
from CynanBot.openWeather.openWeatherMomentReport import OpenWeatherMomentReport
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

    async def parseWeatherMomentReport(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenWeatherMomentReport | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        feelsLikeTemperature = utils.getFloatFromDict(jsonContents, 'feels_like')
        temperature = utils.getFloatFromDict(jsonContents, 'temp')
        uvIndex = utils.getFloatFromDict(jsonContents, 'uvi')
        windSpeed = utils.getFloatFromDict(jsonContents, 'wind_speed')
        humidity = utils.getIntFromDict(jsonContents, 'humidity')
        pressure = utils.getIntFromDict(jsonContents, 'pressure')
        sunrise = utils.getIntFromDict(jsonContents, 'sunrise')
        sunset = utils.getIntFromDict(jsonContents, 'sunset')

        return OpenWeatherMomentReport(
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
