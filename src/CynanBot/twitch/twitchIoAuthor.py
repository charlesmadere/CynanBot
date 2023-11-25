from typing import Union

from twitchio import Chatter, PartialChatter

from twitch.twitchAuthor import TwitchAuthor
from twitch.twitchConfigurationType import TwitchConfigurationType


class TwitchIoAuthor(TwitchAuthor):

    def __init__(self, author: Union[Chatter, PartialChatter]):
        if not isinstance(author, Chatter) and not isinstance(author, PartialChatter):
            raise ValueError(f'author argument is malformed: \"{author}\"')

        self.__author: Union[Chatter, PartialChatter] = author

    def getDisplayName(self) -> str:
        return self.__author.display_name

    def getId(self) -> str:
        return str(self.__author.id)

    def getName(self) -> str:
        return self.__author.name

    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        return TwitchConfigurationType.TWITCHIO

    def isMod(self) -> bool:
        return self.__author.is_mod

    def isVip(self) -> bool:
        return self.__author.is_vip
