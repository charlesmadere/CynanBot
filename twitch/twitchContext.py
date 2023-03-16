from typing import Optional

from twitch.twitchAuthor import TwitchAuthor
from twitch.twitchConfigurationType import TwitchConfigurationType
from twitch.twitchMessageable import TwitchMessageable


class TwitchContext(TwitchMessageable):

    def getAuthor(self) -> TwitchAuthor:
        pass

    def getAuthorDisplayName(self) -> str:
        pass

    def getAuthorId(self) -> str:
        pass

    def getAuthorName(self) -> str:
        pass

    def getMessageContent(self) -> Optional[str]:
        pass

    def getTwitchChannelName(self) -> str:
        pass

    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        pass

    def isAuthorMod(self) -> bool:
        pass

    async def send(self, message: str):
        pass
