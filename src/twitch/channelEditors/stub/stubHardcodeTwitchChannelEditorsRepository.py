from ..hardcodedTwitchChannelEditorsRepositoryInterface import HardcodedTwitchChannelEditorsRepositoryInterface


class StubHardcodedTwitchChannelEditorsRepository(HardcodedTwitchChannelEditorsRepositoryInterface):

    async def get(self, twitchChannelId: str) -> frozenset[str]:
        # this method is intentionally empty
        return frozenset()
