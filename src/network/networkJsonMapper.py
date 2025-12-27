from typing import Any

from .networkClientType import NetworkClientType
from .networkJsonMapperInterface import NetworkJsonMapperInterface


class NetworkJsonMapper(NetworkJsonMapperInterface):

    def parseClientType(
        self,
        clientType: str | Any | None,
    ) -> NetworkClientType:
        if not isinstance(clientType, str):
            raise TypeError(f'clientType argument is malformed: \"{clientType}\"')

        clientType = clientType.lower()

        match clientType:
            case 'aiohttp': return NetworkClientType.AIOHTTP
            case 'requests': return NetworkClientType.REQUESTS
            case _: raise ValueError(f'Unknown NetworkClientType value: \"{clientType}\"')

    async def parseClientTypeAsync(
        self,
        clientType: str | Any | None,
    ) -> NetworkClientType:
        return self.parseClientType(clientType)

    def serializeClientType(
        self,
        clientType: NetworkClientType,
    ) -> str:
        if not isinstance(clientType, NetworkClientType):
            raise TypeError(f'clientType argument is malformed: \"{clientType}\"')

        match clientType:
            case NetworkClientType.AIOHTTP: return 'aiohttp'
            case NetworkClientType.REQUESTS: return 'requests'
            case _: raise ValueError(f'Unknown NetworkClientType value: \"{clientType}\"')
