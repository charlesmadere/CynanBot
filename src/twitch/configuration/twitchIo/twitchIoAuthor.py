from typing import Any, Final

from twitchio import Chatter, PartialChatter

from ..twitchAuthor import TwitchAuthor
from ..twitchConfigurationType import TwitchConfigurationType
from ....misc import utils as utils


class TwitchIoAuthor(TwitchAuthor):

    def __init__(
        self,
        author: Chatter | PartialChatter,
    ):
        if not isinstance(author, Chatter) and not isinstance(author, PartialChatter):
            raise TypeError(f'author argument is malformed: \"{author}\"')

        self.__author: Final[Chatter | PartialChatter] = author

    def getDisplayName(self) -> str:
        displayName: str | Any | None = self.__author.display_name # type: ignore

        if not isinstance(displayName, str):
            raise RuntimeError(f'displayName value is missing! ({displayName=}) ({self.__author=})')

        return displayName

    def getId(self) -> str:
        authorId: str | Any | None = self.__author.id # type: ignore

        if not isinstance(authorId, str):
            raise RuntimeError(f'authorId value is missing! ({authorId=}) ({self.__author=})')

        return authorId

    def getName(self) -> str:
        authorName: str | Any | None = self.__author.name

        if not isinstance(authorName, str):
            raise RuntimeError(f'authorName value is missing! ({authorName=}) ({self.__author=})')

        return authorName

    @property
    def isLeadMod(self) -> bool:
        if not isinstance(self.__author, Chatter):
            # unfortunately, the stupid PartialChatter class has no badge information
            return False

        badges: dict | Any | None = self.__author.badges

        if not isinstance(badges, dict) or len(badges) == 0:
            return False

        leadModerator = utils.getIntFromDict(
            d = badges,
            key = 'lead_moderator',
            fallback = utils.getIntMinSafeSize(),
        )

        return utils.isValidInt(leadModerator) and leadModerator == 1

    @property
    def isMod(self) -> bool:
        isMod: bool | Any | None = self.__author.is_mod # type: ignore

        if not isinstance(isMod, bool):
            raise RuntimeError(f'isMod value is missing! ({isMod=}) ({self.__author=})')

        return isMod or self.isLeadMod

    @property
    def isVip(self) -> bool:
        isVip: bool | Any | None = self.__author.is_vip # type: ignore

        if not isinstance(isVip, bool):
            raise RuntimeError(f'isVip value is missing! ({isVip=}) ({self.__author=})')

        return isVip

    @property
    def twitchConfigurationType(self) -> TwitchConfigurationType:
        return TwitchConfigurationType.TWITCHIO
