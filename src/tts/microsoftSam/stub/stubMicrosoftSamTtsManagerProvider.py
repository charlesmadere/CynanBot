from ..microsoftSamTtsManagerInterface import MicrosoftSamTtsManagerInterface
from ..microsoftSamTtsManagerProviderInterface import MicrosoftSamTtsManagerProviderInterface


class StubMicrosoftSamTtsManagerProvider(MicrosoftSamTtsManagerProviderInterface):

    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> MicrosoftSamTtsManagerInterface | None:
        return None

    def getSharedInstance(self) -> MicrosoftSamTtsManagerInterface | None:
        return None
