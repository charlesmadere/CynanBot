import json
from datetime import datetime, timedelta

import requests


class JokesRepository():

    def __init__(
        self,
        cacheTimeDelta = timedelta(hours = 1)
    ):
        if cacheTimeDelta == None:
            raise ValueError(f'cacheTimeDelta argument is malformed: \"{cacheTimeDelta}\"')

        self.__cacheTime = datetime.now() - cacheTimeDelta
        self.__cacheTimeDelta = cacheTimeDelta
        self.__jokeReponse = None

    def fetchJoke(self):
        if self.__cacheTime + self.__cacheTimeDelta < datetime.now() or self.__jokeReponse == None:
            self.__jokeResponse = self.__refreshJoke()
            self.__cacheTime = datetime.now()

        return self.__jokeResponse

    def __refreshJoke(self):
        print('Refreshing joke of the day...')

        # Retrieve "Joke of the Day" from: https://jokes.one/api/joke/
        rawResponse = requests.get('https://api.jokes.one/jod')
        jsonResponse = rawResponse.json()

        successJson = jsonResponse.get('success')
        if successJson == None or len(successJson) == 0:
            return None

        jokesResponse = jsonResponse['contents']['jokes']
        if len(jokesResponse) == 0:
            return None

        jokeResponse = jokesResponse[0]['joke']

        if jokeResponse.get('clean') != '1':
            cleanValue = jokeResponse['clean']
            print(f'Rejecting joke because \'clean\' value is not 1: \"{cleanValue}\"')
            return None
        elif jokeResponse.get('racial') != '0':
            racialValue = jokeResponse['racial']
            print(f'Rejecting joke because \'racial\' value is not 0: \"{racialValue}\"')
            return None

        text = jokeResponse['text']

        if text == None or len(text) == 0 or text.isspace():
            print(f'Rejecting joke because \'text\' value is malformed: \"{text}\"')
            return None

        text = text.replace('\r\n', ' ').strip()

        return JokeResponse(
            length = int(jokeResponse['length']),
            text = text,
            title = jokeResponse['title'].strip()
        )

class JokeResponse():

    def __init__(
        self,
        length: int,
        text: str,
        title: str
    ):
        if length == None or length < 1:
            raise ValueError(f'length argument is malformed: \"{length}\"')
        elif text == None or len(text) == 0 or text.isspace():
            raise ValueError(f'text argument is malformed: \"{text}\"')
        elif title == None or len(title) == 0 or title.isspace():
            raise ValueError(f'title argument is malformed: \"{title}\"')

        self.__length = length
        self.__text = text
        self.__title = title

    def getLength(self):
        return self.__length

    def getText(self):
        return self.__text

    def getTitle(self):
        return self.__title

    def toStr(self):
        return f'Joke of the Day — {self.__text}'
