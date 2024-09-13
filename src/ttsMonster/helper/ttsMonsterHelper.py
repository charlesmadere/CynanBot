import asyncio
import traceback
from dataclasses import dataclass
from typing import Any, Coroutine

from frozenlist import FrozenList

from .ttsMonsterHelperInterface import TtsMonsterHelperInterface
from ..apiService.ttsMonsterApiServiceInterface import TtsMonsterApiServiceInterface
from ..apiTokens.ttsMonsterApiTokensRepositoryInterface import TtsMonsterApiTokensRepositoryInterface
from ..messageToVoicesHelper.ttsMonsterMessageToVoicePair import TtsMonsterMessageToVoicePair
from ..messageToVoicesHelper.ttsMonsterMessageToVoicesHelperInterface import TtsMonsterMessageToVoicesHelperInterface
from ..models.ttsMonsterTtsRequest import TtsMonsterTtsRequest
from ..models.ttsMonsterUrls import TtsMonsterUrls
from ..settings.ttsMonsterSettingsRepositoryInterface import TtsMonsterSettingsRepositoryInterface
from ..streamerVoices.ttsMonsterStreamerVoicesRepositoryInterface import TtsMonsterStreamerVoicesRepositoryInterface
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...timber.timberInterface import TimberInterface


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
        timber: TimberInterface,
        ttsMonsterApiService: TtsMonsterApiServiceInterface,
        ttsMonsterApiTokensRepository: TtsMonsterApiTokensRepositoryInterface,
        ttsMonsterMessageToVoicesHelper: TtsMonsterMessageToVoicesHelperInterface,
        ttsMonsterSettingsRepository: TtsMonsterSettingsRepositoryInterface,
        ttsMonsterStreamerVoicesRepository: TtsMonsterStreamerVoicesRepositoryInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsMonsterApiService, TtsMonsterApiServiceInterface):
            raise TypeError(f'ttsMonsterApiService argument is malformed: \"{ttsMonsterApiService}\"')
        elif not isinstance(ttsMonsterApiTokensRepository, TtsMonsterApiTokensRepositoryInterface):
            raise TypeError(f'ttsMonsterApiTokensRepository argument is malformed: \"{ttsMonsterApiTokensRepository}\"')
        elif not isinstance(ttsMonsterMessageToVoicesHelper, TtsMonsterMessageToVoicesHelperInterface):
            raise TypeError(f'ttsMonsterMessageToVoicesHelper argument is malformed: \"{ttsMonsterMessageToVoicesHelper}\"')
        elif not isinstance(ttsMonsterSettingsRepository, TtsMonsterSettingsRepositoryInterface):
            raise TypeError(f'ttsMonsterSettingsRepository argument is malformed: \"{ttsMonsterSettingsRepository}\"')
        elif not isinstance(ttsMonsterStreamerVoicesRepository, TtsMonsterStreamerVoicesRepositoryInterface):
            raise TypeError(f'ttsMonsterStreamerVoicesRepository argument is malformed: \"{ttsMonsterStreamerVoicesRepository}\"')

        self.__timber: TimberInterface = timber
        self.__ttsMonsterApiService: TtsMonsterApiServiceInterface = ttsMonsterApiService
        self.__ttsMonsterApiTokensRepository: TtsMonsterApiTokensRepositoryInterface = ttsMonsterApiTokensRepository
        self.__ttsMonsterMessageToVoicesHelper: TtsMonsterMessageToVoicesHelperInterface = ttsMonsterMessageToVoicesHelper
        self.__ttsMonsterSettingsRepository: TtsMonsterSettingsRepositoryInterface = ttsMonsterSettingsRepository
        self.__ttsMonsterStreamerVoicesRepository: TtsMonsterStreamerVoicesRepositoryInterface = ttsMonsterStreamerVoicesRepository

    async def __fetchTtsUrl(
        self,
        index: int,
        apiToken: str,
        message: str,
        voiceId: str
    ) -> TtsResponseEntry:
        if not utils.isValidInt(index):
            raise TypeError(f'index argument is malformed: \"{index}\"')
        elif not utils.isValidStr(apiToken):
            raise TypeError(f'apiToken argument is malformed: \"{apiToken}\"')
        elif not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(voiceId):
            raise TypeError(f'voiceId argument is malformed: \"{voiceId}\"')

        ttsRequest = TtsMonsterTtsRequest(
            returnUsage = await self.__ttsMonsterSettingsRepository.isReturnCharacterUsageEnabled(),
            message = message,
            voiceId = voiceId
        )

        ttsResponse = await self.__ttsMonsterApiService.generateTts(
            apiToken = apiToken,
            request = ttsRequest
        )

        return TtsMonsterHelper.TtsResponseEntry(
            characterUsage = ttsResponse.characterUsage,
            index = index,
            url = ttsResponse.url
        )

    async def __generateMultiVoiceTts(
        self,
        messages: FrozenList[TtsMonsterMessageToVoicePair],
        apiToken: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> TtsMonsterUrls | None:
        ttsRequests: list[TtsMonsterHelper.TtsRequestEntry] = list()

        for index, messageToVoicePair in enumerate(messages):
            ttsRequests.append(TtsMonsterHelper.TtsRequestEntry(
                index = index,
                messageToVoicePair = messageToVoicePair
            ))

        ttsResponseCoroutines: list[Coroutine[Any, Any, TtsMonsterHelper.TtsResponseEntry]] = list()

        for ttsRequest in ttsRequests:
            ttsResponseCoroutines.append(self.__fetchTtsUrl(
                index = ttsRequest.index,
                apiToken = apiToken,
                message = ttsRequest.messageToVoicePair.message,
                voiceId = ttsRequest.messageToVoicePair.voice.voiceId
            ))

        ttsResponses: list[TtsMonsterHelper.TtsResponseEntry] = list()

        try:
            ttsResponses.extend(await asyncio.gather(*ttsResponseCoroutines, return_exceptions = True))
        except GenericNetworkException as e:
            self.__timber.log('TtsMonsterHelper', f'Encountered network error when generating TTS from TTS Monster ({apiToken=}) ({twitchChannel=}) ({twitchChannelId=}): {e}', e, traceback.format_exc())
            return None
        except Exception as e:
            self.__timber.log('TtsMonsterHelper', f'Encountered unknown error when generating TTS from TTS Monster ({apiToken=}) ({twitchChannel=}) ({twitchChannelId=}): {e}', e, traceback.format_exc())
            return None

        if len(ttsResponses) == 0:
            self.__timber.log('TtsMonsterHelper', f'Encountered unknown issue when generating TTS from TTS Monster ({apiToken=}) ({twitchChannel=}) ({twitchChannelId=})')
            return None

        ttsResponses.sort(key = lambda element: element.index)
        ttsUrls: list[str] = list()

        for ttsResponse in ttsResponses:
            ttsUrls.append(ttsResponse.url)

        frozenTtsUrls: FrozenList[str] = FrozenList(ttsUrls)
        frozenTtsUrls.freeze()

        characterUsage: int | None = None
        for ttsResponse in ttsResponses:
            if not utils.isValidInt(ttsResponse.characterUsage):
                continue
            elif characterUsage is None or ttsResponse.characterUsage > characterUsage:
                characterUsage = ttsResponse.characterUsage

        return TtsMonsterUrls(
            urls = frozenTtsUrls,
            characterUsage = characterUsage
        )

    async def __generateSingleVoiceTts(
        self,
        apiToken: str,
        message: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> TtsMonsterUrls | None:
        defaultVoice = await self.__ttsMonsterSettingsRepository.getDefaultVoice()

        try:
            ttsResponse = await self.__fetchTtsUrl(
                index = 0,
                apiToken = apiToken,
                message = message,
                voiceId = defaultVoice.voiceId
            )
        except GenericNetworkException as e:
            self.__timber.log('TtsMonsterHelper', f'Encountered network error when generating TTS from TTS Monster ({apiToken=}) ({twitchChannel=}) ({twitchChannelId=}): {e}', e, traceback.format_exc())
            return None

        ttsUrls: FrozenList[str] = FrozenList()
        ttsUrls.append(ttsResponse.url)
        ttsUrls.freeze()

        return TtsMonsterUrls(
            urls = ttsUrls,
            characterUsage = ttsResponse.characterUsage
        )

    async def generateTts(
        self,
        message: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> TtsMonsterUrls | None:
        if not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        apiToken = await self.__ttsMonsterApiTokensRepository.get(twitchChannelId = twitchChannelId)
        if not utils.isValidStr(apiToken):
            self.__timber.log('TtsMonsterHelper', f'No TTS Monster API token is available for this user ({apiToken=}) ({twitchChannel=}) ({twitchChannelId=})')
            return None

        voices = await self.__ttsMonsterStreamerVoicesRepository.fetchVoices(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        if len(voices) == 0:
            self.__timber.log('TtsMonsterHelper', f'No TTS Monster voices are available for this user ({apiToken=}) ({twitchChannel=}) ({twitchChannelId=}) ({voices=})')
            return None

        messages = await self.__ttsMonsterMessageToVoicesHelper.build(
            voices = voices,
            message = message
        )

        if messages is None or len(messages) == 0:
            return await self.__generateSingleVoiceTts(
                apiToken = apiToken,
                message = message,
                twitchChannel = twitchChannel,
                twitchChannelId = twitchChannelId
            )
        else:
            return await self.__generateMultiVoiceTts(
                messages = messages,
                apiToken = apiToken,
                twitchChannel = twitchChannel,
                twitchChannelId = twitchChannelId
            )
