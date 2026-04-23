import asyncio
from asyncio import AbstractEventLoop
from typing import Final

from src.ecco.eccoApiService import EccoApiService
from src.ecco.eccoApiServiceInterface import EccoApiServiceInterface
from src.ecco.eccoConstants import EccoConstants
from src.ecco.eccoHelper import EccoHelper
from src.ecco.eccoHelperInterface import EccoHelperInterface
from src.ecco.eccoResponseParser import EccoResponseParser
from src.ecco.eccoResponseParserInterface import EccoResponseParserInterface
from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.misc.backgroundTaskHelper import BackgroundTaskHelper
from src.misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from src.network.networkClientProvider import NetworkClientProvider
from src.network.requests.requestsClientProvider import RequestsClientProvider
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub

eventLoop: Final[AbstractEventLoop] = asyncio.new_event_loop()
asyncio.set_event_loop(eventLoop)

backgroundTaskHelper: Final[BackgroundTaskHelperInterface] = BackgroundTaskHelper(
    eventLoop = eventLoop,
)

timber: Final[TimberInterface] = TimberStub()

timeZoneRepository: Final[TimeZoneRepositoryInterface] = TimeZoneRepository()

eccoConstants: Final[EccoConstants] = EccoConstants()

eccoResponseParser: Final[EccoResponseParserInterface] = EccoResponseParser(
    eccoConstants = eccoConstants,
    timber = timber,
)

networkClientProvider: Final[NetworkClientProvider] = RequestsClientProvider(
    timber = timber,
)

eccoApiService: Final[EccoApiServiceInterface] = EccoApiService(
    eccoConstants = eccoConstants,
    eccoResponseParser = eccoResponseParser,
    networkClientProvider = networkClientProvider,
    timber = timber,
)

eccoHelper: Final[EccoHelperInterface] = EccoHelper(
    eccoApiService = eccoApiService,
    timber = timber,
    timeZoneRepository = timeZoneRepository,
)

async def main():
    pass

    eccoTimeRemaining = await eccoHelper.fetchEccoTimeRemaining()
    print(f'{eccoTimeRemaining=}')

    pass

eventLoop.run_until_complete(main())
