from ..commodoreSamTtsManagerInterface import CommodoreSamTtsManagerInterface
from ..commodoreSamTtsManagerProviderInterface import CommodoreSamTtsManagerProviderInterface
from ...models.ttsProvider import TtsProvider


class StubCommodoreSamTtsManagerProvider(CommodoreSamTtsManagerProviderInterface):

    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> CommodoreSamTtsManagerInterface | None:
        return None

    def getSharedInstance(self) -> CommodoreSamTtsManagerInterface | None:
        return None

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.COMMODORE_SAM
