import traceback
from datetime import datetime

from .commodoreSamHelperInterface import CommodoreSamHelperInterface
from ..apiService.commodoreSamApiService import CommodoreSamApiServiceInterface
from ..exceptions import CommodoreSamFailedToGenerateSpeechFileException
from ..models.commodoreSamFileReference import CommodoreSamFileReference
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class CommodoreSamHelper(CommodoreSamHelperInterface):

    def __init__(
        self,
        commodoreSamApiService: CommodoreSamApiServiceInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface
    ):
        if not isinstance(commodoreSamApiService, CommodoreSamApiServiceInterface):
            raise TypeError(f'commodoreSamApiService argument is malformed: \"{commodoreSamApiService}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__commodoreSamApiService: CommodoreSamApiServiceInterface = commodoreSamApiService
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository

    async def generateTts(
        self,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> CommodoreSamFileReference | None:
        if message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not utils.isValidStr(message):
            return None

        try:
            speechFile = await self.__commodoreSamApiService.generateSpeechFile(
                text = message
            )
        except CommodoreSamFailedToGenerateSpeechFileException as e:
            self.__timber.log('CommodoreSamHelper', f'Encountered error when generating speech ({message=}): {e}', e, traceback.format_exc())
            return None

        storeDateTime = datetime.now(self.__timeZoneRepository.getDefault())

        return CommodoreSamFileReference(
            storeDateTime = storeDateTime,
            filePath = speechFile
        )
