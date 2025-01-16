import asyncio
import math
import traceback
from dataclasses import dataclass
from typing import Any, Coroutine

from frozenlist import FrozenList

from .ttsMonsterHelperInterface import TtsMonsterHelperInterface
from .ttsMonsterPrivateApiHelperInterface import TtsMonsterPrivateApiHelperInterface
from ..apiService.ttsMonsterApiServiceInterface import TtsMonsterApiServiceInterface
from ..apiTokens.ttsMonsterApiTokensRepositoryInterface import TtsMonsterApiTokensRepositoryInterface
from ..messageToVoicesHelper.ttsMonsterMessageToVoicePair import TtsMonsterMessageToVoicePair
from ..messageToVoicesHelper.ttsMonsterMessageToVoicesHelperInterface import TtsMonsterMessageToVoicesHelperInterface
from ..models.ttsMonsterTtsRequest import TtsMonsterTtsRequest
from ..models.ttsMonsterUrls import TtsMonsterUrls
from ..models.ttsMonsterUser import TtsMonsterUser
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
        ttsMonsterPrivateApiHelper: TtsMonsterPrivateApiHelperInterface | None,
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
        elif ttsMonsterPrivateApiHelper is not None and not isinstance(ttsMonsterPrivateApiHelper, TtsMonsterPrivateApiHelperInterface):
            raise TypeError(f'ttsMonsterPrivateApiHelper argument is malformed: \"{ttsMonsterPrivateApiHelper}\"')
        elif not isinstance(ttsMonsterSettingsRepository, TtsMonsterSettingsRepositoryInterface):
            raise TypeError(f'ttsMonsterSettingsRepository argument is malformed: \"{ttsMonsterSettingsRepository}\"')
        elif not isinstance(ttsMonsterStreamerVoicesRepository, TtsMonsterStreamerVoicesRepositoryInterface):
            raise TypeError(f'ttsMonsterStreamerVoicesRepository argument is malformed: \"{ttsMonsterStreamerVoicesRepository}\"')

        self.__timber: TimberInterface = timber
        self.__ttsMonsterApiService: TtsMonsterApiServiceInterface = ttsMonsterApiService
        self.__ttsMonsterApiTokensRepository: TtsMonsterApiTokensRepositoryInterface = ttsMonsterApiTokensRepository
        self.__ttsMonsterMessageToVoicesHelper: TtsMonsterMessageToVoicesHelperInterface = ttsMonsterMessageToVoicesHelper
        self.__ttsMonsterPrivateApiHelper: TtsMonsterPrivateApiHelperInterface | None = ttsMonsterPrivateApiHelper
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

    async def generateTts(
        self,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> TtsMonsterUrls | None:
        if message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        if not utils.isValidStr(message):
            return None

        result: TtsMonsterUrls | None = None
        alreadyTriedPrivateApi = False

        if await self.__ttsMonsterSettingsRepository.usePrivateApiFirst():
            result = await self.__generateTtsUsingPrivateApi(
                message = message,
                twitchChannel = twitchChannel,
                twitchChannelId = twitchChannelId
            )

            alreadyTriedPrivateApi = True

            if result is not None:
                return result

        apiToken = await self.__ttsMonsterApiTokensRepository.get(twitchChannelId = twitchChannelId)
        if not utils.isValidStr(apiToken):
            self.__timber.log('TtsMonsterHelper', f'No TTS Monster API token is available for this user ({apiToken=}) ({twitchChannel=}) ({twitchChannelId=})')
            return None

        voices = await self.__ttsMonsterStreamerVoicesRepository.fetchVoices(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        if len(voices) == 0:
            self.__timber.log('TtsMonsterHelper', f'No TTS Monster voices are available for this user ({twitchChannel=}) ({twitchChannelId=}) ({voices=})')
            return None

        try:
            ttsMonsterUser = await self.__ttsMonsterApiService.getUser(apiToken = apiToken)
        except GenericNetworkException as e:
            self.__timber.log('TtsMonsterHelper', f'Encountered network exception when fetching TTS Monster user details ({twitchChannel=}) ({twitchChannelId=}): {e}', e, traceback.format_exc())
            return None

        if ttsMonsterUser.characterUsage >= ttsMonsterUser.characterAllowance:
            self.__timber.log('TtsMonsterHelper', f'This TTS Monster user is beyond their character allowance ({ttsMonsterUser=}) ({twitchChannel=}) ({twitchChannelId=})')

            return await self.__generateTtsUsingPrivateApi(
                message = message,
                twitchChannel = twitchChannel,
                twitchChannelId = twitchChannelId
            )

        messages = await self.__ttsMonsterMessageToVoicesHelper.build(
            voices = voices,
            message = message
        )

        if messages is None or len(messages) == 0:
            return None
        elif await self.__messagesLengthIsBeyondCharacterAllowance(
            messages = messages,
            ttsMonsterUser = ttsMonsterUser
        ):
            if alreadyTriedPrivateApi:
                return None
            else:
                self.__timber.log('TtsMonsterHelper', f'This TTS Monster user isn\'t yet beyond their character allowance, but this new message would surpass it ({ttsMonsterUser=}) ({twitchChannel=}) ({twitchChannelId=})')

                return await self.__generateTtsUsingPrivateApi(
                    message = message,
                    twitchChannel = twitchChannel,
                    twitchChannelId = twitchChannelId
                )
        else:
            return await self.__generateTtsUsingOfficialApi(
                characterAllowance = ttsMonsterUser.characterAllowance,
                messages = messages,
                apiToken = apiToken,
                twitchChannel = twitchChannel,
                twitchChannelId = twitchChannelId
            )

    async def __generateTtsUsingOfficialApi(
        self,
        characterAllowance: int | None,
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
            ttsResponses.extend(await asyncio.gather(*ttsResponseCoroutines, return_exceptions = False))
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
            characterAllowance = characterAllowance,
            characterUsage = characterUsage
        )

    async def __generateTtsUsingPrivateApi(
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

        if self.__ttsMonsterPrivateApiHelper is None:
            return None
        elif not await self.__ttsMonsterSettingsRepository.isUsePrivateApiEnabled():
            return None

        return await self.__ttsMonsterPrivateApiHelper.generateTts(
            message = message,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

    async def __messagesLengthIsBeyondCharacterAllowance(
        self,
        messages: FrozenList[TtsMonsterMessageToVoicePair],
        ttsMonsterUser: TtsMonsterUser,
    ) -> bool:
        if not isinstance(messages, FrozenList) or len(messages) == 0:
            raise TypeError(f'messages argument is malformed: \"{messages}\"')
        elif not isinstance(ttsMonsterUser, TtsMonsterUser):
            raise TypeError(f'ttsMonsterUser argument is malformed: \"{ttsMonsterUser}\"')

        totalMessagesLength = 0

        for message in messages:
            currentMessageLength = len(message.message)
            currentMessageLength += int(math.ceil(float(currentMessageLength) * 0.02)) # add a few extra characters
                                                                                       # just to be safe

            totalMessagesLength = totalMessagesLength + currentMessageLength

        return ttsMonsterUser.characterUsage + totalMessagesLength >= ttsMonsterUser.characterAllowance
