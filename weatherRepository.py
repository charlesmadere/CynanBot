import json
from datetime import timedelta

import requests

from authHelper import AuthHelper
from location import Location
from timedDict import TimedDict
from weatherReport import WeatherReport


class WeatherRepository():

    def __init__(
        self,
        authHelper: AuthHelper,
        cacheTimeDelta = timedelta(hours = 1, minutes = 30)
    ):
        if authHelper == None:
            raise ValueError(f'authHelper argument is malformed: \"{authHelper}\"')
        elif cacheTimeDelta == None:
            raise ValueError(f'cacheTimeDelta argument is malformed: \"{cacheTimeDelta}\"')

        self.__authHelper = authHelper
        self.__cache = TimedDict(timeDelta = cacheTimeDelta)
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
        icons['200'] = '⛈'
        icons['201'] = icons['200']
        icons['202'] = icons['200']
        icons['210'] = '🌩'
        icons['211'] = icons['210']
        icons['212'] = icons['210']
        icons['221'] = icons['200']
        icons['230'] = icons['200']
        icons['231'] = icons['200']
        icons['232'] = icons['200']
        icons['300'] = '☔️'
        icons['301'] = icons['300']
        icons['302'] = icons['300']
        icons['500'] = icons['300']
        icons['501'] = '🌧'
        icons['502'] = icons['501']
        icons['503'] = icons['501']
        icons['504'] = icons['501']
        icons['600'] = '❅'
        icons['601'] = icons['600']
        icons['602'] = icons['600']
        icons['711'] = '🌫'
        icons['721'] = icons['711']
        icons['731'] = icons['711']
        icons['741'] = icons['711']
        icons['762'] = '🌋'
        icons['771'] = '🌬'
        icons['781'] = '🌪'
        icons['802'] = '☁️'
        icons['803'] = icons['802']
        icons['804'] = icons['802']

        return icons

    def __fetchAirQuality(self, location: Location):
        iqAirApiKey = self.__authHelper.getIqAirApiKey()
        if iqAirApiKey == None or len(iqAirApiKey) == 0 or iqAirApiKey.isspace():
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
        if location == None:
            raise ValueError(f'location argument is malformed: \"{location}\"')

        cacheValue = self.__cache[location.getId()]

        if cacheValue != None:
            return cacheValue

        print(f'Refreshing weather for \"{location.getId()}\"...')

        # Retrieve weather report from https://openweathermap.org/api/one-call-api
        # Doing this requires an API key, which you can get here:
        # https://openweathermap.org/api

        oneWeatherApiKey = self.__authHelper.getOneWeatherApiKey()
        if oneWeatherApiKey == None or len(oneWeatherApiKey) == 0 or oneWeatherApiKey.isspace():
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

                if event != None and len(event) >= 1:
                    if senderName == None or len(senderName) == 0:
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
                airQuality = airQuality,
                humidity = humidity,
                pressure = pressure,
                temperature = temperature,
                tomorrowsHighTemperature = tomorrowsHighTemperature,
                tomorrowsLowTemperature = tomorrowsLowTemperature,
                alerts = alerts,
                conditions = conditions,
                tomorrowsConditions = tomorrowsConditions
            )
        except ValueError:
            print(f'Weather Report for \"{location.getId()}\" has a data error')

        if weatherReport == None:
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
