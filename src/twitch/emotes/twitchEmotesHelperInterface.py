from abc import abstractmethod

from ...misc.clearable import Clearable


class TwitchEmotesHelperInterface(Clearable):

    @abstractmethod
    async def fetchViableSubscriptionEmoteNames(
        self,
        twitchAccessToken: str,
        twitchChannelId: str
    ) -> frozenset[str]:
        pass
