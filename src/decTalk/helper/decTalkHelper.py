import traceback
from datetime import datetime
from typing import Final

from .decTalkHelperInterface import DecTalkHelperInterface
from ..apiService.decTalkApiServiceInterface import DecTalkApiServiceInterface
from ..exceptions import DecTalkFailedToGenerateSpeechFileException, DecTalkExecutableIsMissingException
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
        timeZoneRepository: TimeZoneRepositoryInterface,
    ):
        if not isinstance(decTalkApiService, DecTalkApiServiceInterface):
            raise TypeError(f'decTalkApiService argument is malformed: \"{decTalkApiService}\"')
        elif not isinstance(decTalkSettingsRepository, DecTalkSettingsRepositoryInterface):
            raise TypeError(f'decTalkSettingsRepository argument is malformed: \"{decTalkSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__decTalkApiService: Final[DecTalkApiServiceInterface] = decTalkApiService
        self.__decTalkSettingsRepository: Final[DecTalkSettingsRepositoryInterface] = decTalkSettingsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository

    async def __createFullMessage(
        self,
        donationPrefix: str | None,
        message: str | None,
    ) -> str | None:
        if not await self.__decTalkSettingsRepository.useDonationPrefix():
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
        voice: DecTalkVoice | None,
        donationPrefix: str | None,
        message: str | None,
        twitchChannelId: str,
    ) -> DecTalkFileReference | None:
        if voice is not None and not isinstance(voice, DecTalkVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')
        elif donationPrefix is not None and not isinstance(donationPrefix, str):
            raise TypeError(f'donationPrefix argument is malformed: \"{donationPrefix}\"')
        elif message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not utils.isValidStr(donationPrefix) and not utils.isValidStr(message):
            return None

        if voice is None:
            voice = await self.__decTalkSettingsRepository.getDefaultVoice()

        fullMessage = await self.__createFullMessage(
            donationPrefix = donationPrefix,
            message = message,
        )

        if not utils.isValidStr(fullMessage):
            return None

        try:
            speechFile = await self.__decTalkApiService.generateSpeechFile(
                voice = voice,
                text = fullMessage,
            )
        except DecTalkExecutableIsMissingException as e:
            self.__timber.log('DecTalkHelper', f'Encountered executable file is missing exception when generating speech ({voice=}) ({fullMessage=})', e, traceback.format_exc())
            return None
        except DecTalkFailedToGenerateSpeechFileException as e:
            self.__timber.log('DecTalkHelper', f'Encountered failure to create speech file exception when generating speech ({voice=}) ({fullMessage=})', e, traceback.format_exc())
            return None

        storeDateTime = datetime.now(self.__timeZoneRepository.getDefault())

        return DecTalkFileReference(
            storeDateTime = storeDateTime,
            filePath = speechFile,
        )
