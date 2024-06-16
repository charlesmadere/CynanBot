import asyncio
from asyncio import AbstractEventLoop

from CynanBot.jisho.jishoApiService import JishoApiService
from CynanBot.jisho.jishoApiServiceInterface import JishoApiServiceInterface
from CynanBot.jisho.jishoJsonMapper import JishoJsonMapper
from CynanBot.jisho.jishoJsonMapperInterface import JishoJsonMapperInterface
from CynanBot.jisho.jishoPresenter import JishoPresenter
from CynanBot.jisho.jishoPresenterInterface import JishoPresenterInterface
from CynanBot.language.jishoHelper import JishoHelper
from CynanBot.language.jishoHelperInterface import JishoHelperInterface
from CynanBot.network.aioHttpClientProvider import AioHttpClientProvider
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.timber.timberStub import TimberStub

eventLoop: AbstractEventLoop = asyncio.get_event_loop()

timber: TimberInterface = TimberStub()

networkClientProvider: NetworkClientProvider = AioHttpClientProvider(
    eventLoop = eventLoop,
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
