import traceback
from typing import Final

from .ttsMonsterPrivateApiHelperInterface import TtsMonsterPrivateApiHelperInterface
from ..apiService.ttsMonsterPrivateApiServiceInterface import TtsMonsterPrivateApiServiceInterface
from ..tokens.ttsMonsterTokensRepositoryInterface import TtsMonsterTokensRepositoryInterface
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...timber.timberInterface import TimberInterface


class TtsMonsterPrivateApiHelper(TtsMonsterPrivateApiHelperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        ttsMonsterPrivateApiService: TtsMonsterPrivateApiServiceInterface,
        ttsMonsterTokensRepository: TtsMonsterTokensRepositoryInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsMonsterPrivateApiService, TtsMonsterPrivateApiServiceInterface):
            raise TypeError(f'ttsMonsterPrivateApiService argument is malformed: \"{ttsMonsterPrivateApiService}\"')
        elif not isinstance(ttsMonsterTokensRepository, TtsMonsterTokensRepositoryInterface):
            raise TypeError(f'ttsMonsterTokensRepository argument is malformed: \"{ttsMonsterTokensRepository}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__ttsMonsterPrivateApiService: Final[TtsMonsterPrivateApiServiceInterface] = ttsMonsterPrivateApiService
        self.__ttsMonsterTokensRepository: Final[TtsMonsterTokensRepositoryInterface] = ttsMonsterTokensRepository

    async def getSpeech(
        self,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> bytes | None:
        if message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not utils.isValidStr(message):
            return None

        tokens = await self.__ttsMonsterTokensRepository.get(
            twitchChannelId = twitchChannelId
        )

        if tokens is None:
            self.__timber.log('TtsMonsterPrivateApiHelper', f'The given Twitch channel does not have any TTS Monster tokens available ({message=}) ({twitchChannel=}) ({twitchChannelId=}) ({tokens=})')
            return None

        try:
            ttsResponse = await self.__ttsMonsterPrivateApiService.generateTts(
                key = tokens.key,
                message = message,
                userId = tokens.userId,
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
