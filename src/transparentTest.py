import asyncio
from asyncio import AbstractEventLoop

from .language.languagesRepository import LanguagesRepository
from .language.languagesRepositoryInterface import LanguagesRepositoryInterface
from .location.timeZoneRepository import TimeZoneRepository
from .location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from .network.aioHttp.aioHttpClientProvider import AioHttpClientProvider
from .network.aioHttp.aioHttpCookieJarProvider import AioHttpCookieJarProvider
from .network.networkClientProvider import NetworkClientProvider
from .timber.timberInterface import TimberInterface
from .timber.timberStub import TimberStub
from .transparent.transparentApiService import TransparentApiService
from .transparent.transparentApiServiceInterface import TransparentApiServiceInterface
from .transparent.transparentXmlMapper import TransparentXmlMapper
from .transparent.transparentXmlMapperInterface import TransparentXmlMapperInterface

eventLoop: AbstractEventLoop = asyncio.new_event_loop()
asyncio.set_event_loop(eventLoop)

timber: TimberInterface = TimberStub()

languagesRepository: LanguagesRepositoryInterface = LanguagesRepository()

timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

transparentXmlMapper: TransparentXmlMapperInterface = TransparentXmlMapper(
    timeZoneRepository = timeZoneRepository
)

aioHttpCookieJarProvider = AioHttpCookieJarProvider(
    eventLoop = eventLoop
)

networkClientProvider: NetworkClientProvider = AioHttpClientProvider(
    eventLoop = eventLoop,
    cookieJarProvider = aioHttpCookieJarProvider,
    timber = timber
)

transparentApiService: TransparentApiServiceInterface = TransparentApiService(
    networkClientProvider = networkClientProvider,
    timber = timber,
    transparentXmlMapper = transparentXmlMapper
)

async def main():
    pass

    targetLanguage = await languagesRepository.requireLanguageForCommand('spanish')

    response = await transparentApiService.fetchWordOfTheDay(
        targetLanguage = targetLanguage
    )

    print(response)


eventLoop.run_until_complete(main())
