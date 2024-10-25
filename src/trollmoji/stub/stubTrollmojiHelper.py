from ..trollmojiHelperInterface import TrollmojiHelperInterface


class StubTrollmojiHelper(TrollmojiHelperInterface):

    async def getEmote(
        self,
        emoteText: str | None,
        twitchEmoteChannelId: str
    ) -> str | None:
        # this method is intentionally empty
        return None

    async def getGottemEmote(self) -> str | None:
        # this method is intentionally empty
        return None

    async def getHypeEmote(self) -> str | None:
        # this method is intentionally empty
        return None

    async def getShrugEmote(self) -> str | None:
        # this method is intentionally empty
        return None

    async def getThumbsDownEmote(self) -> str | None:
        # this method is intentionally empty
        return None

    async def getThumbsUpEmote(self) -> str | None:
        # this method is intentionally empty
        return None
