from .streamLabsUserIdProviderInterface import StreamLabsUserIdProviderInterface


class StreamLabsUserIdProvider(StreamLabsUserIdProviderInterface):

    def __init__(self, streamLabs: str | None = '105166207'):
        if streamLabs is not None and not isinstance(streamLabs, str):
            raise TypeError(f'streamLabsUserId argument is malformed: \"{streamLabs}\"')

        self.__streamLabsUserId: str | None = streamLabs

    async def getStreamLabsUserId(self) -> str | None:
        return self.__streamLabsUserId
