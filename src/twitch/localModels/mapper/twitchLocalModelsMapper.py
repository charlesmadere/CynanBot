from .twitchLocalModelsMapperInterface import TwitchLocalModelsMapperInterface

from ..twitchChatMessageFragmentType import TwitchChatMessageFragmentType as LocalChatMessageFragmentType
from ..twitchEmoteImageFormat import TwitchEmoteImageFormat as LocalEmoteImageFormat
from ...api.models.twitchChatMessageFragmentType import TwitchChatMessageFragmentType as ApiChatMessageFragmentType
from ...api.models.twitchEmoteImageFormat import TwitchEmoteImageFormat as ApiEmoteImageFormat


class TwitchLocalModelsMapper(TwitchLocalModelsMapperInterface):

    async def mapChatMessageFragmentType(
        self,
        chatMessageFragmentType: ApiChatMessageFragmentType | None,
    ) -> LocalChatMessageFragmentType | None:
        if chatMessageFragmentType is None:
            return None

        match chatMessageFragmentType:
            case ApiChatMessageFragmentType.CHEERMOTE: return LocalChatMessageFragmentType.CHEERMOTE
            case ApiChatMessageFragmentType.EMOTE: return LocalChatMessageFragmentType.EMOTE
            case ApiChatMessageFragmentType.GIF: return LocalChatMessageFragmentType.GIF
            case ApiChatMessageFragmentType.MENTION: return LocalChatMessageFragmentType.MENTION
            case ApiChatMessageFragmentType.TEXT: return LocalChatMessageFragmentType.TEXT

    async def mapEmoteImageFormat(
        self,
        emoteImageFormat: ApiEmoteImageFormat | None,
    ) -> LocalEmoteImageFormat | None:
        if emoteImageFormat is None:
            return None

        match emoteImageFormat:
            case ApiEmoteImageFormat.ANIMATED: return LocalEmoteImageFormat.ANIMATED
            case ApiEmoteImageFormat.STATIC: return LocalEmoteImageFormat.STATIC
