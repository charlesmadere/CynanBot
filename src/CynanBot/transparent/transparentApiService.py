from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.language.languageEntry import LanguageEntry
from CynanBot.network.exceptions import GenericNetworkException
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.transparent.exceptions import WotdApiCodeUnavailableException
from CynanBot.transparent.transparentApiServiceInterface import \
    TransparentApiServiceInterface
from CynanBot.transparent.transparentResponse import TransparentResponse
from CynanBot.transparent.transparentXmlMapperInterface import \
    TransparentXmlMapperInterface


class TransparentApiService(TransparentApiServiceInterface):

    def __init__(
        self,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface,
        transparentXmlMapper: TransparentXmlMapperInterface
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

        wotdApiCode = targetLanguage.getWotdApiCode()
        if not utils.isValidStr(wotdApiCode):
            raise WotdApiCodeUnavailableException(
                languageEntry = targetLanguage,
                message = f'No WOTD API code is available for the given targetLanguage ({wotdApiCode=}) ({targetLanguage=})'
            )

        ##############################################################################
        # retrieve word of the day from https://www.transparent.com/word-of-the-day/ #
        ##############################################################################

        try:
            response = await clientSession.get(f'https://wotd.transparent.com/rss/{wotdApiCode}-widget.xml?t=0')
        except GenericNetworkException as e:
            self.__timber.log('TransparentApiService', f'Encountered network error when fetching word of the day ({targetLanguage=})')
            raise GenericNetworkException(f'TransparentApiService encountered network error when fetching word of the day ({targetLanguage=})')

        responseStatusCode = response.getStatusCode()
        xmlResponse = await response.xml()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('TransparentApiService', f'Encountered non-200 HTTP status code when fetching word of the day ({targetLanguage=}) ({responseStatusCode=}) ({response=}) ({xmlResponse=})')
            raise GenericNetworkException(f'TransparentApiService encountered non-200 HTTP status code when fetching word of the day ({targetLanguage=}) ({responseStatusCode=}) ({response=}) ({xmlResponse=})')
        elif not isinstance(xmlResponse, dict) or len(xmlResponse) == 0:
            self.__timber.log('TransparentApiService', f'Encountered missing/invalid XML data when fetching word of the day ({targetLanguage=}) ({responseStatusCode=}) ({response=}) ({xmlResponse=})')
            raise GenericNetworkException(f'TransparentApiService encountered missing/invalid XML data when fetching word of the day ({targetLanguage=}) ({responseStatusCode=}) ({response=}) ({xmlResponse=})')

        xmlRoot: dict[str, Any] | None = xmlResponse.get('xml')
        if not isinstance(xmlRoot, dict) or len(xmlRoot) == 0:
            self.__timber.log('TransparentApiService', f'Encountered missing/invalid \"xml\" data in XML when fetching word of the day ({targetLanguage=}) ({responseStatusCode=}) ({response=}) ({xmlResponse=})')
            raise GenericNetworkException(f'TransparentApiService encountered missing/invalid \"xml\" data when fetching word of the day ({targetLanguage=}) ({responseStatusCode=}) ({response=}) ({xmlResponse=})')

        transparentResponse = await self.__transparentXmlMapper.parseTransparentResponse(xmlRoot.get('words'))

        if transparentResponse is None:
            self.__timber.log('TransparentApiService', f'Failed to parse JSON response into TransparentResponse instance ({targetLanguage=}) ({responseStatusCode=}) ({response=}) ({xmlResponse=}) ({transparentResponse=})')
            raise GenericNetworkException(f'TransparentApiService failed to parse JSON response into TransparentResponse instance ({targetLanguage=}) ({responseStatusCode=}) ({response=}) ({xmlResponse=}) ({transparentResponse=})')

        return transparentResponse
