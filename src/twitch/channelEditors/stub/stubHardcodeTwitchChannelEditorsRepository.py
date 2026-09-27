from ..hardcodedTwitchChannelEditorsRepositoryInterface import HardcodedTwitchChannelEditorsRepositoryInterface


class StubHardcodedTwitchChannelEditorsRepository(HardcodedTwitchChannelEditorsRepositoryInterface):

    async def clearCaches(self):
        # this method is intentionally empty
        pass

    async def get(self, twitchChannelId: str) -> frozenset[str]:
        # this method is intentionally empty
        return frozenset()
