from typing import Optional

from twitch.twitchAuthor import TwitchAuthor
from twitch.twitchChannel import TwitchChannel
from twitch.twitchConfigurationType import TwitchConfigurationType


class TwitchMessage():

    def getAuthor(self) -> TwitchAuthor:
        pass

    def getAuthorId(self) -> str:
        pass

    def getAuthorName(self) -> str:
        pass

    def getChannel(self) -> TwitchChannel:
        pass

    def getContent(self) -> Optional[str]:
        pass

    def getTwitchChannelName(self) -> str:
        pass

    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        pass
