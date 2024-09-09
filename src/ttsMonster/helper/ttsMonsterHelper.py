import traceback
from dataclasses import dataclass

from frozenlist import FrozenList

from .ttsMonsterHelperInterface import TtsMonsterHelperInterface
from ..apiService.ttsMonsterApiServiceInterface import TtsMonsterApiServiceInterface
from ..apiTokens.ttsMonsterApiTokensRepositoryInterface import TtsMonsterApiTokensRepositoryInterface
from ..messageToVoicesHelper.ttsMonsterMessageToVoicePair import TtsMonsterMessageToVoicePair
from ..messageToVoicesHelper.ttsMonsterMessageToVoicesHelperInterface import TtsMonsterMessageToVoicesHelperInterface
from ..models.ttsMonsterTtsRequest import TtsMonsterTtsRequest
from ..models.ttsMonsterWebsiteVoice import TtsMonsterWebsiteVoice
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
        index: int
        url: str

    def __init__(
        self,
        timber: TimberInterface,
        ttsMonsterApiService: TtsMonsterApiServiceInterface,
        ttsMonsterApiTokensRepository: TtsMonsterApiTokensRepositoryInterface,
        ttsMonsterMessageToVoicesHelper: TtsMonsterMessageToVoicesHelperInterface,
        ttsMonsterStreamerVoicesRepository: TtsMonsterStreamerVoicesRepositoryInterface,
        returnCharacterUsage: bool = True,
        defaultVoice: TtsMonsterWebsiteVoice = TtsMonsterWebsiteVoice.BRIAN
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsMonsterApiService, TtsMonsterApiServiceInterface):
            raise TypeError(f'ttsMonsterApiService argument is malformed: \"{ttsMonsterApiService}\"')
        elif not isinstance(ttsMonsterApiTokensRepository, TtsMonsterApiTokensRepositoryInterface):
            raise TypeError(f'ttsMonsterApiTokensRepository argument is malformed: \"{ttsMonsterApiTokensRepository}\"')
        elif not isinstance(ttsMonsterMessageToVoicesHelper, TtsMonsterMessageToVoicesHelperInterface):
            raise TypeError(f'ttsMonsterMessageToVoicesHelper argument is malformed: \"{ttsMonsterMessageToVoicesHelper}\"')
        elif not isinstance(ttsMonsterStreamerVoicesRepository, TtsMonsterStreamerVoicesRepositoryInterface):
            raise TypeError(f'ttsMonsterStreamerVoicesRepository argument is malformed: \"{ttsMonsterStreamerVoicesRepository}\"')
        elif not utils.isValidBool(returnCharacterUsage):
            raise TypeError(f'returnCharacterUsage argument is malformed: \"{returnCharacterUsage}\"')
        elif not isinstance(defaultVoice, TtsMonsterWebsiteVoice):
            raise TypeError(f'defaultVoice argument is malformed: \"{defaultVoice}\"')

        self.__timber: TimberInterface = timber
        self.__ttsMonsterApiService: TtsMonsterApiServiceInterface = ttsMonsterApiService
        self.__ttsMonsterApiTokensRepository: TtsMonsterApiTokensRepositoryInterface = ttsMonsterApiTokensRepository
        self.__ttsMonsterMessageToVoicesHelper: TtsMonsterMessageToVoicesHelperInterface = ttsMonsterMessageToVoicesHelper
        self.__ttsMonsterStreamerVoicesRepository: TtsMonsterStreamerVoicesRepositoryInterface = ttsMonsterStreamerVoicesRepository
        self.__returnCharacterUsage: bool = returnCharacterUsage
        self.__defaultVoice: TtsMonsterWebsiteVoice = defaultVoice

    async def __fetchTtsUrl(
        self,
        apiToken: str,
        message: str,
        voiceId: str
    ) -> str:
        if not utils.isValidStr(apiToken):
            raise TypeError(f'apiToken argument is malformed: \"{apiToken}\"')
        elif not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(voiceId):
            raise TypeError(f'voiceId argument is malformed: \"{voiceId}\"')

        ttsRequest = TtsMonsterTtsRequest(
            returnUsage = self.__returnCharacterUsage,
            message = message,
            voiceId = voiceId
        )

        ttsResponse = await self.__ttsMonsterApiService.generateTts(
            apiToken = apiToken,
            request = ttsRequest
        )

        return ttsResponse.url

    async def __generateMultiVoiceTts(
        self,
        messages: FrozenList[TtsMonsterMessageToVoicePair],
        apiToken: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> FrozenList[str] | None:
        ttsRequests: list[TtsMonsterHelper.TtsRequestEntry] = list()

        for index, messageToVoicePair in enumerate(messages):
            ttsRequests.append(TtsMonsterHelper.TtsRequestEntry(
                index = index,
                messageToVoicePair = messageToVoicePair
            ))

        ttsResponses: list[TtsMonsterHelper.TtsResponseEntry] = list()

        try:
            for ttsRequest in ttsRequests:
                ttsUrl = await self.__fetchTtsUrl(
                    apiToken = apiToken,
                    message = ttsRequest.messageToVoicePair.message,
                    voiceId = ttsRequest.messageToVoicePair.voice.voiceId
                )

                ttsResponses.append(TtsMonsterHelper.TtsResponseEntry(
                    index = ttsRequest.index,
                    url = ttsUrl
                ))
        except GenericNetworkException as e:
            self.__timber.log('TtsMonsterHelper', f'Encountered network error when generating TTS from TTS Monster ({apiToken=}) ({twitchChannel=}) ({twitchChannelId=}): {e}', e, traceback.format_exc())
            return None

        ttsResponses.sort(key = lambda element: element.index)
        ttsUrls: list[str] = list()

        for ttsResponse in ttsResponses:
            ttsUrls.append(ttsResponse.url)

        frozenTtsUrls: FrozenList[str] = FrozenList(ttsUrls)
        frozenTtsUrls.freeze()

        return frozenTtsUrls

    async def __generateSingleVoiceTts(
        self,
        apiToken: str,
        message: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> FrozenList[str] | None:
        try:
            ttsUrl = await self.__fetchTtsUrl(
                apiToken = apiToken,
                message = message,
                voiceId = self.__defaultVoice.voiceId
            )
        except GenericNetworkException as e:
            self.__timber.log('TtsMonsterHelper', f'Encountered network error when generating TTS from TTS Monster ({apiToken=}) ({twitchChannel=}) ({twitchChannelId=}): {e}', e, traceback.format_exc())
            return None

        ttsUrls: FrozenList[str] = FrozenList()
        ttsUrls.append(ttsUrl)
        ttsUrls.freeze()

        return ttsUrls

    async def generateTts(
        self,
        message: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> FrozenList[str] | None:
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
