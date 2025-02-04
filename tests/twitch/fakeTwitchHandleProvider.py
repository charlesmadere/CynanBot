from src.twitch.twitchHandleProviderInterface import TwitchHandleProviderInterface


class FakeTwitchHandleProvider(TwitchHandleProviderInterface):

    def __init__(self, twitchHandle: str = 'CynanBot'):
        self.__twitchHandle: str = twitchHandle

    async def getTwitchHandle(self) -> str:
        return self.__twitchHandle
