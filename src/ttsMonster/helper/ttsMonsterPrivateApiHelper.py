import traceback

from frozenlist import FrozenList

from .ttsMonsterPrivateApiHelperInterface import TtsMonsterPrivateApiHelperInterface
from ..apiService.ttsMonsterPrivateApiServiceInterface import TtsMonsterPrivateApiServiceInterface
from ..keyAndUserIdRepository.ttsMonsterKeyAndUserIdRepositoryInterface import \
    TtsMonsterKeyAndUserIdRepositoryInterface
from ..models.ttsMonsterUrls import TtsMonsterUrls
from ...network.exceptions import GenericNetworkException
from ...timber.timberInterface import TimberInterface


class TtsMonsterPrivateApiHelper(TtsMonsterPrivateApiHelperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        ttsMonsterKeyAndUserIdRepository: TtsMonsterKeyAndUserIdRepositoryInterface,
        ttsMonsterPrivateApiService: TtsMonsterPrivateApiServiceInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsMonsterKeyAndUserIdRepository, TtsMonsterKeyAndUserIdRepositoryInterface):
            raise TypeError(f'ttsMonsterKeyAndUserIdRepository argument is malformed: \"{ttsMonsterKeyAndUserIdRepository}\"')
        elif not isinstance(ttsMonsterPrivateApiService, TtsMonsterPrivateApiServiceInterface):
            raise TypeError(f'ttsMonsterPrivateApiService argument is malformed: \"{ttsMonsterPrivateApiService}\"')

        self.__timber: TimberInterface = timber
        self.__ttsMonsterKeyAndUserIdRepository: TtsMonsterKeyAndUserIdRepositoryInterface = ttsMonsterKeyAndUserIdRepository
        self.__ttsMonsterPrivateApiService: TtsMonsterPrivateApiServiceInterface = ttsMonsterPrivateApiService

    async def generateTts(
        self,
        message: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> TtsMonsterUrls | None:
        keyAndUserId = await self.__ttsMonsterKeyAndUserIdRepository.get(
            twitchChannel = twitchChannel
        )

        if keyAndUserId is None:
            self.__timber.log('TtsMonsterPrivateApiHelper', f'The given Twitch channel does not have a TTS Monster key and user ID value available ({twitchChannel=}) ({twitchChannelId=})')
            return None

        try:
            ttsResponse = await self.__ttsMonsterPrivateApiService.generateTts(
                key = keyAndUserId.key,
                message = message,
                userId = keyAndUserId.userId
            )
        except GenericNetworkException as e:
            self.__timber.log('TtsMonsterPrivateApiHelper', f'Encountered network error when generating TTS ({message=}) ({twitchChannel=}) ({twitchChannelId=}): {e}', e, traceback.format_exc())
            return None

        urls: FrozenList[str] = FrozenList()
        urls.append(ttsResponse.data.link)
        urls.freeze()

        return TtsMonsterUrls(
            urls = urls,
            characterAllowance = None,
            characterUsage = None
        )
