import asyncio
from asyncio import AbstractEventLoop

from jisho.jishoApiService import JishoApiService
from jisho.jishoApiServiceInterface import JishoApiServiceInterface
from jisho.jishoJsonMapper import JishoJsonMapper
from jisho.jishoJsonMapperInterface import JishoJsonMapperInterface
from jisho.jishoPresenter import JishoPresenter
from jisho.jishoPresenterInterface import JishoPresenterInterface
from language.jishoHelper import JishoHelper
from language.jishoHelperInterface import JishoHelperInterface
from network.aioHttpClientProvider import AioHttpClientProvider
from network.networkClientProvider import NetworkClientProvider
from network.aioHttp.aioHttpCookieJarProvider import AioHttpCookieJarProvider
from timber.timberInterface import TimberInterface
from timber.timberStub import TimberStub

eventLoop: AbstractEventLoop = asyncio.get_event_loop()

timber: TimberInterface = TimberStub()

aioHttpCookieJarProvider = AioHttpCookieJarProvider(
    eventLoop = eventLoop
)

networkClientProvider: NetworkClientProvider = AioHttpClientProvider(
    eventLoop = eventLoop,
    cookieJarProvider = aioHttpCookieJarProvider,
    timber = timber
)

jishoJsonMapper: JishoJsonMapperInterface = JishoJsonMapper(
    timber = timber
)

jishoApiService: JishoApiServiceInterface = JishoApiService(
    jishoJsonMapper = jishoJsonMapper,
    networkClientProvider = networkClientProvider,
    timber = timber
)

jishoPresenter: JishoPresenterInterface = JishoPresenter()

jishoHelper: JishoHelperInterface = JishoHelper(
    jishoApiService = jishoApiService,
    jishoPresenter = jishoPresenter,
    timber = timber
)

async def main():
    pass

    results = await jishoHelper.search('今日は')

    for result in results:
        print(result)

    pass

eventLoop.run_until_complete(main())
