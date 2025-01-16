from ..trollmojiHelperInterface import TrollmojiHelperInterface
from ...misc import utils as utils


class StubTrollmojiHelper(TrollmojiHelperInterface):

    def __init__(
        self,
        gottemEmoteBackup: str = 'RIPBOZO'
    ):
        if not utils.isValidStr(gottemEmoteBackup):
            raise TypeError(f'gottemEmoteBackup argument is malformed: \"{gottemEmoteBackup}\"')

        self.__gottemEmoteBackup: str = gottemEmoteBackup

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

    async def getGottemEmoteOrBackup(self) -> str:
        gottemEmote = await self.getGottemEmote()

        if utils.isValidStr(gottemEmote):
            return gottemEmote
        else:
            return self.__gottemEmoteBackup

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
