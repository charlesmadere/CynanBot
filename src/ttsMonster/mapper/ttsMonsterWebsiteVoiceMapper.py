from frozendict import frozendict

from .ttsMonsterWebsiteVoiceMapperInterface import TtsMonsterWebsiteVoiceMapperInterface
from ..models.ttsMonsterWebsiteVoice import TtsMonsterWebsiteVoice
from ...misc import utils as utils


class TtsMonsterWebsiteVoiceMapper(TtsMonsterWebsiteVoiceMapperInterface):

    def __init__(self):
        self.__apiVoiceIdToWebsiteVoiceDictionary: frozendict[str, TtsMonsterWebsiteVoice | None] | None = None

    async def __getApiVoiceIdToWebsiteVoices(self) -> frozendict[str, TtsMonsterWebsiteVoice | None]:
        apiVoiceIdToWebsiteVoices = self.__apiVoiceIdToWebsiteVoiceDictionary

        if apiVoiceIdToWebsiteVoices is None:
            newApiVoiceIdToWebsiteVoices = dict()

            for websiteVoice in TtsMonsterWebsiteVoice:
                newApiVoiceIdToWebsiteVoices[websiteVoice.voiceId] = websiteVoice

            apiVoiceIdToWebsiteVoices = frozendict(newApiVoiceIdToWebsiteVoices)

        return apiVoiceIdToWebsiteVoices

    async def map(self, apiVoiceId: str) -> TtsMonsterWebsiteVoice | None:
        if not utils.isValidStr(apiVoiceId):
            raise TypeError(f'apiVoiceId argument is malformed: \"{apiVoiceId}\"')

        apiVoiceIdToWebsiteVoices = await self.__getApiVoiceIdToWebsiteVoices()
        return apiVoiceIdToWebsiteVoices.get(apiVoiceId, None)
