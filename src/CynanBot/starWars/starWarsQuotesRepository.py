import random
import re
from typing import Any, Dict, List, Optional, Pattern

import CynanBot.misc.utils as utils
from CynanBot.starWars.starWarsQuotesRepositoryInterface import \
    StarWarsQuotesRepositoryInterface
from CynanBot.storage.jsonReaderInterface import JsonReaderInterface


class StarWarsQuotesRepository(StarWarsQuotesRepositoryInterface):

    def __init__(self, quotesJsonReader: JsonReaderInterface):
        assert isinstance(quotesJsonReader, JsonReaderInterface), f"malformed {quotesJsonReader=}"

        self.__quotesJsonReader: JsonReaderInterface = quotesJsonReader

        self.__cache: Optional[Dict[str, Any]] = None
        self.__quoteInputRegEx: Pattern = re.compile(r'\$\((.*)\)', re.IGNORECASE)

    async def clearCaches(self):
        self.__cache.clear()

    async def fetchRandomQuote(self, trilogy: Optional[str] = None) -> str:
        jsonContents = await self.__getQuotes(trilogy)
        quote = random.choice(jsonContents)
        return self.__processQuote(quote)

    async def __getQuotes(self, trilogy: str = None) -> List[str]:
        trilogy = utils.cleanStr(trilogy)
        jsonContents = await self.__readJson()
        quotes: Optional[Dict[str, List[str]]] = jsonContents.get('quotes')

        if not utils.hasItems(quotes):
            raise RuntimeError(f'No quotes are available: \"{jsonContents}\"')

        if utils.isValidStr(trilogy) and trilogy in quotes.keys():
            result = quotes[trilogy]
        else:
            result = [ item for sublist in quotes.values() for item in sublist ]

        return result

    def __processQuote(self, quote: str, input: str = None) -> str:
        result = self.__quoteInputRegEx.search(quote)
        if not result:
            return quote

        value = result.group(1)
        if utils.isValidStr(input):
            value = input

        return quote.replace(result.group(0), value)

    async def __readJson(self) -> Dict[str, Any]:
        if self.__cache is not None:
            return self.__cache

        jsonContents: Optional[Dict[str, Any]] = None

        if await self.__quotesJsonReader.fileExistsAsync():
            jsonContents = await self.__quotesJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if jsonContents is None:
            raise IOError(f'Error reading from trivia settings file: {self.__quotesJsonReader}')

        self.__cache = jsonContents
        return jsonContents

    async def searchQuote(self, query: str, input: Optional[str] = None) -> str:
        if not utils.isValidStr(query):
            raise ValueError(f'query argument is malformed: \"{query}\"')

        query = utils.cleanStr(query)
        jsonContents = await self.__getQuotes()

        for quote in jsonContents:
            if self.__processQuote(quote).lower().find(query.lower()) >= 0:
                return self.__processQuote(quote, input = input)

        return None
