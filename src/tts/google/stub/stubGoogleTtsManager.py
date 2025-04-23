from ..googleTtsManagerInterface import GoogleTtsManagerInterface
from ...models.ttsEvent import TtsEvent
from ...models.ttsProvider import TtsProvider


class StubGoogleTtsManager(GoogleTtsManagerInterface):

    @property
    def isLoadingOrPlaying(self) -> bool:
        return False

    async def playTtsEvent(self, event: TtsEvent):
        # this method is intentionally empty
        pass

    async def stopTtsEvent(self):
        # this method is intentionally empty
        pass

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.GOOGLE
