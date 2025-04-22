import traceback
from datetime import datetime

from .commodoreSamHelperInterface import CommodoreSamHelperInterface
from ..apiService.commodoreSamApiService import CommodoreSamApiServiceInterface
from ..exceptions import CommodoreSamFailedToGenerateSpeechFileException, CommodoreSamExecutableIsMissingException
from ..models.commodoreSamFileReference import CommodoreSamFileReference
from ..settings.commodoreSamSettingsRepositoryInterface import CommodoreSamSettingsRepositoryInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class CommodoreSamHelper(CommodoreSamHelperInterface):

    def __init__(
        self,
        commodoreSamApiService: CommodoreSamApiServiceInterface,
        commodoreSamSettingsRepository: CommodoreSamSettingsRepositoryInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface
    ):
        if not isinstance(commodoreSamApiService, CommodoreSamApiServiceInterface):
            raise TypeError(f'commodoreSamApiService argument is malformed: \"{commodoreSamApiService}\"')
        elif not isinstance(commodoreSamSettingsRepository, CommodoreSamSettingsRepositoryInterface):
            raise TypeError(f'commodoreSamSettingsRepository argument is malformed: \"{commodoreSamSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__commodoreSamApiService: CommodoreSamApiServiceInterface = commodoreSamApiService
        self.__commodoreSamSettingsRepository: CommodoreSamSettingsRepositoryInterface = commodoreSamSettingsRepository
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository

    async def __createFullMessage(
        self,
        donationPrefix: str | None,
        message: str | None
    ) -> str | None:
        if not await self.__commodoreSamSettingsRepository.useDonationPrefix():
            return message
        elif utils.isValidStr(donationPrefix) and utils.isValidStr(message):
            return f'{donationPrefix} {message}'
        elif utils.isValidStr(donationPrefix):
            return donationPrefix
        elif utils.isValidStr(message):
            return message
        else:
            return None

    async def generateTts(
        self,
        donationPrefix: str | None,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> CommodoreSamFileReference | None:
        if donationPrefix is not None and not isinstance(donationPrefix, str):
            raise TypeError(f'donationPrefix argument is malformed: \"{donationPrefix}\"')
        elif message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not utils.isValidStr(donationPrefix) and not utils.isValidStr(message):
            return None

        fullMessage = await self.__createFullMessage(
            donationPrefix = donationPrefix,
            message = message
        )

        if not utils.isValidStr(fullMessage):
            return None

        try:
            speechFile = await self.__commodoreSamApiService.generateSpeechFile(
                text = fullMessage
            )
        except CommodoreSamExecutableIsMissingException as e:
            self.__timber.log('CommodoreSamHelper', f'Encountered executable file is missing exception when generating speech ({fullMessage=}): {e}', e, traceback.format_exc())
            return None
        except CommodoreSamFailedToGenerateSpeechFileException as e:
            self.__timber.log('CommodoreSamHelper', f'Encountered failure to create speech file exception when generating speech ({fullMessage=}): {e}', e, traceback.format_exc())
            return None

        storeDateTime = datetime.now(self.__timeZoneRepository.getDefault())

        return CommodoreSamFileReference(
            storeDateTime = storeDateTime,
            filePath = speechFile
        )
