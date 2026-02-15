from typing import Any, Final

import aiohttp

from .aioHttpResponse import AioHttpResponse
from ..exceptions import GenericNetworkException
from ..networkClientType import NetworkClientType
from ..networkHandle import NetworkHandle
from ..networkResponse import NetworkResponse
from ...timber.timberInterface import TimberInterface


class AioHttpHandle(NetworkHandle):

    def __init__(
        self,
        clientSession: aiohttp.ClientSession,
        timber: TimberInterface,
    ):
        if not isinstance(clientSession, aiohttp.ClientSession):
            raise TypeError(f'clientSession argument is malformed: \"{clientSession}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__clientSession: Final[aiohttp.ClientSession] = clientSession
        self.__timber: Final[TimberInterface] = timber

    async def delete(
        self,
        url: str,
        headers: dict[str, Any] | None = None,
    ) -> NetworkResponse:
        response: aiohttp.ClientResponse | None

        try:
            response = await self.__clientSession.delete(
                url = url,
                headers = headers,
            )
        except Exception as e:
            self.__timber.log('AioHttpHandle', f'Encountered network error (via {self.networkClientType}) when trying to HTTP DELETE ({url=}) ({headers=})', e)
            raise GenericNetworkException(f'Encountered network error (via {self.networkClientType}) when trying to HTTP DELETE ({url=}) ({headers=}): {e}')

        if not isinstance(response, aiohttp.ClientResponse):
            self.__timber.log('AioHttpHandle', f'Received no response (via {self.networkClientType}) when trying to HTTP DELETE ({url=}) ({headers=})')
            raise GenericNetworkException(f'Received no response (via {self.networkClientType}) when trying to HTTP DELETE ({url=}) ({headers=})')

        return AioHttpResponse(
            response = response,
            url = url,
            timber = self.__timber,
        )

    async def get(
        self,
        url: str,
        headers: dict[str, Any] | None = None,
    ) -> NetworkResponse:
        response: aiohttp.ClientResponse | None

        try:
            response = await self.__clientSession.get(
                url = url,
                headers = headers,
            )
        except Exception as e:
            self.__timber.log('AioHttpHandle', f'Encountered network error (via {self.networkClientType}) when trying to HTTP GET ({url=}) ({headers=})', e)
            raise GenericNetworkException(f'Encountered network error (via {self.networkClientType}) when trying to HTTP GET ({url=}) ({headers=}): {e}')

        if not isinstance(response, aiohttp.ClientResponse):
            self.__timber.log('AioHttpHandle', f'Received no response (via {self.networkClientType}) when trying to HTTP GET ({url=}) ({headers=})')
            raise GenericNetworkException(f'Received no response (via {self.networkClientType}) when trying to HTTP GET ({url=}) ({headers=})')

        return AioHttpResponse(
            response = response,
            url = url,
            timber = self.__timber,
        )

    @property
    def networkClientType(self) -> NetworkClientType:
        return NetworkClientType.AIOHTTP

    async def post(
        self,
        url: str,
        headers: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> NetworkResponse:
        response: aiohttp.ClientResponse | None

        try:
            response = await self.__clientSession.post(
                url = url,
                headers = headers,
                json = json,
            )
        except Exception as e:
            self.__timber.log('AioHttpHandle', f'Encountered network error (via {self.networkClientType}) when trying to HTTP POST ({url=}) ({headers=}) ({json=})', e)
            raise GenericNetworkException(f'Encountered network error (via {self.networkClientType}) when trying to HTTP POST ({url=}) ({headers=}) ({json=}): {e}')

        if not isinstance(response, aiohttp.ClientResponse):
            self.__timber.log('AioHttpHandle', f'Received no response (via {self.networkClientType}) when trying to HTTP POST ({url=}) ({headers=}) ({json=})')
            raise GenericNetworkException(f'Received no response (via {self.networkClientType}) when trying to HTTP POST ({url=}) ({headers=}) ({json=})')

        return AioHttpResponse(
            response = response,
            url = url,
            timber = self.__timber,
        )
