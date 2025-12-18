from typing import Any

from ..chatterPreferredNameHelperInterface import ChatterPreferredNameHelperInterface
from ...exceptions import ChatterPreferredNameFeatureIsDisabledException
from ...models.chatterPreferredNameData import ChatterPreferredNameData


class StubChatterPreferredNameHelper(ChatterPreferredNameHelperInterface):

    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> ChatterPreferredNameData | None:
        # this method is intentionally empty
        return None

    async def set(
        self,
        chatterUserId: str,
        preferredName: str | Any | None,
        twitchChannelId: str,
    ) -> ChatterPreferredNameData:
        raise ChatterPreferredNameFeatureIsDisabledException()
