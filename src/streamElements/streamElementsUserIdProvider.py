from .streamElementsUserIdProviderInterface import StreamElementsUserIdProviderInterface


class StreamElementsUserIdProvider(StreamElementsUserIdProviderInterface):

    def __init__(self, streamElementsUserId: str | None = '100135110'):
        if streamElementsUserId is not None and not isinstance(streamElementsUserId, str):
            raise TypeError(f'streamElementsUserId argument is malformed: \"{streamElementsUserId}\"')

        self.__streamElementsUserId: str | None = streamElementsUserId

    async def getStreamElementsUserId(self) -> str | None:
        return self.__streamElementsUserId
