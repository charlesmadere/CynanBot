import json
import random
import re
from typing import Any, Dict, List

import aiofiles
import aiofiles.ospath

import CynanBot.misc.utils as utils


class StarWarsQuotesRepository():

    def __init__(
        self,
        quotesFile: str = 'CynanBotCommon/starWars/starWarsQuotesRepository.json'
    ):
        if not utils.isValidStr(quotesFile):
            raise ValueError(f'quotesFile argument is malformed: \"{quotesFile}\"')

        self.__quotesFile: str = quotesFile
        self.__quoteInputRegEx = re.compile('\$\((.*)\)')

    async def fetchRandomQuote(self, trilogy: str = None) -> str:
        jsonContents = await self.__getQuotes(trilogy)
        quote = random.choice(jsonContents)
        return self.__processQuote(quote)

    async def __getQuotes(self, trilogy: str = None) -> List[str]:
        trilogy = utils.cleanStr(trilogy)
        jsonContents = await self.__readJson()

        quotes = jsonContents.get('quotes')
        if not utils.hasItems(quotes):
            raise ValueError(f'JSON contents of quotes file \"{self.__quotesFile}\" is missing \"quotes\" key')

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
        if not await aiofiles.ospath.exists(self.__quotesFile):
            raise FileNotFoundError(f'quotes file not found: \"{self.__quotesFile}\"')

        async with aiofiles.open(self.__quotesFile, mode = 'r') as file:
            data = await file.read()
            jsonContents = json.loads(data)

        if jsonContents is None:
            raise IOError(f'Error reading from quotes file: \"{self.__quotesFile}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of quotes file \"{self.__quotesFile}\" is empty')

        return jsonContents

    async def searchQuote(self, query: str, input: str = None) -> str:
        if not utils.isValidStr(query):
            raise ValueError(f'query argument is malformed: \"{query}\"')

        query = utils.cleanStr(query)
        jsonContents = await self.__getQuotes()

        for quote in jsonContents:
            if self.__processQuote(quote).lower().find(query.lower()) >= 0:
                return self.__processQuote(quote, input = input)

        return None
