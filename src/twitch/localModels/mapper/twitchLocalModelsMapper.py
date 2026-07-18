from .twitchLocalModelsMapperInterface import TwitchLocalModelsMapperInterface
from ..twitchChatMessageFragmentCheermote import TwitchChatMessageFragmentCheermote as LocalChatMessageFragmentCheermote
from ..twitchChatMessageFragmentEmote import TwitchChatMessageFragmentEmote as LocalChatMessageFragmentEmote
from ..twitchChatMessageFragmentGif import TwitchChatMessageFragmentGif as LocalChatMessageFragmentGif
from ..twitchChatMessageFragmentType import TwitchChatMessageFragmentType as LocalChatMessageFragmentType
from ..twitchEmoteImageFormat import TwitchEmoteImageFormat as LocalEmoteImageFormat
from ...api.models.twitchChatMessageFragmentCheermote import \
    TwitchChatMessageFragmentCheermote as ApiChatMessageFragmentCheermote
from ...api.models.twitchChatMessageFragmentEmote import TwitchChatMessageFragmentEmote as ApiChatMessageFragmentEmote
from ...api.models.twitchChatMessageFragmentGif import TwitchChatMessageFragmentGif as ApiChatMessageFragmentGif
from ...api.models.twitchChatMessageFragmentType import TwitchChatMessageFragmentType as ApiChatMessageFragmentType
from ...api.models.twitchEmoteImageFormat import TwitchEmoteImageFormat as ApiEmoteImageFormat


class TwitchLocalModelsMapper(TwitchLocalModelsMapperInterface):

    async def mapChatMessageFragmentCheermote(
        self,
        chatMessageFragmentCheermote: ApiChatMessageFragmentCheermote | None,
    ) -> LocalChatMessageFragmentCheermote | None:
        if chatMessageFragmentCheermote is None:
            return None

        return LocalChatMessageFragmentCheermote(
            bits = chatMessageFragmentCheermote.bits,
            tier = chatMessageFragmentCheermote.tier,
            prefix = chatMessageFragmentCheermote.prefix,
        )

    async def mapChatMessageFragmentEmote(
        self,
        chatMessageFragmentEmote: ApiChatMessageFragmentEmote | None,
    ) -> LocalChatMessageFragmentEmote | None:
        if chatMessageFragmentEmote is None:
            return None

        imageFormats: set[LocalEmoteImageFormat] = set()

        for apiImageFormat in chatMessageFragmentEmote.imageFormats:
            imageFormat = await self.requireEmoteImageFormat(apiImageFormat)
            imageFormats.add(imageFormat)

        return LocalChatMessageFragmentEmote(
            imageFormats = frozenset(imageFormats),
            emoteId = chatMessageFragmentEmote.emoteId,
            emoteSetId = chatMessageFragmentEmote.emoteSetId,
            ownerId = chatMessageFragmentEmote.ownerId,
        )

    async def mapChatMessageFragmentGif(
        self,
        chatMessageFragmentGif: ApiChatMessageFragmentGif | None,
    ) -> LocalChatMessageFragmentGif | None:
        if chatMessageFragmentGif is None:
            return None

        return LocalChatMessageFragmentGif(
            gifId = chatMessageFragmentGif.gifId,
            url = chatMessageFragmentGif.url,
        )

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

    async def requireEmoteImageFormat(
        self,
        emoteImageFormat: ApiEmoteImageFormat | None,
    ) -> LocalEmoteImageFormat:
        result = await self.mapEmoteImageFormat(
            emoteImageFormat = emoteImageFormat,
        )

        if result is None:
            raise ValueError(f'Unable to map \"{emoteImageFormat}\" into LocalEmoteImageFormat value!')

        return result
