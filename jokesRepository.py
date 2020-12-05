import json
from datetime import datetime, timedelta

import requests

import utils


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

        # Retrieve "Joke of the Day" from: https://jokes.one/api/joke/
        rawResponse = requests.get('https://api.jokes.one/jod')
        jsonResponse = rawResponse.json()

        successJson = jsonResponse.get('success')
        if successJson is None or len(successJson) == 0:
            print(f'Joke JSON has malformed \'success\' data: \"{jsonResponse}\"')
            return None

        jokesResponse = jsonResponse.get('contents').get('jokes')
        if jokesResponse is None or len(jokesResponse) == 0:
            print(f'Joke JSON is malformed: \"{jsonResponse}\"')
            return None

        jokeResponse = jokesResponse[0]['joke']

        joke = JokeResponse(
            clean=utils.getIntFromDict(jokeResponse, 'clean', fallback=0),
            length=utils.getIntFromDict(jokeResponse, 'length'),
            racial=utils.getIntFromDict(jokeResponse, 'racial', fallback=0),
            _id=utils.getStrFromDict(jokeResponse, 'id'),
            text=utils.getStrFromDict(jokeResponse, 'text', clean=True),
            title=utils.getStrFromDict(jokeResponse, 'title')
        )

        # I used to also check the joke's `clean` value, and return None if it was != 0. But then I found that
        # sometimes a joke that was clearly "clean" would sometimes have a `clean` value of 0. AND THEN now I've
        # also seen some clean jokes with a `clean` value of null. So whatever, let's just ignore that field.
        if joke.getRacial() != 0:
            print(f'Rejecting joke because of incorrect \'racial\' values: \"{jokeResponse}\"')
            return None

        return joke


class JokeResponse():

    def __init__(
        self,
        clean: int,
        length: int,
        racial: int,
        _id: str,
        text: str,
        title: str
    ):
        if clean is None:
            raise ValueError(f'clean argument is malformed: \"{clean}\"')
        elif length is None:
            raise ValueError(f'length argument is malformed: \"{length}\"')
        elif racial is None:
            raise ValueError(f'racial argument is malformed: \"{racial}\"')
        elif _id is None or len(_id) == 0 or _id.isspace():
            raise ValueError(f'_id argument is malformed: \"{_id}\"')
        elif text is None or len(text) == 0 or text.isspace():
            raise ValueError(f'text argument is malformed: \"{text}\"')
        elif title is None or len(title) == 0 or title.isspace():
            raise ValueError(f'title argument is malformed: \"{title}\"')

        self.__clean = clean
        self.__length = length
        self.__racial = racial
        self.__id = _id
        self.__text = text
        self.__title = title

    def getClean(self):
        return self.__clean

    def getId(self):
        return self.__id

    def getLength(self):
        return self.__length

    def getRacial(self):
        return self.__racial

    def getText(self):
        return self.__text

    def getTitle(self):
        return self.__title

    def toStr(self):
        return f'Joke of the Day — {self.__text}'
