from typing import Any

from CynanBot.jisho.jishoMeta import JishoMeta
from CynanBot.jisho.jishoResponse import JishoResponse
import CynanBot.misc.utils as utils
from CynanBot.jisho.jishoData import JishoData
from CynanBot.jisho.jishoJlptLevel import JishoJlptLevel
from CynanBot.jisho.jishoJsonMapperInterface import JishoJsonMapperInterface
from CynanBot.timber.timberInterface import TimberInterface


class JishoJsonMapper(JishoJsonMapperInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

    async def parseData(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> JishoData | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        isCommon = utils.getBoolFromDict(jsonContents, 'is_common')

        jlptArray: list[str | None] | None = jsonContents.get('jlpt')
        jlpt: set[JishoJlptLevel] | None = None

        if isinstance(jlptArray, list) and len(jlptArray) >= 1:
            jlpt = set()

            for index, jlptEntryString in enumerate(jlptArray):
                jlptLevel = await self.parseJlptLevel(jlptEntryString)

                if jlptLevel is None:
                    self.__timber.log('JishoJsonMapper', f'Unable to parse value at index {index} for \"jlpt\" data: ({jsonContents=})')
                else:
                    jlpt.add(jlptLevel)

        slug = utils.getStrFromDict(jsonContents, 'slug')

        return JishoData(
            isCommon = isCommon,
            jlpt = jlpt,
            slug = slug
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
        data: list[JishoData] | None = None

        if isinstance(dataArray, list) and len(dataArray) >= 1:
            data = list()

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
