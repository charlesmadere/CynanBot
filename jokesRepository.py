import json
from datetime import datetime, timedelta

import requests

import CynanBotCommon.utils as utils


class JokesRepository():

    def __init__(
        self,
        cacheTimeDelta=timedelta(hours=1)
    ):
        if cacheTimeDelta is None:
            raise ValueError(f'cacheTimeDelta argument is malformed: \"{cacheTimeDelta}\"')

        self.__cacheTime = datetime.now() - cacheTimeDelta
        self.__cacheTimeDelta = cacheTimeDelta
        self.__jokeReponse = None

    def fetchJoke(self):
        if self.__cacheTime + self.__cacheTimeDelta < datetime.now() or self.__jokeReponse is None:
            self.__jokeResponse = self.__refreshJoke()
            self.__cacheTime = datetime.now()

        return self.__jokeResponse

    def __refreshJoke(self):
        print('Refreshing joke of the day...')

        # This used to be a feature but has been removed since the API endpoint in use was
        # unpredictable and had unfortunately terrible taste. Maybe in the future we can use a new
        # API endpoint or something.

        raise NotImplementedError('Joke of the day is not currently an implemented feature.')


class JokeResponse():

    def __init__(self, text: str):
        if not utils.isValidStr(text):
            raise ValueError(f'text argument is malformed: \"{text}\"')

        self.__text = text

    def getText(self):
        return self.__text

    def toStr(self):
        return f'Joke of the Day — {self.__text} 🥁'
