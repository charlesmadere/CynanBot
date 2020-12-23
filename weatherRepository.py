import json
import locale
import math
from datetime import timedelta
from typing import List

import requests

import utils
from authHelper import AuthHelper
from locationsRepository import Location
from timedDict import TimedDict


class WeatherRepository():

    def __init__(
        self,
        authHelper: AuthHelper,
        cacheTimeDelta=timedelta(hours=1, minutes=30)
    ):
        if authHelper is None:
            raise ValueError(f'authHelper argument is malformed: \"{authHelper}\"')
        elif cacheTimeDelta is None:
            raise ValueError(f'cacheTimeDelta argument is malformed: \"{cacheTimeDelta}\"')

        self.__authHelper = authHelper
        self.__cache = TimedDict(timeDelta=cacheTimeDelta)
        self.__conditionIcons = self.__createConditionIconsDict()

    def __chooseTomorrowFromForecast(self, jsonResponse: dict):
        currentSunrise = jsonResponse['current']['sunrise']
        currentSunset = jsonResponse['current']['sunset']

        for dayJson in jsonResponse['daily']:
            if dayJson['sunrise'] > currentSunrise and dayJson['sunset'] > currentSunset:
                return dayJson

        raise RuntimeError(f'Unable to find viable tomorrow data in JSON response: \"{jsonResponse}\"')

    def __createConditionIconsDict(self):
        # This dictionary is built from the Weather Condition Codes listed here:
        # https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2

        icons = dict()
        icons['200'] = '⛈️'
        icons['201'] = icons['200']
        icons['202'] = icons['200']
        icons['210'] = '🌩️'
        icons['211'] = icons['210']
        icons['212'] = icons['211']
        icons['221'] = icons['200']
        icons['230'] = icons['200']
        icons['231'] = icons['200']
        icons['232'] = icons['200']
        icons['300'] = '☔'
        icons['301'] = icons['300']
        icons['310'] = icons['300']
        icons['311'] = icons['300']
        icons['313'] = icons['300']
        icons['500'] = icons['300']
        icons['501'] = '🌧️'
        icons['502'] = icons['501']
        icons['503'] = icons['501']
        icons['504'] = icons['501']
        icons['520'] = icons['501']
        icons['521'] = icons['501']
        icons['522'] = icons['501']
        icons['531'] = icons['501']
        icons['600'] = '❄️'
        icons['601'] = icons['600']
        icons['602'] = '🌨️'
        icons['711'] = '🌫️'
        icons['721'] = icons['711']
        icons['731'] = icons['711']
        icons['741'] = icons['711']
        icons['762'] = '🌋'
        icons['771'] = '🌬'
        icons['781'] = '🌪️'
        icons['801'] = '☁️'
        icons['802'] = icons['801']
        icons['803'] = icons['801']
        icons['804'] = icons['801']

        return icons

    def __fetchAirQuality(self, location: Location):
        iqAirApiKey = self.__authHelper.getIqAirApiKey()
        if not utils.isValidStr(iqAirApiKey):
            print(f'iqAirApiKey is missing: \"{iqAirApiKey}\"')
            return None

        # Retrieve air quality from: https://api-docs.iqair.com/
        # Doing this requires an API key, which you can get here:
        # https://www.iqair.com/us/commercial/air-quality-monitors/airvisual-platform/api

        requestUrl = "https://api.airvisual.com/v2/nearest_city?key={}&lat={}&lon={}".format(
            iqAirApiKey, location.getLatitude(), location.getLongitude())

        rawResponse = requests.get(requestUrl)
        jsonResponse = rawResponse.json()

        if jsonResponse.get('status') != 'success':
            return None

        return jsonResponse['data']['current']['pollution']['aqius']

    def fetchWeather(self, location: Location):
        if location is None:
            raise ValueError(f'location argument is malformed: \"{location}\"')

        cacheValue = self.__cache[location.getId()]

        if cacheValue is not None:
            return cacheValue

        print(f'Refreshing weather for \"{location.getId()}\"...')

        # Retrieve weather report from https://openweathermap.org/api/one-call-api
        # Doing this requires an API key, which you can get here:
        # https://openweathermap.org/api

        oneWeatherApiKey = self.__authHelper.getOneWeatherApiKey()
        if not utils.isValidStr(oneWeatherApiKey):
            raise RuntimeError(f'oneWeatherApiKey is malformed: \"{oneWeatherApiKey}\"')

        requestUrl = "https://api.openweathermap.org/data/2.5/onecall?appid={}&lat={}&lon={}&exclude=minutely,hourly&units=metric".format(
            oneWeatherApiKey, location.getLatitude(), location.getLongitude())

        rawResponse = requests.get(requestUrl)
        jsonResponse = rawResponse.json()

        currentJson = jsonResponse['current']
        humidity = currentJson['humidity']
        pressure = currentJson['pressure']
        temperature = currentJson['temp']

        conditions = list()
        if 'weather' in currentJson and len(currentJson['weather']) >= 1:
            for conditionJson in currentJson['weather']:
                conditions.append(self.__prettifyCondition(conditionJson))

        alerts = list()
        if 'alerts' in jsonResponse and len(jsonResponse['alerts']) >= 1:
            for alertJson in jsonResponse['alerts']:
                event = alertJson.get('event')
                senderName = alertJson.get('sender_name')

                if event is not None and len(event) >= 1:
                    if senderName is None or len(senderName) == 0:
                        alerts.append(f'Alert: {event}.')
                    else:
                        alerts.append(f'Alert from {senderName}: {event}.')

        tomorrowsJson = self.__chooseTomorrowFromForecast(jsonResponse)
        tomorrowsHighTemperature = tomorrowsJson['temp']['max']
        tomorrowsLowTemperature = tomorrowsJson['temp']['min']

        tomorrowsConditions = list()
        if 'weather' in tomorrowsJson and len(tomorrowsJson['weather']) >= 1:
            for conditionJson in tomorrowsJson['weather']:
                tomorrowsConditions.append(conditionJson['description'])

        airQuality = self.__fetchAirQuality(location)
        weatherReport = None

        try:
            weatherReport = WeatherReport(
                airQuality=airQuality,
                humidity=humidity,
                pressure=pressure,
                temperature=temperature,
                tomorrowsHighTemperature=tomorrowsHighTemperature,
                tomorrowsLowTemperature=tomorrowsLowTemperature,
                alerts=alerts,
                conditions=conditions,
                tomorrowsConditions=tomorrowsConditions
            )
        except ValueError:
            print(f'Weather Report for \"{location.getId()}\" has a data error')

        if weatherReport is None:
            del self.__cache[location.getId()]
        else:
            self.__cache[location.getId()] = weatherReport

        return weatherReport

    def __prettifyCondition(self, conditionJson: dict):
        conditionIcon = ''
        if 'id' in conditionJson:
            id_ = str(conditionJson['id'])

            if id_ in self.__conditionIcons:
                icon = self.__conditionIcons[id_]
                conditionIcon = f'{icon} '

        conditionDescription = conditionJson['description']
        return f'{conditionIcon}{conditionDescription}'


class WeatherReport():

    def __init__(
        self,
        airQuality: int,
        humidity: float,
        pressure: float,
        temperature: float,
        tomorrowsHighTemperature: float,
        tomorrowsLowTemperature: float,
        alerts: List[str],
        conditions: List[str],
        tomorrowsConditions: List[str]
    ):
        if humidity is None or not math.isfinite(humidity):
            raise ValueError(f'humidity argument is malformed: \"{humidity}\"')
        elif pressure is None or not math.isfinite(pressure):
            raise ValueError(f'pressure argument is malformed: \"{pressure}\"')
        elif temperature is None or not math.isfinite(temperature):
            raise ValueError(f'temperature argument is malformed: \"{temperature}\"')
        elif tomorrowsHighTemperature is None or not math.isfinite(tomorrowsHighTemperature):
            raise ValueError(f'tomorrowsHighTemperature argument is malformed: \"{tomorrowsHighTemperature}\"')
        elif tomorrowsLowTemperature is None or not math.isfinite(tomorrowsLowTemperature):
            raise ValueError(f'tomorrowsLowTemperature argument is malformed: \"{tomorrowsLowTemperature}\"')

        self.__airQuality = airQuality
        self.__humidity = int(round(humidity))
        self.__pressure = int(round(pressure))
        self.__temperature = temperature
        self.__tomorrowsHighTemperature = tomorrowsHighTemperature
        self.__tomorrowsLowTemperature = tomorrowsLowTemperature
        self.__alerts = alerts
        self.__conditions = conditions
        self.__tomorrowsConditions = tomorrowsConditions

    def __cToF(self, celsius: float):
        return (celsius * (9 / 5)) + 32

    def getAirQuality(self):
        return self.__airQuality

    def getAirQualityStr(self):
        return locale.format_string("%d", self.getAirQuality(), grouping=True)

    def getAlerts(self):
        return self.__alerts

    def getConditions(self):
        return self.__conditions

    def getHumidity(self):
        return self.__humidity

    def getPressure(self):
        return self.__pressure

    def getPressureStr(self):
        return locale.format_string("%d", self.getPressure(), grouping=True)

    def getTemperature(self):
        return int(round(self.__temperature))

    def getTemperatureStr(self):
        return locale.format_string("%d", self.getTemperature(), grouping=True)

    def getTemperatureImperial(self):
        return int(round(self.__cToF(self.__temperature)))

    def getTemperatureImperialStr(self):
        return locale.format_string("%d", self.getTemperatureImperial(), grouping=True)

    def getTomorrowsConditions(self):
        return self.__tomorrowsConditions

    def getTomorrowsLowTemperature(self):
        return int(round(self.__tomorrowsLowTemperature))

    def getTomorrowsLowTemperatureStr(self):
        return locale.format_string("%d", self.getTomorrowsLowTemperature(), grouping=True)

    def getTomorrowsLowTemperatureImperial(self):
        return int(round(self.__cToF(self.__tomorrowsLowTemperature)))

    def getTomorrowsLowTemperatureImperialStr(self):
        return locale.format_string("%d", self.getTomorrowsLowTemperatureImperial(), grouping=True)

    def getTomorrowsHighTemperature(self):
        return int(round(self.__tomorrowsHighTemperature))

    def getTomorrowsHighTemperatureStr(self):
        return locale.format_string("%d", self.getTomorrowsHighTemperature(), grouping=True)

    def getTomorrowsHighTemperatureImperial(self):
        return int(round(self.__cToF(self.__tomorrowsHighTemperature)))

    def getTomorrowsHighTemperatureImperialStr(self):
        return locale.format_string("%d", self.getTomorrowsHighTemperatureImperial(), grouping=True)

    def hasAirQuality(self):
        return self.__airQuality is not None

    def hasAlerts(self):
        return self.__alerts is not None and len(self.__alerts) >= 1

    def hasConditions(self):
        return self.__conditions is not None and len(self.__conditions) >= 1

    def hasTomorrowsConditions(self):
        return self.__tomorrowsConditions is not None and len(self.__tomorrowsConditions) >= 1
