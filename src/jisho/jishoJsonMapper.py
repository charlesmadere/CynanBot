from typing import Any

from .jishoAttribution import JishoAttribution
from .jishoData import JishoData
from .jishoJapaneseWord import JishoJapaneseWord
from .jishoJlptLevel import JishoJlptLevel
from .jishoJsonMapperInterface import JishoJsonMapperInterface
from .jishoMeta import JishoMeta
from .jishoResponse import JishoResponse
from .jishoSense import JishoSense
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface


class JishoJsonMapper(JishoJsonMapperInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

    async def parseAttribution(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> JishoAttribution | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        dbpedia: bool | None = None
        dbpediaUrl: str | None = None
        if 'dbpedia' in jsonContents:
            if utils.isValidBool(jsonContents.get('dbpedia')):
                dbpedia = utils.getBoolFromDict(jsonContents, 'dbpedia')
            elif utils.isValidUrl(jsonContents.get('dbpedia')):
                dbpediaUrl = utils.getStrFromDict(jsonContents, 'dbpedia')

        jmdict: bool | None = None
        jmdictUrl: str | None = None
        if 'jmdict' in jsonContents:
            if utils.isValidBool(jsonContents.get('jmdict')):
                jmdict = utils.getBoolFromDict(jsonContents, 'jmdict')
            elif utils.isValidUrl(jsonContents.get('jmdict')):
                jmdictUrl = utils.getStrFromDict(jsonContents, 'jmdict')

        jmnedict: bool | None = None
        jmnedictUrl: str | None = None
        if 'jmnedict' in jsonContents:
            if utils.isValidBool(jsonContents.get('jmnedict')):
                jmnedict = utils.getBoolFromDict(jsonContents, 'jmnedict')
            elif utils.isValidUrl(jsonContents.get('jmnedict')):
                jmnedictUrl = utils.getStrFromDict(jsonContents, 'jmnedict')

        if dbpedia is None and dbpediaUrl is None and \
            jmdict is None and jmdictUrl is None and \
            jmnedict is None and jmnedictUrl is None:
            return None

        return JishoAttribution(
            dbpedia = dbpedia,
            jmdict = jmdict,
            jmnedict = jmnedict,
            dbpediaUrl = dbpediaUrl,
            jmdictUrl = jmdictUrl,
            jmnedictUrl = jmnedictUrl
        )

    async def parseData(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> JishoData | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        isCommon = utils.getBoolFromDict(jsonContents, 'is_common', fallback = False)
        attribution = await self.parseAttribution(jsonContents.get('attribution'))

        japaneseArray: list[dict[str, Any]] | None = jsonContents.get('japanese')
        japaneseWords: list[JishoJapaneseWord] = list()

        if isinstance(japaneseArray, list) and len(japaneseArray) >= 1:
            for index, japaneseWordEntry in enumerate(japaneseArray):
                japaneseWord = await self.parseJapaneseWord(japaneseWordEntry)

                if japaneseWord is None:
                    self.__timber.log('JishoJsonMapper', f'Unable to parse value at index {index} for \"japanese\" data: ({jsonContents=})')
                else:
                    japaneseWords.append(japaneseWord)

        if len(japaneseWords) == 0:
            self.__timber.log('JishoJsonMapper', f'Encountered missing/invalid \"japanese\" field in JSON data: ({jsonContents=})')
            return None

        jlptArray: list[str | None] | None = jsonContents.get('jlpt')
        jlptLevels: list[JishoJlptLevel] | None = None

        if isinstance(jlptArray, list) and len(jlptArray) >= 1:
            jlptLevels = list()

            for index, jlptEntryString in enumerate(jlptArray):
                jlptLevel = await self.parseJlptLevel(jlptEntryString)

                if jlptLevel is None:
                    self.__timber.log('JishoJsonMapper', f'Unable to parse value at index {index} for \"jlpt\" data: ({jsonContents=})')
                else:
                    jlptLevels.append(jlptLevel)

            if len(jlptLevels) == 0:
                jlptLevels = None
            else:
                jlptLevels.sort(key = lambda jlptLevel: jlptLevel.value)

        sensesArray: list[dict[str, Any] | None] | None = jsonContents.get('senses')
        senses: list[JishoSense] = list()

        if isinstance(sensesArray, list) and len(sensesArray) >= 1:
            for index, senseEntryJson in enumerate(sensesArray):
                sense = await self.parseSense(senseEntryJson)

                if sense is None:
                    self.__timber.log('JishoJsonMapper', f'Unable to parse value for \"senses\" data: ({jsonContents=})')
                else:
                    senses.append(sense)

        if len(senses) == 0:
            self.__timber.log('JishoJsonMapper', f'Encountered missing/invalid \"senses\" field in JSON data: ({jsonContents=})')
            return None

        slug = utils.getStrFromDict(jsonContents, 'slug')

        return JishoData(
            isCommon = isCommon,
            attribution = attribution,
            japanese = japaneseWords,
            jlptLevels = jlptLevels,
            senses = senses,
            slug = slug
        )

    async def parseJapaneseWord(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> JishoJapaneseWord | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        reading: str | None = None
        if 'reading' in jsonContents and utils.isValidStr(jsonContents.get('reading')):
            reading = utils.getStrFromDict(jsonContents, 'reading')

        word: str | None = None
        if 'word' in jsonContents and utils.isValidStr(jsonContents.get('word')):
            word = utils.getStrFromDict(jsonContents, 'word')

        if reading is None and word is None:
            return None

        return JishoJapaneseWord(
            reading = reading,
            word = word
        )

    async def parseJlptLevel(
        self,
        jsonString: str | Any | None
    ) -> JishoJlptLevel | None:
        if not utils.isValidStr(jsonString):
            return None

        jsonString = jsonString.lower()

        match jsonString:
            case 'jlpt-n1': return JishoJlptLevel.N1
            case 'jlpt-n2': return JishoJlptLevel.N2
            case 'jlpt-n3': return JishoJlptLevel.N3
            case 'jlpt-n4': return JishoJlptLevel.N4
            case 'jlpt-n5': return JishoJlptLevel.N5
            case _:
                self.__timber.log('JishoJsonMapper', f'Encountered unknown JishoJlptLevel value: \"{jsonString}\"')
                return None

    async def parseMeta(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> JishoMeta | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        status = utils.getIntFromDict(jsonContents, 'status')

        return JishoMeta(
            status = status
        )

    async def parseResponse(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> JishoResponse | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        meta = await self.parseMeta(jsonContents.get('meta'))
        if meta is None:
            self.__timber.log('JishoJsonMapper', f'Encountered missing/invalid \"meta\" field in JSON data: ({jsonContents=})')
            return None

        dataArray: list[dict[str, Any] | None] | None = jsonContents.get('data')
        data: list[JishoData] = list()

        if isinstance(dataArray, list) and len(dataArray) >= 1:
            for index, dataEntryJson in enumerate(dataArray):
                dataEntry = await self.parseData(dataEntryJson)

                if dataEntry is None:
                    self.__timber.log('JishoJsonMapper', f'Unable to parse value at index {index} for \"data\" data: ({jsonContents=})')
                else:
                    data.append(dataEntry)

        return JishoResponse(
            data = data,
            meta = meta
        )

    async def parseSense(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> JishoSense | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        englishDefinitionsArray: list[str | None] | None = jsonContents.get('english_definitions')
        englishDefinitions: list[str] = list()

        if isinstance(englishDefinitionsArray, list) and len(englishDefinitionsArray) >= 1:
            for index, englishDefinition in enumerate(englishDefinitionsArray):
                if utils.isValidStr(englishDefinition):
                    englishDefinitions.append(englishDefinition)
                else:
                    self.__timber.log('JishoJsonMapper', f'Unable to parse value at index {index} for \"english_definitions\" data: ({jsonContents=})')

        if len(englishDefinitions) == 0:
            self.__timber.log('JishoJsonMapper', f'Encountered missing/invalid \"english_definitions\" field in JSON data: ({jsonContents=})')
            return None

        partsOfSpeechArray: list[str | None] | None = jsonContents.get('parts_of_speech')
        partsOfSpeech: list[str] | None = None

        if isinstance(partsOfSpeechArray, list) and len(partsOfSpeechArray) >= 1:
            partsOfSpeech = list()

            for index, partOfSpeech in enumerate(partsOfSpeechArray):
                if utils.isValidStr(partOfSpeech):
                    partsOfSpeech.append(partOfSpeech)
                else:
                    self.__timber.log('JishoJsonMapper', f'Unable to parse value at index {index} for \"parts_of_speech\" data: ({jsonContents=})')

            if len(partsOfSpeech) == 0:
                partsOfSpeech = None

        tagsArray: list[str | None] | None = jsonContents.get('tags')
        tags: list[str] | None = None

        if isinstance(tagsArray, list) and len(tagsArray) >= 1:
            tags = list()

            for index, tag in enumerate(tagsArray):
                if utils.isValidStr(tag):
                    tags.append(tag)
                else:
                    self.__timber.log('JishoJsonMapper', f'Unable to parse value at index {index} for \"tags\" data: ({jsonContents=})')

            if len(tags) == 0:
                tags = None

        return JishoSense(
            englishDefinitions = englishDefinitions,
            partsOfSpeech = partsOfSpeech,
            tags = tags
        )
