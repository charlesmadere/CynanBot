from typing import Any, Dict, Optional

import aiohttp

from CynanBot.network.aioHttpResponse import AioHttpResponse
from CynanBot.network.exceptions import GenericNetworkException
from CynanBot.network.networkClientType import NetworkClientType
from CynanBot.network.networkHandle import NetworkHandle
from CynanBot.network.networkResponse import NetworkResponse
from CynanBot.timber.timberInterface import TimberInterface


class AioHttpHandle(NetworkHandle):

    def __init__(
        self,
        clientSession: aiohttp.ClientSession,
        timber: TimberInterface
    ):
        if not isinstance(clientSession, aiohttp.ClientSession):
            raise ValueError(f'clientSession argument is malformed: \"{clientSession}\"')
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"

        self.__clientSession: aiohttp.ClientSession = clientSession
        self.__timber: TimberInterface = timber

    async def delete(
        self,
        url: str,
        headers: Optional[Dict[str, Any]] = None
    ) -> NetworkResponse:
        response: Optional[aiohttp.ClientResponse] = None

        try:
            response = await self.__clientSession.delete(
                url = url,
                headers = headers
            )
        except Exception as e:
            self.__timber.log('AioHttpHandle', f'Encountered network error (via {self.getNetworkClientType()}) when trying to HTTP DELETE \"{url}\" with headers \"{headers}\": {e}', e)
            raise GenericNetworkException(f'Encountered network error (via {self.getNetworkClientType()}) when trying to HTTP DELETE \"{url}\" with headers \"{headers}\": {e}')

        if response is None:
            self.__timber.log('AioHttpHandle', f'Received no response (via {self.getNetworkClientType()}) when trying to HTTP DELETE \"{url}\" with headers \"{headers}\"')
            raise GenericNetworkException(f'Received no response (via {self.getNetworkClientType()}) when trying to HTTP DELETE \"{url}\" with headers \"{headers}\"')

        return AioHttpResponse(
            response = response,
            url = url,
            timber = self.__timber
        )

    async def get(
        self,
        url: str,
        headers: Optional[Dict[str, Any]] = None
    ) -> NetworkResponse:
        response: Optional[aiohttp.ClientResponse] = None

        try:
            response = await self.__clientSession.get(
                url = url,
                headers = headers
            )
        except Exception as e:
            self.__timber.log('AioHttpHandle', f'Encountered network error (via {self.getNetworkClientType()}) when trying to HTTP GET \"{url}\" with headers \"{headers}\": {e}', e)
            raise GenericNetworkException(f'Encountered network error (via {self.getNetworkClientType()}) when trying to HTTP GET \"{url}\" with headers \"{headers}\": {e}')

        if response is None:
            self.__timber.log('AioHttpHandle', f'Received no response (via {self.getNetworkClientType()}) when trying to HTTP GET \"{url}\" with headers \"{headers}\"')
            raise GenericNetworkException(f'Received no response (via {self.getNetworkClientType()}) when trying to HTTP GET \"{url}\" with headers \"{headers}\"')

        return AioHttpResponse(
            response = response,
            url = url,
            timber = self.__timber
        )

    def getNetworkClientType(self) -> NetworkClientType:
        return NetworkClientType.AIOHTTP

    async def post(
        self,
        url: str,
        headers: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None
    ) -> NetworkResponse:
        response: Optional[aiohttp.ClientResponse] = None

        try:
            response = await self.__clientSession.post(
                url = url,
                headers = headers,
                json = json
            )
        except Exception as e:
            self.__timber.log('AioHttpHandle', f'Encountered network error (via {self.getNetworkClientType()}) when trying to HTTP POST \"{url}\" with headers \"{headers}\" and json \"{json}\": {e}', e)
            raise GenericNetworkException(f'Encountered network error (via {self.getNetworkClientType()}) when trying to HTTP POST \"{url}\" with headers \"{headers}\" and json \"{json}\": {e}')

        if response is None:
            self.__timber.log('AioHttpHandle', f'Received no response (via {self.getNetworkClientType()}) when trying to HTTP POST \"{url}\" with headers \"{headers}\" and json \"{json}\"')
            raise GenericNetworkException(f'Received no response (via {self.getNetworkClientType()}) when trying to HTTP POST \"{url}\" with headers \"{headers}\" and json \"{json}\"')

        return AioHttpResponse(
            response = response,
            url = url,
            timber = self.__timber
        )
