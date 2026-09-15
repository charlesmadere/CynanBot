from ..twitchChannelEditorsRepositoryInterface import TwitchChannelEditorsRepositoryInterface


class StubTwitchChannelEditorsRepository(TwitchChannelEditorsRepositoryInterface):

    async def clearCaches(self):
        # this method is intentionally empty
        pass

    async def fetchEditorIds(
        self,
        twitchChannelId: str,
        forceRefresh: bool = False,
    ) -> frozenset[str]:
        # this method is intentionally empty
        return frozenset()

    async def isEditor(
        self,
        chatterUserId: str,
        twitchChannelId: str,
        forceRefresh: bool = False,
    ) -> bool:
        # this method is intentionally empty
        return False
