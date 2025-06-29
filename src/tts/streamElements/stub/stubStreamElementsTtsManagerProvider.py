from ..streamElementsTtsManagerInterface import StreamElementsTtsManagerInterface
from ..streamElementsTtsManagerProviderInterface import StreamElementsTtsManagerProviderInterface


class StubStreamElementsTtsManagerProvider(StreamElementsTtsManagerProviderInterface):

    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> StreamElementsTtsManagerInterface | None:
        return None

    def getSharedInstance(self) -> StreamElementsTtsManagerInterface | None:
        return None
