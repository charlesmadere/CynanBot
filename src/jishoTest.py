import asyncio
from asyncio import AbstractEventLoop
from typing import Final

from src.jisho.jishoApiService import JishoApiService
from src.jisho.jishoApiServiceInterface import JishoApiServiceInterface
from src.jisho.jishoJsonMapper import JishoJsonMapper
from src.jisho.jishoJsonMapperInterface import JishoJsonMapperInterface
from src.jisho.jishoPresenter import JishoPresenter
from src.jisho.jishoPresenterInterface import JishoPresenterInterface
from src.language.jishoHelper import JishoHelper
from src.language.jishoHelperInterface import JishoHelperInterface
from src.network.aioHttp.aioHttpClientProvider import AioHttpClientProvider
from src.network.aioHttp.aioHttpCookieJarProvider import AioHttpCookieJarProvider
from src.network.networkClientProvider import NetworkClientProvider
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub

eventLoop: Final[AbstractEventLoop] = asyncio.new_event_loop()
asyncio.set_event_loop(eventLoop)

timber: Final[TimberInterface] = TimberStub()

aioHttpCookieJarProvider = AioHttpCookieJarProvider(
    eventLoop = eventLoop
)

networkClientProvider: Final[NetworkClientProvider] = AioHttpClientProvider(
    eventLoop = eventLoop,
    cookieJarProvider = aioHttpCookieJarProvider,
    timber = timber,
)

jishoJsonMapper: Final[JishoJsonMapperInterface] = JishoJsonMapper(
    timber = timber,
)

jishoApiService: Final[JishoApiServiceInterface] = JishoApiService(
    jishoJsonMapper = jishoJsonMapper,
    networkClientProvider = networkClientProvider,
    timber = timber,
)

jishoPresenter: Final[JishoPresenterInterface] = JishoPresenter()

jishoHelper: Final[JishoHelperInterface] = JishoHelper(
    jishoApiService = jishoApiService,
    jishoPresenter = jishoPresenter,
    timber = timber,
)

async def main():
    pass

    results = await jishoHelper.search('今日は')

    for result in results:
        print(result)

    pass

eventLoop.run_until_complete(main())
