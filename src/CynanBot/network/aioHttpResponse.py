from json import JSONDecodeError
from typing import Any

import aiohttp

import CynanBot.misc.utils as utils
from CynanBot.network.exceptions import NetworkResponseIsClosedException
from CynanBot.network.networkClientType import NetworkClientType
from CynanBot.network.networkResponse import NetworkResponse
from CynanBot.timber.timberInterface import TimberInterface


class AioHttpResponse(NetworkResponse):

    def __init__(
        self,
        response: aiohttp.ClientResponse,
        url: str,
        timber: TimberInterface
    ):
        if not isinstance(response, aiohttp.ClientResponse):
            raise TypeError(f'response argument is malformed: \"{response}\"')
        elif not utils.isValidStr(url):
            raise TypeError(f'url argument is malformed: \"{url}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__response: aiohttp.ClientResponse = response
        self.__url: str = url
        self.__timber: TimberInterface = timber

        self.__isClosed: bool = False

    async def close(self):
        if self.__isClosed:
            return

        self.__isClosed = True
        self.__response.close()

    def getNetworkClientType(self) -> NetworkClientType:
        return NetworkClientType.AIOHTTP

    def getStatusCode(self) -> int:
        self.__requireNotClosed()
        return self.__response.status

    def getUrl(self) -> str:
        return self.__url

    def isClosed(self) -> bool:
        return self.__isClosed

    async def json(self) -> dict[str, Any] | None:
        self.__requireNotClosed()

        try:
            return await self.__response.json()
        except JSONDecodeError as e:
            self.__timber.log('AioHttpResponse', f'Unable to decode response into JSON for url \"{self.__url}\"', e)
            return None

    async def read(self) -> bytes:
        self.__requireNotClosed()
        return await self.__response.read()

    def __requireNotClosed(self):
        if self.__isClosed:
            raise NetworkResponseIsClosedException(f'This response has already been closed! ({self.getNetworkClientType()})')

    def toDictionary(self) -> dict[str, Any]:
        return {
            'isClosed': self.__isClosed,
            'response': self.__response,
            'url': self.__url
        }
