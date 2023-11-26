from asyncio import AbstractEventLoop
from typing import Optional

import aiohttp

import CynanBot.misc.utils as utils
from CynanBot.network.aioHttpHandle import AioHttpHandle
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.network.networkClientType import NetworkClientType
from CynanBot.network.networkHandle import NetworkHandle
from CynanBot.timber.timberInterface import TimberInterface


class AioHttpClientProvider(NetworkClientProvider):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        timber: TimberInterface,
        timeoutSeconds: int = 8
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise ValueError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidNum(timeoutSeconds):
            raise ValueError(f'timeoutSeconds argument is malformed: \"{timeoutSeconds}\"')
        elif timeoutSeconds < 2 or timeoutSeconds > 16:
            raise ValueError(f'timeoutSeconds argument is out of bounds: {timeoutSeconds}')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__timber: TimberInterface = timber
        self.__timeoutSeconds: int = timeoutSeconds

        self.__clientSession: Optional[aiohttp.ClientSession] = None

    async def get(self) -> NetworkHandle:
        clientSession = self.__clientSession

        if clientSession is None:
            clientSession = aiohttp.ClientSession(
                loop = self.__eventLoop,
                cookie_jar = aiohttp.DummyCookieJar(),
                timeout = aiohttp.ClientTimeout(total = self.__timeoutSeconds)
            )

            self.__clientSession = clientSession

        return AioHttpHandle(
            clientSession = clientSession,
            timber = self.__timber
        )

    def getNetworkClientType(self) -> NetworkClientType:
        return NetworkClientType.AIOHTTP
