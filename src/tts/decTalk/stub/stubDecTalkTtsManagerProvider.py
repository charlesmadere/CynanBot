from ..decTalkTtsManagerInterface import DecTalkTtsManagerInterface
from ..decTalkTtsManagerProviderInterface import DecTalkTtsManagerProviderInterface
from ...models.ttsProvider import TtsProvider


class StubDecTalkTtsManagerProvider(DecTalkTtsManagerProviderInterface):

    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> DecTalkTtsManagerInterface | None:
        return None

    def getSharedInstance(self) -> DecTalkTtsManagerInterface | None:
        return None

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.DEC_TALK
