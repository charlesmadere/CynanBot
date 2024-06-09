import traceback

import CynanBot.misc.utils as utils
from CynanBot.jisho.jishoApiServiceInterface import JishoApiServiceInterface
from CynanBot.jisho.jishoJlptLevel import JishoJlptLevel
from CynanBot.jisho.jishoResponse import JishoResponse
from CynanBot.language.jishoHelperInterface import JishoHelperInterface
from CynanBot.network.exceptions import GenericNetworkException
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.timber.timberInterface import TimberInterface


class JishoHelper(JishoHelperInterface):

    def __init__(
        self,
        jishoApiService: JishoApiServiceInterface,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface,
        definitionsMaxSize: int = 3
    ):
        if not isinstance(jishoApiService, JishoApiServiceInterface):
            raise TypeError(f'jishoApiService argument is malformed: \"{jishoApiService}\"')
        elif not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidInt(definitionsMaxSize):
            raise TypeError(f'definitionsMaxSize argument is malformed: \"{definitionsMaxSize}\"')
        elif definitionsMaxSize < 1 or definitionsMaxSize > 5:
            raise ValueError(f'definitionsMaxSize argument is out of bounds: \"{definitionsMaxSize}\"')

        self.__jishoApiService: JishoApiServiceInterface = jishoApiService
        self.__timber: TimberInterface = timber
        self.__definitionsMaxSize: int = definitionsMaxSize

    async def __jlptToString(self, jlptLevel: JishoJlptLevel) -> str:
        match jlptLevel:
            case JishoJlptLevel.N1: return '(JLPT N1)'
            case JishoJlptLevel.N2: return '(JLPT N2)'
            case JishoJlptLevel.N3: return '(JLPT N3)'
            case JishoJlptLevel.N4: return '(JLPT N4)'
            case JishoJlptLevel.N5: return '(JLPT N5)'
            case _: raise ValueError(f'unknown JishoJlptLevel value: \"{jlptLevel}\"')

    async def search(self, query: str) -> list[str]:
        if not utils.isValidStr(query):
            raise TypeError(f'query argument is malformed: \"{query}\"')

        try:
            response = await self.__jishoApiService.search(query)
        except GenericNetworkException as e:
            self.__timber.log('JishoHelper', f'Encountered network error when searching Jisho ({query=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'JishoHelper encountered network error when searching Jisho ({query=}): {e}')

        definitions: list[str] = list()
        index = 0

        while index < len(response.data) and len(definitions) < self.__definitionsMaxSize:
            jishoData = response.data[index]
            jishoJapanese = jishoData.japanese[0]
            jishoSense = jishoData.senses[0]

            jlptLevel: str = ''
            if jishoData.jlptLevels is not None and len(jishoData.jlptLevels) >= 1:
                jlptLevel = await self.__jlptToString(jishoData.jlptLevels[0])

            definition = f'{jishoJapanese.word} ({jishoJapanese.reading}) — {jishoSense.partsOfSpeech[0]} {jlptLevel}'.strip()
            definitions.append(definition)

        return definitions
