from typing import Final

from frozenlist import FrozenList

from .jishoJlptLevel import JishoJlptLevel
from .jishoPresenterInterface import JishoPresenterInterface
from .jishoResponse import JishoResponse
from ..misc import utils as utils


class JishoPresenter(JishoPresenterInterface):

    def __init__(
        self,
        definitionsMaxSize: int = 3,
    ):
        if not utils.isValidInt(definitionsMaxSize):
            raise TypeError(f'definitionsMaxSize argument is malformed: \"{definitionsMaxSize}\"')
        elif definitionsMaxSize < 1 or definitionsMaxSize > utils.getIntMaxSafeSize():
            raise ValueError(f'definitionsMaxSize argument is out of bounds: \"{definitionsMaxSize}\"')

        self.__definitionsMaxSize: Final[int] = definitionsMaxSize

    async def __jlptToString(self, jlptLevel: JishoJlptLevel) -> str:
        match jlptLevel:
            case JishoJlptLevel.N1: return '(JLPT N1)'
            case JishoJlptLevel.N2: return '(JLPT N2)'
            case JishoJlptLevel.N3: return '(JLPT N3)'
            case JishoJlptLevel.N4: return '(JLPT N4)'
            case JishoJlptLevel.N5: return '(JLPT N5)'
            case _: raise ValueError(f'unknown JishoJlptLevel value: \"{jlptLevel}\"')

    async def toStrings(
        self,
        includeRomaji: bool,
        jishoResponse: JishoResponse,
    ) -> FrozenList[str]:
        if not utils.isValidBool(includeRomaji):
            raise TypeError(f'includeRomaji argument is malformed: \"{includeRomaji}\"')
        elif not isinstance(jishoResponse, JishoResponse):
            raise TypeError(f'jishoResponse argument is malformed: \"{jishoResponse}\"')

        strings: FrozenList[str] = FrozenList()

        if len(jishoResponse.data) == 0:
            strings.append(f'ⓘ No Jisho results')
            strings.freeze()
            return strings

        index = 0

        while index < len(jishoResponse.data) and len(strings) < self.__definitionsMaxSize:
            jishoData = jishoResponse.data[index]
            jishoJapanese = jishoData.japanese[0]
            jishoSense = jishoData.senses[0]

            jlptLevel: str = ''
            if jishoData.jlptLevels is not None and len(jishoData.jlptLevels) >= 1:
                jlptLevel = await self.__jlptToString(jishoData.jlptLevels[0])

            wordAndReading: str
            if utils.isValidStr(jishoJapanese.word) and utils.isValidStr(jishoJapanese.reading):
                wordAndReading = f'{jishoJapanese.word} ({jishoJapanese.reading})'
            elif utils.isValidStr(jishoJapanese.word):
                wordAndReading = jishoJapanese.word
            elif utils.isValidStr(jishoJapanese.reading):
                wordAndReading = jishoJapanese.reading
            else:
                raise ValueError(f'Illegal/impossible Jisho value: \"{jishoJapanese}\"')

            definition = f'{wordAndReading} — {jishoSense.englishDefinitions[0]} {jlptLevel}'.strip()
            strings.append(definition)
            index = index + 1

        strings.freeze()
        return strings
