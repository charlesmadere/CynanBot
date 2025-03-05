import traceback
from datetime import datetime

from .decTalkHelperInterface import DecTalkHelperInterface
from ..apiService.decTalkApiServiceInterface import DecTalkApiServiceInterface
from ..exceptions import DecTalkFailedToGenerateSpeechFileException
from ..models.decTalkFileReference import DecTalkFileReference
from ..models.decTalkVoice import DecTalkVoice
from ..settings.decTalkSettingsRepositoryInterface import DecTalkSettingsRepositoryInterface
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class DecTalkHelper(DecTalkHelperInterface):

    def __init__(
        self,
        decTalkApiService: DecTalkApiServiceInterface,
        decTalkSettingsRepository: DecTalkSettingsRepositoryInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface
    ):
        if not isinstance(decTalkApiService, DecTalkApiServiceInterface):
            raise TypeError(f'decTalkApiService argument is malformed: \"{decTalkApiService}\"')
        elif not isinstance(decTalkSettingsRepository, DecTalkSettingsRepositoryInterface):
            raise TypeError(f'decTalkSettingsRepository argument is malformed: \"{decTalkSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__decTalkApiService: DecTalkApiServiceInterface = decTalkApiService
        self.__decTalkSettingsRepository: DecTalkSettingsRepositoryInterface = decTalkSettingsRepository
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository

    async def generateTts(
        self,
        voice: DecTalkVoice | None,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> DecTalkFileReference | None:
        if voice is not None and not isinstance(voice, DecTalkVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')
        elif message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not utils.isValidStr(message):
            return None

        if voice is None:
            voice = await self.__decTalkSettingsRepository.getDefaultVoice()

        try:
            speechFile = await self.__decTalkApiService.generateSpeechFile(
                voice = voice,
                text = message
            )
        except DecTalkFailedToGenerateSpeechFileException as e:
            self.__timber.log('DecTalkHelper', f'Encountered error when generating speech ({voice=}) ({message=}): {e}', e, traceback.format_exc())
            return None

        storeDateTime = datetime.now(self.__timeZoneRepository.getDefault())

        return DecTalkFileReference(
            storeDateTime = storeDateTime,
            filePath = speechFile
        )
