from typing import Any

from frozenlist import FrozenList

from .ttsMonsterJsonMapperInterface import TtsMonsterJsonMapperInterface
from .ttsMonsterWebsiteVoiceMapperInterface import TtsMonsterWebsiteVoiceMapperInterface
from ..models.ttsMonsterPrivateApiTtsResponse import TtsMonsterPrivateApiTtsResponse
from ..models.ttsMonsterTtsRequest import TtsMonsterTtsRequest
from ..models.ttsMonsterTtsResponse import TtsMonsterTtsResponse
from ..models.ttsMonsterUser import TtsMonsterUser
from ..models.ttsMonsterVoice import TtsMonsterVoice
from ..models.ttsMonsterVoicesResponse import TtsMonsterVoicesResponse
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class TtsMonsterJsonMapper(TtsMonsterJsonMapperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        websiteVoiceMapper: TtsMonsterWebsiteVoiceMapperInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(websiteVoiceMapper, TtsMonsterWebsiteVoiceMapperInterface):
            raise TypeError(f'websiteVoiceMapper argument is malformed: \"{websiteVoiceMapper}\"')

        self.__timber: TimberInterface = timber
        self.__websiteVoiceMapper: TtsMonsterWebsiteVoiceMapperInterface = websiteVoiceMapper

    async def parseFromPrivateTtsResponse(
        self,
        privateTtsResponse: TtsMonsterPrivateApiTtsResponse
    ) -> TtsMonsterTtsResponse:
        if not isinstance(privateTtsResponse, TtsMonsterPrivateApiTtsResponse):
            raise TypeError(f'privateTtsResponse argument is malformed: \"{privateTtsResponse}\"')

        return TtsMonsterTtsResponse(
            characterUsage = None,
            status = privateTtsResponse.status,
            url = privateTtsResponse.data.link
        )

    async def parseTtsResponse(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> TtsMonsterTtsResponse | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        characterUsage: int | None = None
        if 'characterUsage' in jsonContents and utils.isValidInt(jsonContents.get('characterUsage')):
            characterUsage = utils.getIntFromDict(jsonContents, 'characterUsage')

        status = utils.getIntFromDict(jsonContents, 'status')
        url = utils.getStrFromDict(jsonContents, 'url')

        return TtsMonsterTtsResponse(
            characterUsage = characterUsage,
            status = status,
            url = url
        )

    async def parseUser(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> TtsMonsterUser | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        currentPlan: str | None = None
        if 'current_plan' in jsonContents and utils.isValidStr(currentPlan):
            currentPlan = utils.getStrFromDict(jsonContents, 'current_plan')

        characterAllowance = utils.getIntFromDict(jsonContents, 'character_allowance')
        characterUsage = utils.getIntFromDict(jsonContents, 'character_usage')
        status = utils.getStrFromDict(jsonContents, 'status')

        return TtsMonsterUser(
            characterAllowance = characterAllowance,
            characterUsage = characterUsage,
            currentPlan = currentPlan,
            status = status
        )

    async def parseVoice(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> TtsMonsterVoice | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        language: str | None = None
        if 'language' in jsonContents and utils.isValidStr(jsonContents.get('language')):
            language = utils.getStrFromDict(jsonContents, 'language')

        metadata: str | None = None
        if 'metadata' in jsonContents and utils.isValidStr(jsonContents.get('metadata')):
            metadata = utils.getStrFromDict(jsonContents, 'metadata')

        name = utils.getStrFromDict(jsonContents, 'name')

        sample: str | None = None
        if 'sample' in jsonContents and utils.isValidUrl(jsonContents.get('sample')):
            sample = utils.getStrFromDict(jsonContents, 'sample')

        voiceId = utils.getStrFromDict(jsonContents, 'voice_id')
        websiteVoice = await self.__websiteVoiceMapper.fromApiVoiceId(voiceId)

        return TtsMonsterVoice(
            language = language,
            metadata = metadata,
            name = name,
            sample = sample,
            voiceId = voiceId,
            websiteVoice = websiteVoice
        )

    async def parseVoicesResponse(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> TtsMonsterVoicesResponse | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        customVoicesArray: list[dict[str, Any]] | Any | None = jsonContents.get('customVoices', None)
        customVoices: list[TtsMonsterVoice] = list()

        if isinstance(customVoicesArray, list) and len(customVoicesArray) >= 1:
            for index, customVoiceJson in enumerate(customVoicesArray):
                customVoice = await self.parseVoice(customVoiceJson)

                if customVoice is None:
                    self.__timber.log('TtsMonsterJsonMapper', f'Unable to parse value at index {index} for \"customVoices\" data: ({jsonContents=})')
                else:
                    customVoices.append(customVoice)

        frozenCustomVoices: FrozenList[TtsMonsterVoice] | None = None

        if len(customVoices) >= 1:
            customVoices.sort(key = lambda element: element.name.casefold())
            frozenCustomVoices = FrozenList(customVoices)
            frozenCustomVoices.freeze()

        voicesArray: list[dict[str, Any]] | Any | None = jsonContents.get('voices', None)
        voices: list[TtsMonsterVoice] = list()

        if isinstance(voicesArray, list) and len(voicesArray) >= 1:
            for index, voiceJson in enumerate(voicesArray):
                voice = await self.parseVoice(voiceJson)

                if voice is None:
                    self.__timber.log('TtsMonsterJsonMapper', f'Unable to parse value at index {index} for \"voices\" data: ({jsonContents=})')
                else:
                    voices.append(voice)

        frozenVoices: FrozenList[TtsMonsterVoice] | None = None

        if len(voices) >= 1:
            voices.sort(key = lambda element: element.name.casefold())
            frozenVoices = FrozenList(voices)
            frozenVoices.freeze()

        return TtsMonsterVoicesResponse(
            customVoices = frozenCustomVoices,
            voices = frozenVoices
        )

    async def serializeTtsRequest(
        self,
        request: TtsMonsterTtsRequest
    ) -> dict[str, Any]:
        if not isinstance(request, TtsMonsterTtsRequest):
            raise TypeError(f'request argument is malformed: \"{request}\"')

        dictionary: dict[str, Any] = {
            'message': request.message,
            'voice_id': request.voiceId
        }

        if request.returnUsage:
            dictionary['return_usage'] = True

        return dictionary
