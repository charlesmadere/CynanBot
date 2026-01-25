from typing import Final

from ..trollmojiHelperInterface import TrollmojiHelperInterface
from ...misc import utils as utils


class StubTrollmojiHelper(TrollmojiHelperInterface):

    def __init__(
        self,
        bombEmoteBackup: str = '💣',
        explodedEmoteBackup: str = '💥',
        gottemEmoteBackup: str = 'RIPBOZO',
        hypeEmoteBackup: str = '‼️',
    ):
        if not utils.isValidStr(bombEmoteBackup):
            raise TypeError(f'bombEmoteBackup argument is malformed: \"{bombEmoteBackup}\"')
        elif not utils.isValidStr(explodedEmoteBackup):
            raise TypeError(f'explodedEmoteBackup argument is malformed: \"{explodedEmoteBackup}\"')
        elif not utils.isValidStr(gottemEmoteBackup):
            raise TypeError(f'gottemEmoteBackup argument is malformed: \"{gottemEmoteBackup}\"')
        elif not utils.isValidStr(hypeEmoteBackup):
            raise TypeError(f'hypeEmoteBackup argument is malformed: \"{hypeEmoteBackup}\"')

        self.__bombEmoteBackup: Final[str] = bombEmoteBackup
        self.__explodedEmoteBackup: Final[str] = explodedEmoteBackup
        self.__gottemEmoteBackup: Final[str] = gottemEmoteBackup
        self.__hypeEmoteBackup: Final[str] = hypeEmoteBackup

    async def getBombEmote(self) -> str | None:
        # this method is intentionally empty
        return None

    async def getBombEmoteOrBackup(self) -> str:
        bombEmote = await self.getBombEmote()

        if utils.isValidStr(bombEmote):
            return bombEmote
        else:
            return self.__bombEmoteBackup

    async def getDinkDonkEmote(self) -> str | None:
        # this method is intentionally empty
        return None

    async def getEmote(
        self,
        emoteText: str | None,
        twitchEmoteChannelId: str,
    ) -> str | None:
        # this method is intentionally empty
        return None

    async def getExplodedEmote(self) -> str | None:
        # this method is intentionally empty
        return None

    async def getExplodedEmoteOrBackup(self) -> str:
        explodedEmote = await self.getExplodedEmote()

        if utils.isValidStr(explodedEmote):
            return explodedEmote
        else:
            return self.__explodedEmoteBackup

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

    async def getHypeEmoteOrBackup(self) -> str:
        hypeEmote = await self.getHypeEmote()

        if utils.isValidStr(hypeEmote):
            return hypeEmote
        else:
            return self.__hypeEmoteBackup

    async def getShrugEmote(self) -> str | None:
        # this method is intentionally empty
        return None

    async def getThumbsDownEmote(self) -> str | None:
        # this method is intentionally empty
        return None

    async def getThumbsUpEmote(self) -> str | None:
        # this method is intentionally empty
        return None
