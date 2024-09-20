from .streamElementsHelperInterface import StreamElementsHelperInterface
from ..userKeyRepository.streamElementsUserKeyRepositoryInterface import StreamElementsUserKeyRepositoryInterface


class StreamElementsHelper(StreamElementsHelperInterface):

    def __init__(
        self,
        streamElementsUserKeyRepository: StreamElementsUserKeyRepositoryInterface
    ):
        if not isinstance(streamElementsUserKeyRepository, StreamElementsUserKeyRepositoryInterface):
            raise TypeError(f'streamElementsUserKeyRepository argument is malformed: \"{streamElementsUserKeyRepository}\"')

        self.__streamElementsUserKeyRepository: StreamElementsUserKeyRepositoryInterface = streamElementsUserKeyRepository

    async def getSpeech(
        self,
        message: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ) -> bytes | None:
        return None
