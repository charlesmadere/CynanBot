import traceback
from datetime import datetime, timedelta

from .ttsMonsterStreamerVoicesCache import TtsMonsterStreamerVoicesCache
from .ttsMonsterStreamerVoicesRepositoryInterface import TtsMonsterStreamerVoicesRepositoryInterface
from ..apiService.ttsMonsterApiServiceInterface import TtsMonsterApiServiceInterface
from ..apiTokens.ttsMonsterApiTokensRepositoryInterface import TtsMonsterApiTokensRepositoryInterface
from ..models.ttsMonsterVoice import TtsMonsterVoice
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...timber.timberInterface import TimberInterface


class TtsMonsterStreamerVoicesRepository(TtsMonsterStreamerVoicesRepositoryInterface):

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        ttsMonsterApiService: TtsMonsterApiServiceInterface,
        ttsMonsterApiTokensRepository: TtsMonsterApiTokensRepositoryInterface,
        cacheTimeToLive: timedelta(hours = 3)
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(ttsMonsterApiTokensRepository, TtsMonsterApiTokensRepositoryInterface):
            raise TypeError(f'ttsMonsterApiTokensRepository argument is malformed: \"{ttsMonsterApiTokensRepository}\"')
        elif not isinstance(cacheTimeToLive, timedelta):
            raise TypeError(f'cacheTimeToLive argument is malformed: \"{cacheTimeToLive}\"')

        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__ttsMonsterApiService: TtsMonsterApiServiceInterface = ttsMonsterApiService
        self.__ttsMonsterApiTokensRepository: TtsMonsterApiTokensRepositoryInterface = ttsMonsterApiTokensRepository
        self.__cacheTimeToLive: timedelta = cacheTimeToLive

        self.__cache: dict[str, TtsMonsterStreamerVoicesCache | None] = dict()

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('TtsMonsterStreamerVoicesRepository', f'Caches cleared')

    async def fetchVoices(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> frozenset[TtsMonsterVoice]:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        voicesCache = self.__cache[twitchChannelId]
        now = datetime.now(self.__timeZoneRepository.getDefault())

        if voicesCache is not None and voicesCache.expirationDateTime >= now:
            return voicesCache.voices

        allVoices = await self.__fetchVoicesFromTtsMonsterApi(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        voicesCache = TtsMonsterStreamerVoicesCache(
            expirationDateTime = now + self.__cacheTimeToLive,
            voices = allVoices,
            twitchChannelId = twitchChannelId
        )

        self.__cache[twitchChannelId] = voicesCache
        return allVoices

    async def __fetchVoicesFromTtsMonsterApi(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> frozenset[TtsMonsterVoice]:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        apiToken = await self.__ttsMonsterApiTokensRepository.get(twitchChannelId = twitchChannelId)
        if not utils.isValidStr(apiToken):
            self.__timber.log('TtsMonsterStreamerVoicesRepository', f'Can\'t fetch TTS Monster voices as no API token is available ({twitchChannel=}) ({twitchChannelId=}) ({apiToken=})')
            return frozenset()

        try:
            voicesResponse = await self.__ttsMonsterApiService.getVoices(
                apiToken = apiToken
            )
        except GenericNetworkException as e:
            self.__timber.log('TtsMonsterStreamerVoicesRepository', f'Encountered network exception when fetching TTS Monster voices ({twitchChannel=}) (({twitchChannelId=}): {e}', e, traceback.format_exc())
            return frozenset()

        voices: set[TtsMonsterVoice] = set()

        for voice in voicesResponse.voices:
            voices.add(voice)

        for customVoice in voicesResponse.customVoices:
            voices.add(customVoice)

        return frozenset(voices)
