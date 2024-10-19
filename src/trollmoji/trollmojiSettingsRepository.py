from .trollmojiDetails import TrollmojiDetails
from .trollmojiSettingsRepositoryInterface import TrollmojiSettingsRepositoryInterface


class TrollmojiSettingsRepository(TrollmojiSettingsRepositoryInterface):

    async def clearCaches(self):
        # TODO
        pass

    async def getGottemEmote(self) -> TrollmojiDetails | None:
        # TODO
        return None

    async def getHypeEmote(self) -> TrollmojiDetails | None:
        # TODO
        return None
