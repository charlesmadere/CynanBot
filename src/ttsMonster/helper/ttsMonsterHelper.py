import random
import traceback

from .ttsMonsterHelperInterface import TtsMonsterHelperInterface
from ..apiService.ttsMonsterApiServiceInterface import TtsMonsterApiServiceInterface
from ..apiTokens.ttsMonsterApiTokensRepositoryInterface import TtsMonsterApiTokensRepositoryInterface
from ..models.ttsMonsterTtsRequest import TtsMonsterTtsRequest
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...timber.timberInterface import TimberInterface


class TtsMonsterHelper(TtsMonsterHelperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        ttsMonsterApiService: TtsMonsterApiServiceInterface,
        ttsMonsterApiTokensRepository: TtsMonsterApiTokensRepositoryInterface,
        returnCharacterUsage: bool = True
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsMonsterApiService, TtsMonsterApiServiceInterface):
            raise TypeError(f'ttsMonsterApiService argument is malformed: \"{ttsMonsterApiService}\"')
        elif not isinstance(ttsMonsterApiTokensRepository, TtsMonsterApiTokensRepositoryInterface):
            raise TypeError(f'ttsMonsterApiTokensRepository argument is malformed: \"{ttsMonsterApiTokensRepository}\"')
        elif not utils.isValidBool(returnCharacterUsage):
            raise TypeError(f'returnCharacterUsage argument is malformed: \"{returnCharacterUsage}\"')

        self.__timber: TimberInterface = timber
        self.__ttsMonsterApiService: TtsMonsterApiServiceInterface = ttsMonsterApiService
        self.__ttsMonsterApiTokensRepository: TtsMonsterApiTokensRepositoryInterface = ttsMonsterApiTokensRepository
        self.__returnCharacterUsage: bool = returnCharacterUsage

    async def __chooseRandomVoiceId(self, apiToken: str) -> str | None:
        if not utils.isValidStr(apiToken):
            raise TypeError(f'apiToken argument is malformed: \"{apiToken}\"')

        try:
            voicesResponse = await self.__ttsMonsterApiService.getVoices(apiToken = apiToken)
        except GenericNetworkException as e:
            self.__timber.log('TtsMonsterHelper', f'Encountered network error when fetching voices from TTS Monster: {e}', e, traceback.format_exc())
            return None

        allVoiceIds: set[str] = set()

        if voicesResponse.voices is not None:
            for voice in voicesResponse.voices:
                allVoiceIds.add(voice.voiceId)

        if voicesResponse.customVoices is not None:
            for voice in voicesResponse.customVoices:
                allVoiceIds.add(voice.voiceId)

        allVoiceIdsList: list[str] = list(allVoiceIds)
        return random.choice(allVoiceIdsList)

    async def generateTts(
        self,
        message: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> str | None:
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

        voiceId = await self.__chooseRandomVoiceId(apiToken = apiToken)
        if not utils.isValidStr(voiceId):
            self.__timber.log('TtsMonsterHelper', f'Failed to choose a random TTS Monster voice for this user ({apiToken=}) ({twitchChannel=}) ({twitchChannelId=})')
            return None

        ttsRequest = TtsMonsterTtsRequest(
            returnUsage = self.__returnCharacterUsage,
            message = message,
            voiceId = voiceId
        )

        try:
            ttsResponse = await self.__ttsMonsterApiService.generateTts(
                apiToken = apiToken,
                request = ttsRequest
            )
        except GenericNetworkException as e:
            self.__timber.log('TtsMonsterHelper', f'Encountered network error when generating TTS from TTS Monster ({apiToken=}) ({twitchChannel=}) ({twitchChannelId=}): {e}', e, traceback.format_exc())
            return None

        self.__timber.log('TtsMonsterHelper', f'Successfully generated TTS from TTS Monster ({apiToken=}) ({twitchChannel=}) ({twitchChannelId=}) ({ttsResponse=})')
        return ttsResponse.url
