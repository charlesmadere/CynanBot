from abc import ABC, abstractmethod

from aiohttp.abc import AbstractCookieJar


class AioHttpCookieJarProviderInterface(ABC):

    @abstractmethod
    async def get(self) -> AbstractCookieJar:
        pass
