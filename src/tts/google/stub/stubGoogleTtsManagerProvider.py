from ..googleTtsManagerInterface import GoogleTtsManagerInterface
from ..googleTtsManagerProviderInterface import GoogleTtsManagerProviderInterface
from ...models.ttsProvider import TtsProvider


class StubGoogleTtsManagerProvider(GoogleTtsManagerProviderInterface):

    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> GoogleTtsManagerInterface | None:
        return None

    def getSharedInstance(self) -> GoogleTtsManagerInterface | None:
        return None

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.GOOGLE
