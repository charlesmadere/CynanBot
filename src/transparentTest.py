import asyncio
from asyncio import AbstractEventLoop

from CynanBot.language.languagesRepository import LanguagesRepository
from CynanBot.language.languagesRepositoryInterface import \
    LanguagesRepositoryInterface
from CynanBot.location.timeZoneRepository import TimeZoneRepository
from CynanBot.location.timeZoneRepositoryInterface import \
    TimeZoneRepositoryInterface
from CynanBot.network.aioHttpClientProvider import AioHttpClientProvider
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.timber.timberStub import TimberStub
from CynanBot.transparent.transparentApiService import TransparentApiService
from CynanBot.transparent.transparentApiServiceInterface import \
    TransparentApiServiceInterface
from CynanBot.transparent.transparentXmlMapper import TransparentXmlMapper
from CynanBot.transparent.transparentXmlMapperInterface import \
    TransparentXmlMapperInterface

timber: TimberInterface = TimberStub()

languagesRepository: LanguagesRepositoryInterface = LanguagesRepository()

timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

transparentXmlMapper: TransparentXmlMapperInterface = TransparentXmlMapper(
    timeZoneRepository = timeZoneRepository
)

eventLoop: AbstractEventLoop = asyncio.get_event_loop()

networkClientProvider: NetworkClientProvider = AioHttpClientProvider(
    eventLoop = eventLoop,
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
