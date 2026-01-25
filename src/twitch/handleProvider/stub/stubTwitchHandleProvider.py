from dataclasses import dataclass

from ..twitchHandleProviderInterface import TwitchHandleProviderInterface


@dataclass(frozen = True, slots = True)
class StubTwitchHandleProvider(TwitchHandleProviderInterface):
    twitchHandle: str = 'CynanBot'

    async def getTwitchHandle(self) -> str:
        return self.twitchHandle
