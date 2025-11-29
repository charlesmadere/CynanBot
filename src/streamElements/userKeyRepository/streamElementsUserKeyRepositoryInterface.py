from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class StreamElementsUserKeyRepositoryInterface(Clearable, ABC):

    # This returned value corresponds directly to the "key" HTTP query parameter in this example:
    # https://api.streamelements.com/kappa/v2/speech?voice=Brian&text=marley+cheered+x1000%2C++&key=BIG_KEY_STRING_HERE
    @abstractmethod
    async def get(
        self,
        twitchChannelId: str,
    ) -> str | None:
        pass

    @abstractmethod
    async def remove(
        self,
        twitchChannelId: str,
    ):
        pass

    @abstractmethod
    async def set(
        self,
        userKey: str | None,
        twitchChannelId: str,
    ):
        pass
