from dataclasses import dataclass

from .ttsMonsterHelperInterface import TtsMonsterHelperInterface
from .ttsMonsterPrivateApiHelperInterface import TtsMonsterPrivateApiHelperInterface
from ..apiService.ttsMonsterApiServiceInterface import TtsMonsterApiServiceInterface
from ..messageToVoicesHelper.ttsMonsterMessageToVoicePair import TtsMonsterMessageToVoicePair
from ..settings.ttsMonsterSettingsRepositoryInterface import TtsMonsterSettingsRepositoryInterface
from ...glacialTtsStorage.helper.glacialTtsFileRetrieverInterface import GlacialTtsFileRetrieverInterface
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...timber.timberInterface import TimberInterface
from ...tts.ttsProvider import TtsProvider


class TtsMonsterHelper(TtsMonsterHelperInterface):

    @dataclass(frozen = True)
    class TtsRequestEntry:
        index: int
        messageToVoicePair: TtsMonsterMessageToVoicePair

    @dataclass(frozen = True)
    class TtsResponseEntry:
        characterUsage: int | None
        index: int
        url: str

    def __init__(
        self,
        glacialTtsFileRetriever: GlacialTtsFileRetrieverInterface,
        timber: TimberInterface,
        ttsMonsterApiService: TtsMonsterApiServiceInterface,
        ttsMonsterPrivateApiHelper: TtsMonsterPrivateApiHelperInterface,
        ttsMonsterSettingsRepository: TtsMonsterSettingsRepositoryInterface
    ):
        if not isinstance(glacialTtsFileRetriever, GlacialTtsFileRetrieverInterface):
            raise TypeError(f'glacialTtsFileRetriever argument is malformed: \"{glacialTtsFileRetriever}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsMonsterApiService, TtsMonsterApiServiceInterface):
            raise TypeError(f'ttsMonsterApiService argument is malformed: \"{ttsMonsterApiService}\"')
        elif not isinstance(ttsMonsterPrivateApiHelper, TtsMonsterPrivateApiHelperInterface):
            raise TypeError(f'ttsMonsterPrivateApiHelper argument is malformed: \"{ttsMonsterPrivateApiHelper}\"')
        elif not isinstance(ttsMonsterSettingsRepository, TtsMonsterSettingsRepositoryInterface):
            raise TypeError(f'ttsMonsterSettingsRepository argument is malformed: \"{ttsMonsterSettingsRepository}\"')

        self.__glacialTtsFileRetriever: GlacialTtsFileRetrieverInterface = glacialTtsFileRetriever
        self.__timber: TimberInterface = timber
        self.__ttsMonsterApiService: TtsMonsterApiServiceInterface = ttsMonsterApiService
        self.__ttsMonsterPrivateApiHelper: TtsMonsterPrivateApiHelperInterface = ttsMonsterPrivateApiHelper
        self.__ttsMonsterSettingsRepository: TtsMonsterSettingsRepositoryInterface = ttsMonsterSettingsRepository

    async def generateTts(
        self,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> str | None:
        if message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not utils.isValidStr(message):
            return None

        glacialFile = await self.__glacialTtsFileRetriever.findFile(
            message = message,
            provider = TtsProvider.TTS_MONSTER
        )

        if glacialFile is not None:
            return glacialFile.filePath

        ttsMonsterUrls = await self.__ttsMonsterPrivateApiHelper.generateTts(
            message = message,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        if ttsMonsterUrls is None or len(ttsMonsterUrls.urls) == 0:
            return None

        try:
            speechBytes = await self.__ttsMonsterApiService.fetchGeneratedTts(
                ttsUrl = ttsMonsterUrls.urls[0]
            )
        except GenericNetworkException as e:
            return None

        # TODO
        return None
