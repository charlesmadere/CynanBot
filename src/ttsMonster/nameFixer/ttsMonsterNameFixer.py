from frozendict import frozendict

from .ttsMonsterNameFixerInterface import TtsMonsterNameFixerInterface


class TtsMonsterNameFixer(TtsMonsterNameFixerInterface):

    def __init__(
        self,
        voiceIdToWebsiteName: frozendict[str, str] = frozendict({
            '50570964-9672-4927-ac7d-40575e9112d3': 'kkona',
            '1de3db1e-a4aa-4103-b399-ba6c1f1f95db': 'shadow'
        })
    ):
        if not isinstance(voiceIdToWebsiteName, frozendict):
            raise TypeError(f'voiceIdToWebsiteName argument is malformed: \"{voiceIdToWebsiteName}\"')

        self.__voiceIdToWebsiteName: frozendict[str, str] = voiceIdToWebsiteName

    async def getWebsiteName(self, apiVoiceId: str) -> str | None:
        return self.__voiceIdToWebsiteName.get(apiVoiceId, None)
