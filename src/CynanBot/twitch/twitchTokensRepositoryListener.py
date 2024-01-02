from abc import ABC, abstractmethod

from CynanBot.twitch.api.twitchTokensDetails import TwitchTokensDetails


class TwitchTokensRepositoryListener(ABC):

    @abstractmethod
    async def onUserAdded(self, tokensDetails: TwitchTokensDetails, twitchChannel: str):
        pass

    @abstractmethod
    async def onUserRemoved(self, twitchChannel: str):
        pass
