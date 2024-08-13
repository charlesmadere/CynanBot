from abc import abstractmethod

from ...misc.clearable import Clearable


class TwitchEmotesHelperInterface(Clearable):

    @abstractmethod
    async def fetchViableSubscriptionEmoteNames(
        self,
        twitchChannelId: str
    ) -> frozenset[str]:
        pass
