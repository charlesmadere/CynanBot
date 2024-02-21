import traceback
from typing import Any, Dict, List, Optional
from urllib.parse import quote

import CynanBot.misc.utils as utils
from CynanBot.language.jishoHelperInterface import JishoHelperInterface
from CynanBot.language.jishoResult import JishoResult
from CynanBot.language.jishoVariant import JishoVariant
from CynanBot.network.exceptions import GenericNetworkException
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.timber.timberInterface import TimberInterface


class JishoHelper(JishoHelperInterface):

    def __init__(
        self,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface,
        definitionsMaxSize: int = 3,
        variantsMaxSize: int = 3
    ):
        assert isinstance(networkClientProvider, NetworkClientProvider), f"malformed {networkClientProvider=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        if not utils.isValidInt(definitionsMaxSize):
            raise ValueError(f'definitionsMaxSize argument is malformed: \"{definitionsMaxSize}\"')
        if definitionsMaxSize < 1 or definitionsMaxSize > 5:
            raise ValueError(f'definitionsMaxSize argument is out of bounds: \"{definitionsMaxSize}\"')
        if not utils.isValidInt(variantsMaxSize):
            raise ValueError(f'variantsMaxSize argument is malformed: \"{variantsMaxSize}\"')
        if variantsMaxSize < 1 or variantsMaxSize > 5:
            raise ValueError(f'variantsMaxSize argument is out of bounds: \"{variantsMaxSize}\"')

        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__timber: TimberInterface = timber
        self.__definitionsMaxSize: int = definitionsMaxSize
        self.__variantsMaxSize: int = variantsMaxSize

    async def search(self, query: str) -> JishoResult:
        if not utils.isValidStr(query):
            raise ValueError(f'query argument is malformed: \"{query}\"')

        query = utils.cleanStr(query)
        encodedQuery = quote(query)
        self.__timber.log('JishoHelper', f'Looking up \"{query}\" at Jisho...')
        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(f'https://jisho.org/api/v1/search/words?keyword={encodedQuery}')
        except GenericNetworkException as e:
            self.__timber.log('JishoHelper', f'Encountered network error when searching Jisho for \"{query}\": {e}', e, traceback.format_exc())
            raise RuntimeError(f'Encountered network error when searching Jisho for \"{query}\": {e}')

        if response.getStatusCode() != 200:
            self.__timber.log('JishoHelper', f'Encountered non-200 HTTP status code when searching Jisho for \"{query}\": {response.getStatusCode()}')
            raise RuntimeError(f'Encountered non-200 HTTP status code when searching Jisho for \"{query}\": {response.getStatusCode()}')

        jsonResponse: Optional[Dict[str, Any]] = await response.json()
        await response.close()

        if not utils.hasItems(jsonResponse):
            raise RuntimeError(f'Jisho\'s response for \"{query}\" has malformed or empty JSON: {jsonResponse}')
        if 'meta' not in jsonResponse or utils.getIntFromDict(jsonResponse['meta'], 'status') != 200:
            raise RuntimeError(f'Jisho\'s response for \"{query}\" has an invalid \"status\": {jsonResponse}')
        if not utils.hasItems(jsonResponse['data']):
            raise RuntimeError(f'Jisho\'s response for \"{query}\" has malformed or empty \"data\": {jsonResponse}')

        variants: List[JishoVariant] = list()
        for variantJson in jsonResponse['data']:
            if not utils.hasItems(variantJson['japanese']):
                raise RuntimeError(f'Jisho\'s response for \"{query}\" has malformed or empty \"japanese\": {jsonResponse}')
            if not utils.hasItems(variantJson['senses']):
                raise RuntimeError(f'Jisho\'s response for \"{query}\" has malformed or empty \"senses\": {jsonResponse}')

            word = utils.cleanStr(variantJson['japanese'][0].get('word', ''))
            furigana = utils.cleanStr(variantJson['japanese'][0].get('reading', ''))

            if not utils.isValidStr(word) and not utils.isValidStr(furigana):
                continue

            definitions: List[str] = list()
            for definition in variantJson['senses'][0]['english_definitions']:
                definitions.append(utils.cleanStr(definition))

                if len(definitions) >= self.__definitionsMaxSize:
                    break

            partsOfSpeech: List[str] = list()
            for partOfSpeech in variantJson['senses'][0]['parts_of_speech']:
                partsOfSpeech.append(utils.cleanStr(partOfSpeech))

                if len(partsOfSpeech) >= self.__definitionsMaxSize:
                    break

            variants.append(JishoVariant(
                definitions = definitions,
                partsOfSpeech = partsOfSpeech,
                furigana = furigana,
                word = word
            ))

            if len(variants) >= self.__variantsMaxSize:
                break

        return JishoResult(
            variants = variants,
            initialQuery = query
        )
