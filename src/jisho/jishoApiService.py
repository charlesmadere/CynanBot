import traceback
from urllib.parse import quote

from jisho.jishoApiServiceInterface import JishoApiServiceInterface
from jisho.jishoJsonMapperInterface import JishoJsonMapperInterface
from jisho.jishoResponse import JishoResponse
from network.exceptions import GenericNetworkException
from network.networkClientProvider import NetworkClientProvider
from timber.timberInterface import TimberInterface

from ..misc import utils as utils


class JishoApiService(JishoApiServiceInterface):

    def __init__(
        self,
        jishoJsonMapper: JishoJsonMapperInterface,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface
    ):
        if not isinstance(jishoJsonMapper, JishoJsonMapperInterface):
            raise TypeError(f'jishoJsonMapper argument is malformed: \"{jishoJsonMapper}\"')
        elif not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__jishoJsonMapper: JishoJsonMapperInterface = jishoJsonMapper
        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__timber: TimberInterface = timber

    async def search(self, keyword: str) -> JishoResponse:
        if not utils.isValidStr(keyword):
            raise TypeError(f'keyword argument is malformed: \"{keyword}\"')

        keyword = utils.cleanStr(keyword)
        encodedQuery = quote(keyword)
        self.__timber.log('JishoApiService', f'Performing Jisho lookup for \"{keyword}\"... ({encodedQuery=})')

        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(
                url = f'https://jisho.org/api/v1/search/words?keyword={encodedQuery}'
            )
        except GenericNetworkException as e:
            self.__timber.log('JishoApiService', f'Encountered network error when fetching Jisho query ({encodedQuery=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'JishoApiService encountered network error when fetching Jisho query ({encodedQuery=}): {e}')

        responseStatusCode = response.getStatusCode()
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('JishoApiService', f'Encountered non-200 HTTP status code when fetching Jisho query ({encodedQuery=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=})')
            raise GenericNetworkException(f'JishoApiService encountered non-200 HTTP status code when fetching Jisho query ({encodedQuery=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=})')

        jishoResponse = await self.__jishoJsonMapper.parseResponse(jsonResponse)

        if jishoResponse is None:
            self.__timber.log('JishoApiService', f'Failed to parse JSON response into JishoResponse instance ({encodedQuery=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({jishoResponse=})')
            raise GenericNetworkException(f'JishoApiService failed to parse JSON resposne into JishoResponse instance ({encodedQuery=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({jishoResponse=})')
        elif jishoResponse.meta.status != 200:
            self.__timber.log('JishoApiService', f'Received JishoResponse with a bad metadata status code ({encodedQuery=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({jishoResponse=})')
            raise GenericNetworkException(f'JishoApiService received JishoResponse with a bad metadata status code ({encodedQuery=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({jishoResponse=})')

        return jishoResponse
