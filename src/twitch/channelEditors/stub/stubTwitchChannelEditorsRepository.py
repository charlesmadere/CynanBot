from ..twitchChannelEditorsRepositoryInterface import TwitchChannelEditorsRepositoryInterface


class StubTwitchChannelEditorsRepository(TwitchChannelEditorsRepositoryInterface):

    async def clearCaches(self):
        # this method is intentionally empty
        pass

    async def isEditor(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> bool:
        # this method is intentionally empty
        return False
