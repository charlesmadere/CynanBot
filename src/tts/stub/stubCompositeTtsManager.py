from ..compositeTtsManagerInterface import CompositeTtsManagerInterface
from ..models.ttsEvent import TtsEvent


class StubCompositeTtsManager(CompositeTtsManagerInterface):

    @property
    def isLoadingOrPlaying(self) -> bool:
        # this method is intentionally empty
        return False

    async def playTtsEvent(self, event: TtsEvent) -> bool:
        # this method is intentionally empty
        return False

    async def stopTtsEvent(self):
        # this method is intentionally empty
        pass
