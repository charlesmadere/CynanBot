from ..ttsEvent import TtsEvent
from ..ttsManagerInterface import TtsManagerInterface


class StubTtsManager(TtsManagerInterface):

    async def isPlaying(self) -> bool:
        return False

    async def playTtsEvent(self, event: TtsEvent) -> bool:
        return False
