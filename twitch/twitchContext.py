from typing import Optional

from twitch.twitchContextType import TwitchContextType
from twitch.twitchMessageable import TwitchMessageable


class TwitchContext(TwitchMessageable):

    def getAuthorId(self) -> str:
        pass

    def getAuthorName(self) -> str:
        pass

    def getMessageContent(self) -> Optional[str]:
        pass

    def getTwitchChannelName(self) -> str:
        pass

    def getTwitchContextType(self) -> TwitchContextType:
        pass

    async def send(self, message: str):
        pass
