from ..microsoftTtsManagerInterface import MicrosoftTtsManagerInterface
from ..microsoftTtsManagerProviderInterface import MicrosoftTtsManagerProviderInterface
from ...models.ttsProvider import TtsProvider


class StubMicrosoftTtsManagerProvider(MicrosoftTtsManagerProviderInterface):

    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> MicrosoftTtsManagerInterface | None:
        return None

    def getSharedInstance(self) -> MicrosoftTtsManagerInterface | None:
        return None

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.MICROSOFT
