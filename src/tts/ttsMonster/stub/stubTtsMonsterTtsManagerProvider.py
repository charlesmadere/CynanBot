from ..ttsMonsterTtsManagerInterface import TtsMonsterTtsManagerInterface
from ..ttsMonsterTtsManagerProviderInterface import TtsMonsterTtsManagerProviderInterface
from ...models.ttsProvider import TtsProvider


class StubTtsMonsterTtsManagerProvider(TtsMonsterTtsManagerProviderInterface):

    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> TtsMonsterTtsManagerInterface | None:
        return None

    def getSharedInstance(self) -> TtsMonsterTtsManagerInterface | None:
        return None

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.TTS_MONSTER
