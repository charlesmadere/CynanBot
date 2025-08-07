import traceback
from typing import Any

from .exceptions import WotdApiCodeUnavailableException
from .transparentApiServiceInterface import TransparentApiServiceInterface
from .transparentResponse import TransparentResponse
from .transparentXmlMapperInterface import TransparentXmlMapperInterface
from ..language.languageEntry import LanguageEntry
from ..misc import utils as utils
from ..network.exceptions import GenericNetworkException
from ..network.networkClientProvider import NetworkClientProvider
from ..timber.timberInterface import TimberInterface


class TransparentApiService(TransparentApiServiceInterface):

    def __init__(
        self,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface,
        transparentXmlMapper: TransparentXmlMapperInterface,
    ):
        if not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(transparentXmlMapper, TransparentXmlMapperInterface):
            raise TypeError(f'transparentXmlMapper argument is malformed: \"{transparentXmlMapper}\"')

        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__timber: TimberInterface = timber
        self.__transparentXmlMapper: TransparentXmlMapperInterface = transparentXmlMapper

    async def fetchWordOfTheDay(
        self,
        targetLanguage: LanguageEntry
    ) -> TransparentResponse:
        if not isinstance(targetLanguage, LanguageEntry):
            raise TypeError(f'targetLanguage argument is malformed: \"{targetLanguage}\"')

        self.__timber.log('TransparentApiService', f'Fetching Word of the Day from Transparent... ({targetLanguage=})')
        clientSession = await self.__networkClientProvider.get()

        wotdApiCode = targetLanguage.wotdApiCode
        if not utils.isValidStr(wotdApiCode):
            raise WotdApiCodeUnavailableException(
                languageEntry = targetLanguage,
                message = f'No WOTD API code is available for the given targetLanguage ({wotdApiCode=}) ({targetLanguage=})'
            )

        ################################################################################
        ## retrieve word of the day from https://www.transparent.com/word-of-the-day/ ##
        ################################################################################

        try:
            response = await clientSession.get(f'https://wotd.transparent.com/rss/{wotdApiCode}-widget.xml?t=0')
        except GenericNetworkException as e:
            self.__timber.log('TransparentApiService', f'Encountered network error when fetching word of the day ({targetLanguage=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'TransparentApiService encountered network error when fetching word of the day ({targetLanguage=}): {e}')

        responseStatusCode = response.statusCode
        xmlResponse = await response.xml()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TransparentApiService', f'Encountered non-200 HTTP status code when fetching word of the day ({targetLanguage=}) ({responseStatusCode=}) ({response=}) ({xmlResponse=})')
            raise GenericNetworkException(f'TransparentApiService encountered non-200 HTTP status code when fetching word of the day ({targetLanguage=}) ({responseStatusCode=}) ({response=}) ({xmlResponse=})')
        elif not isinstance(xmlResponse, dict) or len(xmlResponse) == 0:
            self.__timber.log('TransparentApiService', f'Encountered missing/invalid XML data when fetching word of the day ({targetLanguage=}) ({responseStatusCode=}) ({response=}) ({xmlResponse=})')
            raise GenericNetworkException(f'TransparentApiService encountered missing/invalid XML data when fetching word of the day ({targetLanguage=}) ({responseStatusCode=}) ({response=}) ({xmlResponse=})')

        xmlRoot: dict[str, Any] | Any | None = xmlResponse.get('xml')
        if not isinstance(xmlRoot, dict) or len(xmlRoot) == 0:
            self.__timber.log('TransparentApiService', f'Encountered missing/invalid \"xml\" data in XML when fetching word of the day ({targetLanguage=}) ({responseStatusCode=}) ({response=}) ({xmlResponse=}) ({xmlRoot=})')
            raise GenericNetworkException(f'TransparentApiService encountered missing/invalid \"xml\" data when fetching word of the day ({targetLanguage=}) ({responseStatusCode=}) ({response=}) ({xmlResponse=}) ({xmlRoot=})')

        transparentResponse = await self.__transparentXmlMapper.parseTransparentResponse(xmlRoot.get('words'))

        if transparentResponse is None:
            self.__timber.log('TransparentApiService', f'Failed to parse JSON response into TransparentResponse instance ({targetLanguage=}) ({responseStatusCode=}) ({response=}) ({xmlResponse=}) ({xmlRoot=}) ({transparentResponse=})')
            raise GenericNetworkException(f'TransparentApiService failed to parse JSON response into TransparentResponse instance ({targetLanguage=}) ({responseStatusCode=}) ({response=}) ({xmlResponse=}) ({xmlRoot=}) ({transparentResponse=})')

        return transparentResponse
