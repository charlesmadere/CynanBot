from ..chatterPreferredNameHelperInterface import ChatterPreferredNameHelperInterface
from ...models.chatterPreferredNameData import ChatterPreferredNameData


class StubChatterPreferredNameHelper(ChatterPreferredNameHelperInterface):

    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> ChatterPreferredNameData | None:
        # this method is intentionally empty
        return None
