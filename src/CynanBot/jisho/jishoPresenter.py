import CynanBot.misc.utils as utils
from CynanBot.jisho.jishoJlptLevel import JishoJlptLevel
from CynanBot.jisho.jishoPresenterInterface import JishoPresenterInterface
from CynanBot.jisho.jishoResponse import JishoResponse


class JishoPresenter(JishoPresenterInterface):

    def __init__(
        self,
        definitionsMaxSize: int = 3
    ):
        if not utils.isValidInt(definitionsMaxSize):
            raise TypeError(f'definitionsMaxSize argument is malformed: \"{definitionsMaxSize}\"')
        elif definitionsMaxSize < 1 or definitionsMaxSize > 5:
            raise ValueError(f'definitionsMaxSize argument is out of bounds: \"{definitionsMaxSize}\"')

        self.__definitionsMaxSize: int = definitionsMaxSize

    async def __jlptToString(self, jlptLevel: JishoJlptLevel) -> str:
        match jlptLevel:
            case JishoJlptLevel.N1: return '(JLPT N1)'
            case JishoJlptLevel.N2: return '(JLPT N2)'
            case JishoJlptLevel.N3: return '(JLPT N3)'
            case JishoJlptLevel.N4: return '(JLPT N4)'
            case JishoJlptLevel.N5: return '(JLPT N5)'
            case _: raise ValueError(f'unknown JishoJlptLevel value: \"{jlptLevel}\"')

    async def toStrings(self, jishoResponse: JishoResponse) -> list[str]:
        if not isinstance(jishoResponse, JishoResponse):
            raise TypeError(f'jishoResponse argument is malformed: \"{jishoResponse}\"')

        definitions: list[str] = list()
        index = 0

        while index < len(jishoResponse.data) and len(definitions) <= self.__definitionsMaxSize:
            jishoData = jishoResponse.data[index]
            jishoJapanese = jishoData.japanese[0]
            jishoSense = jishoData.senses[0]

            jlptLevel: str = ''
            if jishoData.jlptLevels is not None and len(jishoData.jlptLevels) >= 1:
                jlptLevel = await self.__jlptToString(jishoData.jlptLevels[0])

            definition = f'{jishoJapanese.word} ({jishoJapanese.reading}) — {jishoSense.englishDefinitions[0]} {jlptLevel}'.strip()
            definitions.append(definition)
            index = index + 1

        return definitions
