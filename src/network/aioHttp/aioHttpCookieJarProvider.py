from asyncio import AbstractEventLoop
from typing import Final

from aiohttp import DummyCookieJar
from aiohttp.abc import AbstractCookieJar


class AioHttpCookieJarProvider:

    def __init__(self, eventLoop: AbstractEventLoop):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')

        self.__eventLoop: Final[AbstractEventLoop] = eventLoop

        self.__cookieJar: AbstractCookieJar | None = None

    async def get(self) -> AbstractCookieJar:
        cookieJar = self.__cookieJar

        if cookieJar is None:
            cookieJar = DummyCookieJar(
                loop = self.__eventLoop,
            )

            self.__cookieJar = cookieJar

        return cookieJar
