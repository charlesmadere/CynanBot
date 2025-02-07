import traceback

from .ttsMonsterPrivateApiHelperInterface import TtsMonsterPrivateApiHelperInterface
from ..apiService.ttsMonsterPrivateApiServiceInterface import TtsMonsterPrivateApiServiceInterface
from ..keyAndUserIdRepository.ttsMonsterKeyAndUserIdRepositoryInterface import \
    TtsMonsterKeyAndUserIdRepositoryInterface
from ...misc import utils as utils
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

    async def getSpeech(
        self,
        message: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> bytes | None:
        if not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        keyAndUserId = await self.__ttsMonsterKeyAndUserIdRepository.get(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        if keyAndUserId is None:
            self.__timber.log('TtsMonsterPrivateApiHelper', f'The given Twitch channel does not have a TTS Monster key and user ID value available ({message=}) ({twitchChannel=}) ({twitchChannelId=})')
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

        try:
            speechBytes = await self.__ttsMonsterPrivateApiService.fetchGeneratedTts(
                ttsUrl = ttsResponse.data.link
            )
        except GenericNetworkException as e:
            self.__timber.log('TtsMonsterPrivateApiHelper', f'Encountered network error when fetching generated TTS ({message=}) ({twitchChannel=}) ({twitchChannelId=}) ({ttsResponse=}): {e}', e, traceback.format_exc())
            return None

        return speechBytes
