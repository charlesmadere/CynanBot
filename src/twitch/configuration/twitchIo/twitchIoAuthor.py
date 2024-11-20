from typing import Union

from twitchio import Chatter, PartialChatter

from ..twitchAuthor import TwitchAuthor
from ..twitchConfigurationType import TwitchConfigurationType


class TwitchIoAuthor(TwitchAuthor):

    def __init__(self, author: Union[Chatter, PartialChatter]):
        if not isinstance(author, Chatter) and not isinstance(author, PartialChatter):
            raise TypeError(f'author argument is malformed: \"{author}\"')

        self.__author: Union[Chatter, PartialChatter] = author

    def getDisplayName(self) -> str:
        if isinstance(self.__author, PartialChatter):
            raise TypeError(f'displayName property is not available for type ({PartialChatter=}) ({self.__author=})')

        displayName: str | None = self.__author.display_name

        if not isinstance(displayName, str):
            raise RuntimeError(f'displayName value is missing! ({displayName=}) ({self.__author=})')

        return displayName

    def getId(self) -> str:
        if isinstance(self.__author, PartialChatter):
            raise TypeError(f'id property is not available for type ({PartialChatter=}) ({self.__author=})')

        authorId: str | None = self.__author.id

        if not isinstance(authorId, str):
            raise RuntimeError(f'authorId value is missing! ({authorId=}) ({self.__author=})')

        return authorId

    def getName(self) -> str:
        authorName: str | None = self.__author.name

        if not isinstance(authorName, str):
            raise RuntimeError(f'authorName value is missing! ({authorName=}) ({self.__author=})')

        return authorName

    def isMod(self) -> bool:
        if isinstance(self.__author, PartialChatter):
            raise TypeError(f'isMod property is not available for type ({PartialChatter=}) ({self.__author=})')

        isMod: bool | None = self.__author.is_mod

        if not isinstance(isMod, bool):
            raise RuntimeError(f'isMod value is missing! ({isMod=}) ({self.__author=})')

        return isMod

    def isVip(self) -> bool:
        if isinstance(self.__author, PartialChatter):
            raise TypeError(f'isVip property is not available for type ({PartialChatter=}) ({self.__author=})')

        isVip: bool | None = self.__author.is_vip

        if not isinstance(isVip, bool):
            raise RuntimeError(f'isVip value is missing! ({isVip=}) ({self.__author=})')

        return isVip

    @property
    def twitchConfigurationType(self) -> TwitchConfigurationType:
        return TwitchConfigurationType.TWITCHIO
