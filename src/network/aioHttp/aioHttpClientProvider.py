from asyncio import AbstractEventLoop
from typing import Final

import aiohttp

from .aioHttpCookieJarProvider import AioHttpCookieJarProvider
from .aioHttpHandle import AioHttpHandle
from ..networkClientProvider import NetworkClientProvider
from ..networkClientType import NetworkClientType
from ..networkHandle import NetworkHandle
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class AioHttpClientProvider(NetworkClientProvider):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        cookieJarProvider: AioHttpCookieJarProvider,
        timber: TimberInterface,
        timeoutSeconds: int = 30,
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(cookieJarProvider, AioHttpCookieJarProvider):
            raise TypeError(f'cookieJarProvider argument is malformed: \"{cookieJarProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidInt(timeoutSeconds):
            raise TypeError(f'timeoutSeconds argument is malformed: \"{timeoutSeconds}\"')
        elif timeoutSeconds < 3 or timeoutSeconds > 60:
            raise ValueError(f'timeoutSeconds argument is out of bounds: {timeoutSeconds}')

        self.__eventLoop: Final[AbstractEventLoop] = eventLoop
        self.__cookieJarProvider: Final[AioHttpCookieJarProvider] = cookieJarProvider
        self.__timber: Final[TimberInterface] = timber
        self.__timeoutSeconds: Final[int] = timeoutSeconds

        self.__clientSession: aiohttp.ClientSession | None = None

    async def get(self) -> NetworkHandle:
        clientSession = self.__clientSession

        if clientSession is None:
            clientSession = aiohttp.ClientSession(
                loop = self.__eventLoop,
                cookie_jar = await self.__cookieJarProvider.get(),
                timeout = aiohttp.ClientTimeout(total = self.__timeoutSeconds),
            )

            self.__clientSession = clientSession

        return AioHttpHandle(
            clientSession = clientSession,
            timber = self.__timber,
        )

    @property
    def networkClientType(self) -> NetworkClientType:
        return NetworkClientType.AIOHTTP
