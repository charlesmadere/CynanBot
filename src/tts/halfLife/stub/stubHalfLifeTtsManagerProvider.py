from ..halfLifeTtsManagerInterface import HalfLifeTtsManagerInterface
from ..halfLifeTtsManagerProviderInterface import HalfLifeTtsManagerProviderInterface
from ...models.ttsProvider import TtsProvider


class StubHalfLifeTtsManagerProvider(HalfLifeTtsManagerProviderInterface):

    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> HalfLifeTtsManagerInterface | None:
        return None

    def getSharedInstance(self) -> HalfLifeTtsManagerInterface | None:
        return None

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.HALF_LIFE
