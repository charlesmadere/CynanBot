from abc import ABC, abstractmethod

from ..twitchChatMessageFragmentGif import TwitchChatMessageFragmentGif as LocalChatMessageFragmentGif
from ..twitchChatMessageFragmentType import TwitchChatMessageFragmentType as LocalChatMessageFragmentType
from ..twitchEmoteImageFormat import TwitchEmoteImageFormat as LocalEmoteImageFormat
from ...api.models.twitchChatMessageFragmentGif import TwitchChatMessageFragmentGif as ApiChatMessageFragmentGif
from ...api.models.twitchChatMessageFragmentType import TwitchChatMessageFragmentType as ApiChatMessageFragmentType
from ...api.models.twitchEmoteImageFormat import TwitchEmoteImageFormat as ApiEmoteImageFormat


class TwitchLocalModelsMapperInterface(ABC):

    @abstractmethod
    async def mapChatMessageFragmentGif(
        self,
        chatMessageFragmentGif: ApiChatMessageFragmentGif | None,
    ) -> LocalChatMessageFragmentGif | None:
        pass

    @abstractmethod
    async def mapChatMessageFragmentType(
        self,
        chatMessageFragmentType: ApiChatMessageFragmentType | None,
    ) -> LocalChatMessageFragmentType | None:
        pass

    @abstractmethod
    async def mapEmoteImageFormat(
        self,
        emoteImageFormat: ApiEmoteImageFormat | None,
    ) -> LocalEmoteImageFormat | None:
        pass
