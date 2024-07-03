from abc import abstractmethod

from ...misc.clearable import Clearable


class TwitchEmotesHelperInterface(Clearable):

    @abstractmethod
    async def fetchViableEmoteNamesFor(
        self,
        twitchAccessToken: str,
        twitchChannelId: str
    ) -> set[str]:
        pass
