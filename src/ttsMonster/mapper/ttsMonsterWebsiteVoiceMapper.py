from frozendict import frozendict

from .ttsMonsterWebsiteVoiceMapperInterface import TtsMonsterWebsiteVoiceMapperInterface
from ..models.ttsMonsterWebsiteVoice import TtsMonsterWebsiteVoice
from ...misc import utils as utils


class TtsMonsterWebsiteVoiceMapper(TtsMonsterWebsiteVoiceMapperInterface):

    def __init__(self):
        self.__apiVoiceIdToWebsiteVoiceDictionary: frozendict[str, TtsMonsterWebsiteVoice | None] | None = None
        self.__websiteNameToWebsiteVoiceDictionary: frozendict[str, TtsMonsterWebsiteVoice | None] | None = None

    async def __getApiVoiceIdToWebsiteVoices(self) -> frozendict[str, TtsMonsterWebsiteVoice | None]:
        apiVoiceIdToWebsiteVoices = self.__apiVoiceIdToWebsiteVoiceDictionary

        if apiVoiceIdToWebsiteVoices is None:
            newApiVoiceIdToWebsiteVoices: dict[str, TtsMonsterWebsiteVoice] = dict()

            for websiteVoice in TtsMonsterWebsiteVoice:
                newApiVoiceIdToWebsiteVoices[websiteVoice.voiceId] = websiteVoice

            apiVoiceIdToWebsiteVoices = frozendict(newApiVoiceIdToWebsiteVoices)

        return apiVoiceIdToWebsiteVoices

    async def __getWebsiteNameToWebsiteVoices(self) -> frozendict[str, TtsMonsterWebsiteVoice | None]:
        websiteNameToWebsiteVoices = self.__websiteNameToWebsiteVoiceDictionary

        if websiteNameToWebsiteVoices is None:
            newWebsiteNameToWebsiteVoices: dict[str, TtsMonsterWebsiteVoice] = dict()

            for websiteVoice in TtsMonsterWebsiteVoice:
                newWebsiteNameToWebsiteVoices[websiteVoice.websiteName.casefold()] = websiteVoice

            websiteNameToWebsiteVoices = frozendict(newWebsiteNameToWebsiteVoices)

        return websiteNameToWebsiteVoices

    async def fromApiVoiceId(self, apiVoiceId: str) -> TtsMonsterWebsiteVoice | None:
        if not utils.isValidStr(apiVoiceId):
            raise TypeError(f'apiVoiceId argument is malformed: \"{apiVoiceId}\"')

        apiVoiceIdToWebsiteVoices = await self.__getApiVoiceIdToWebsiteVoices()
        return apiVoiceIdToWebsiteVoices.get(apiVoiceId, None)

    async def fromWebsiteName(self, websiteName: str) -> TtsMonsterWebsiteVoice:
        if not utils.isValidStr(websiteName):
            raise TypeError(f'websiteName argument is malformed: \"{websiteName}\"')

        websiteNameToWebsiteVoices = await self.__getWebsiteNameToWebsiteVoices()
        websiteVoice = websiteNameToWebsiteVoices.get(websiteName.casefold(), None)

        if websiteVoice is None:
            raise ValueError(f'Encountered unknown TtsMonsterWebsiteVoice value: \"{websiteName}\"')

        return websiteVoice
