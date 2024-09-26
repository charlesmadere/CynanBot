import traceback

from .streamElementsHelperInterface import StreamElementsHelperInterface
from ..apiService.streamElementsApiServiceInterface import StreamElementsApiServiceInterface
from ..parser.streamElementsMessageVoiceParserInterface import StreamElementsMessageVoiceParserInterface
from ..settings.streamElementsSettingsRepositoryInterface import StreamElementsSettingsRepositoryInterface
from ..streamElementsMessageCleaner import StreamElementsMessageCleaner
from ..userKeyRepository.streamElementsUserKeyRepositoryInterface import StreamElementsUserKeyRepositoryInterface
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...timber.timberInterface import TimberInterface


class StreamElementsHelper(StreamElementsHelperInterface):

    def __init__(
        self,
        streamElementsApiService: StreamElementsApiServiceInterface,
        streamElementsMessageCleaner: StreamElementsMessageCleaner,
        streamElementsMessageVoiceParser: StreamElementsMessageVoiceParserInterface,
        streamElementsSettingsRepository: StreamElementsSettingsRepositoryInterface,
        streamElementsUserKeyRepository: StreamElementsUserKeyRepositoryInterface,
        timber: TimberInterface
    ):
        if not isinstance(streamElementsApiService, StreamElementsApiServiceInterface):
            raise TypeError(f'streamElementsApiService argument is malformed: \"{streamElementsApiService}\"')
        elif not isinstance(streamElementsMessageCleaner, StreamElementsMessageCleaner):
            raise TypeError(f'streamElementsMessageCleaner argument is malformed: \"{streamElementsMessageCleaner}\"')
        elif not isinstance(streamElementsMessageVoiceParser, StreamElementsMessageVoiceParserInterface):
            raise TypeError(f'streamElementsMessageVoiceParser argument is malformed: \"{streamElementsMessageVoiceParser}\"')
        elif not isinstance(streamElementsSettingsRepository, StreamElementsSettingsRepositoryInterface):
            raise TypeError(f'streamElementsSettingsRepository argument is malformed: \"{streamElementsSettingsRepository}\"')
        elif not isinstance(streamElementsUserKeyRepository, StreamElementsUserKeyRepositoryInterface):
            raise TypeError(f'streamElementsUserKeyRepository argument is malformed: \"{streamElementsUserKeyRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__streamElementsApiService: StreamElementsApiServiceInterface = streamElementsApiService
        self.__streamElementsMessageCleaner: StreamElementsMessageCleaner = streamElementsMessageCleaner
        self.__streamElementsMessageVoiceParser: StreamElementsMessageVoiceParserInterface = streamElementsMessageVoiceParser
        self.__streamElementsSettingsRepository: StreamElementsSettingsRepositoryInterface = streamElementsSettingsRepository
        self.__streamElementsUserKeyRepository: StreamElementsUserKeyRepositoryInterface = streamElementsUserKeyRepository
        self.__timber: TimberInterface = timber

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

        message = await self.__streamElementsMessageCleaner.clean(message)
        if not utils.isValidStr(message):
            return None

        userKey = await self.__streamElementsUserKeyRepository.get(
            twitchChannelId = twitchChannelId
        )

        if not utils.isValidStr(userKey):
            self.__timber.log('StreamElementsHelper', f'No Stream Elements user key available for this user: ({message=}) ({twitchChannel=}) ({twitchChannelId=}) ({userKey=})')
            return None

        voice = await self.__streamElementsMessageVoiceParser.determineVoiceFromMessage(message)

        if voice is None:
            voice = await self.__streamElementsSettingsRepository.getDefaultVoice()

        try:
            return await self.__streamElementsApiService.getSpeech(
                text = message,
                userKey = userKey,
                voice = voice
            )
        except GenericNetworkException as e:
            self.__timber.log('StreamElementsHelper', f'Encountered network error when fetching speech ({message=}) ({twitchChannel=}) ({twitchChannelId=}) ({userKey=}): {e}', e, traceback.format_exc())
            return None
