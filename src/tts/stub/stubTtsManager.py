from ..ttsEvent import TtsEvent
from ..ttsManagerInterface import TtsManagerInterface


class StubTtsManager(TtsManagerInterface):

    async def isPlaying(self) -> bool:
        # this method is intentionally empty
        return False

    async def playTtsEvent(self, event: TtsEvent) -> bool:
        # this method is intentionally empty
        return False

    async def stopTtsEvent(self):
        # this method is intentionally empty
        pass
