from typing import Collection

from frozenlist import FrozenList

from .twitchLocalModelsMapperInterface import TwitchLocalModelsMapperInterface
from ..twitchChatMessageFragment import TwitchChatMessageFragment as LocalChatMessageFragment
from ..twitchChatMessageFragmentCheermote import TwitchChatMessageFragmentCheermote as LocalChatMessageFragmentCheermote
from ..twitchChatMessageFragmentEmote import TwitchChatMessageFragmentEmote as LocalChatMessageFragmentEmote
from ..twitchChatMessageFragmentGif import TwitchChatMessageFragmentGif as LocalChatMessageFragmentGif
from ..twitchChatMessageFragmentMention import TwitchChatMessageFragmentMention as LocalChatMessageFragmentMention
from ..twitchChatMessageFragmentType import TwitchChatMessageFragmentType as LocalChatMessageFragmentType
from ..twitchCheerMetadata import TwitchCheerMetadata as LocalCheerMetadata
from ..twitchEmoteImageFormat import TwitchEmoteImageFormat as LocalEmoteImageFormat
from ..twitchWatchStreak import TwitchWatchStreak as LocalWatchStreak
from ...api.models.twitchChatMessageFragment import TwitchChatMessageFragment as ApiChatMessageFragment
from ...api.models.twitchChatMessageFragmentCheermote import \
    TwitchChatMessageFragmentCheermote as ApiChatMessageFragmentCheermote
from ...api.models.twitchChatMessageFragmentEmote import TwitchChatMessageFragmentEmote as ApiChatMessageFragmentEmote
from ...api.models.twitchChatMessageFragmentGif import TwitchChatMessageFragmentGif as ApiChatMessageFragmentGif
from ...api.models.twitchChatMessageFragmentMention import \
    TwitchChatMessageFragmentMention as ApiChatMessageFragmentMention
from ...api.models.twitchChatMessageFragmentType import TwitchChatMessageFragmentType as ApiChatMessageFragmentType
from ...api.models.twitchCheerMetadata import TwitchCheerMetadata as ApiCheerMetadata
from ...api.models.twitchEmoteImageFormat import TwitchEmoteImageFormat as ApiEmoteImageFormat
from ...api.models.twitchWatchStreak import TwitchWatchStreak as ApiWatchStreak


class TwitchLocalModelsMapper(TwitchLocalModelsMapperInterface):

    async def mapChatMessageFragment(
        self,
        chatMessageFragment: ApiChatMessageFragment | None,
    ) -> LocalChatMessageFragment | None:
        if chatMessageFragment is None:
            return None

        cheermote = await self.mapChatMessageFragmentCheermote(chatMessageFragment.cheermote)
        emote = await self.mapChatMessageFragmentEmote(chatMessageFragment.emote)
        gif = await self.mapChatMessageFragmentGif(chatMessageFragment.gif)
        mention = await self.mapChatMessageFragmentMention(chatMessageFragment.mention)
        fragmentType = await self.requireChatMessageFragmentType(chatMessageFragment.fragmentType)

        return LocalChatMessageFragment(
            text = chatMessageFragment.text,
            cheermote = cheermote,
            emote = emote,
            gif = gif,
            mention = mention,
            fragmentType = fragmentType,
        )

    async def mapChatMessageFragments(
        self,
        chatMessageFragments: Collection[ApiChatMessageFragment] | None,
    ) -> FrozenList[LocalChatMessageFragment]:
        fragments: FrozenList[LocalChatMessageFragment] = FrozenList()

        if chatMessageFragments is not None:
            for chatMessageFragment in chatMessageFragments:
                fragment = await self.requireChatMessageFragment(chatMessageFragment)
                fragments.append(fragment)

        fragments.freeze()
        return fragments

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

    async def mapChatMessageFragmentMention(
        self,
        chatMessageFragmentMention: ApiChatMessageFragmentMention | None,
    ) -> LocalChatMessageFragmentMention | None:
        if chatMessageFragmentMention is None:
            return None

        return LocalChatMessageFragmentMention(
            userId = chatMessageFragmentMention.userId,
            userLogin = chatMessageFragmentMention.userLogin,
            userName = chatMessageFragmentMention.userName,
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

    async def mapCheerMetadata(
        self,
        cheerMetadata: ApiCheerMetadata | None,
    ) -> LocalCheerMetadata | None:
        if cheerMetadata is None:
            return None

        return LocalCheerMetadata(
            bits = cheerMetadata.bits,
        )

    async def mapEmoteImageFormat(
        self,
        emoteImageFormat: ApiEmoteImageFormat | None,
    ) -> LocalEmoteImageFormat | None:
        if emoteImageFormat is None:
            return None

        match emoteImageFormat:
            case ApiEmoteImageFormat.ANIMATED: return LocalEmoteImageFormat.ANIMATED
            case ApiEmoteImageFormat.STATIC: return LocalEmoteImageFormat.STATIC

    async def mapWatchStreak(
        self,
        watchStreak: ApiWatchStreak | None,
    ) -> LocalWatchStreak | None:
        if watchStreak is None:
            return None

        return LocalWatchStreak(
            channelPointsAwarded = watchStreak.channelPointsAwarded,
            streakCount = watchStreak.streakCount,
        )

    async def requireChatMessageFragment(
        self,
        chatMessageFragment: ApiChatMessageFragment | None,
    ) -> LocalChatMessageFragment:
        result = await self.mapChatMessageFragment(
            chatMessageFragment = chatMessageFragment,
        )

        if result is None:
            raise ValueError(f'Unable to map \"{chatMessageFragment}\" into LocalChatMessageFragment value!')

        return result

    async def requireChatMessageFragmentType(
        self,
        chatMessageFragmentType: ApiChatMessageFragmentType | None,
    ) -> LocalChatMessageFragmentType:
        result = await self.mapChatMessageFragmentType(
            chatMessageFragmentType = chatMessageFragmentType,
        )

        if result is None:
            raise ValueError(f'Unable to map \"{chatMessageFragmentType}\" into LocalChatMessageFragmentType value!')

        return result

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
