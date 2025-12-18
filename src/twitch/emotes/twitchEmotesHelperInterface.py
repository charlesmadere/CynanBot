from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class TwitchEmotesHelperInterface(Clearable, ABC):

    @abstractmethod
    async def fetchViableSubscriptionEmoteNames(
        self,
        twitchChannelId: str,
    ) -> frozenset[str]:
        pass
