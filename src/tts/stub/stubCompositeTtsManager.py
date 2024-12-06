from ..compositeTtsManagerInterface import CompositeTtsManagerInterface
from ..ttsEvent import TtsEvent


class StubCompositeTtsManager(CompositeTtsManagerInterface):

    async def isPlaying(self) -> bool:
        # this method is intentionally empty
        return False

    async def playTtsEvent(self, event: TtsEvent) -> bool:
        # this method is intentionally empty
        return False

    async def stopTtsEvent(self):
        # this method is intentionally empty
        pass
