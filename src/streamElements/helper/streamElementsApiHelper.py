import traceback
from typing import Final

from .streamElementsApiHelperInterface import StreamElementsApiHelperInterface
from ..apiService.streamElementsApiServiceInterface import StreamElementsApiServiceInterface
from ..models.streamElementsVoice import StreamElementsVoice
from ..userKeyRepository.streamElementsUserKeyRepositoryInterface import StreamElementsUserKeyRepositoryInterface
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...timber.timberInterface import TimberInterface


class StreamElementsApiHelper(StreamElementsApiHelperInterface):

    def __init__(
        self,
        streamElementsApiService: StreamElementsApiServiceInterface,
        streamElementsUserKeyRepository: StreamElementsUserKeyRepositoryInterface,
        timber: TimberInterface,
    ):
        if not isinstance(streamElementsApiService, StreamElementsApiServiceInterface):
            raise TypeError(f'streamElementsApiService argument is malformed: \"{streamElementsApiService}\"')
        elif not isinstance(streamElementsUserKeyRepository, StreamElementsUserKeyRepositoryInterface):
            raise TypeError(f'streamElementsUserKeyRepository argument is malformed: \"{streamElementsUserKeyRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__streamElementsApiService: Final[StreamElementsApiServiceInterface] = streamElementsApiService
        self.__streamElementsUserKeyRepository: Final[StreamElementsUserKeyRepositoryInterface] = streamElementsUserKeyRepository
        self.__timber: Final[TimberInterface] = timber

    async def getSpeech(
        self,
        message: str | None,
        twitchChannelId: str,
        voice: StreamElementsVoice,
    ) -> bytes | None:
        if message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(voice, StreamElementsVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        if not utils.isValidStr(message):
            return None

        userKey = await self.__streamElementsUserKeyRepository.get(
            twitchChannelId = twitchChannelId,
        )

        if not utils.isValidStr(userKey):
            self.__timber.log('StreamElementsApiHelper', f'No Stream Elements user key available for this user: ({message=}) ({twitchChannelId=}) ({userKey=})')
            return None

        try:
            return await self.__streamElementsApiService.getSpeech(
                text = message,
                userKey = userKey,
                voice = voice,
            )
        except GenericNetworkException as e:
            self.__timber.log('StreamElementsApiHelper', f'Encountered network error when fetching speech ({message=}) ({twitchChannelId=}) ({userKey=})', e, traceback.format_exc())
            return None
