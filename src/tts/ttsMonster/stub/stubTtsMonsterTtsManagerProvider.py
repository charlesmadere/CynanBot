from ..ttsMonsterTtsManagerInterface import TtsMonsterTtsManagerInterface
from ..ttsMonsterTtsManagerProviderInterface import TtsMonsterTtsManagerProviderInterface


class StubTtsMonsterTtsManagerProvider(TtsMonsterTtsManagerProviderInterface):

    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> TtsMonsterTtsManagerInterface | None:
        return None

    def getSharedInstance(self) -> TtsMonsterTtsManagerInterface | None:
        return None
