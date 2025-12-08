from ..nickNameHelperInterface import NickNameHelperInterface
from ...models.nickNameData import NickNameData


class StubNickNameHelper(NickNameHelperInterface):

    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> NickNameData | None:
        # this method is intentionally empty
        return None
