from typing import Final

import pytest

from src.twitch.api.models.twitchChatMessageFragmentGif import TwitchChatMessageFragmentGif as ApiChatMessageFragmentGif
from src.twitch.api.models.twitchChatMessageFragmentType import \
    TwitchChatMessageFragmentType as ApiChatMessageFragmentType
from src.twitch.api.models.twitchEmoteImageFormat import TwitchEmoteImageFormat as ApiEmoteImageFormat
from src.twitch.localModels.mapper.twitchLocalModelsMapper import TwitchLocalModelsMapper
from src.twitch.localModels.mapper.twitchLocalModelsMapperInterface import TwitchLocalModelsMapperInterface
from src.twitch.localModels.twitchChatMessageFragmentGif import \
    TwitchChatMessageFragmentGif as LocalChatMessageFragmentGif
from src.twitch.localModels.twitchChatMessageFragmentType import \
    TwitchChatMessageFragmentType as LocalChatMessageFragmentType
from src.twitch.localModels.twitchEmoteImageFormat import TwitchEmoteImageFormat as LocalEmoteImageFormat


class TestTwitchLocalModelsMapper:

    mapper: Final[TwitchLocalModelsMapperInterface] = TwitchLocalModelsMapper()

    @pytest.mark.asyncio
    async def test_mapChatMessageFragmentGif(self):
        apiFragmentGif = ApiChatMessageFragmentGif(
            gifId = 'abc123',
            url = 'https://www.google.com/',
        )

        result = await self.mapper.mapChatMessageFragmentGif(apiFragmentGif)
        assert isinstance(result, LocalChatMessageFragmentGif)
        assert result.gifId == apiFragmentGif.gifId
        assert result.url == apiFragmentGif.url

    @pytest.mark.asyncio
    async def test_mapChatMessageFragmentGif_withNone(self):
        result = await self.mapper.mapChatMessageFragmentGif(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_mapChatMessageFragmentType_withAll(self):
        results: set[LocalChatMessageFragmentType | None] = set()

        for chatMessageFragmentType in ApiChatMessageFragmentType:
            result = await self.mapper.mapChatMessageFragmentType(chatMessageFragmentType)
            results.add(result)

        assert len(results) == len(LocalChatMessageFragmentType)

    @pytest.mark.asyncio
    async def test_mapChatMessageFragmentType_withCheermote(self):
        result = await self.mapper.mapChatMessageFragmentType(ApiChatMessageFragmentType.CHEERMOTE)
        assert result == LocalChatMessageFragmentType.CHEERMOTE

    @pytest.mark.asyncio
    async def test_mapChatMessageFragmentType_withEmote(self):
        result = await self.mapper.mapChatMessageFragmentType(ApiChatMessageFragmentType.EMOTE)
        assert result == LocalChatMessageFragmentType.EMOTE

    @pytest.mark.asyncio
    async def test_mapChatMessageFragmentType_withGif(self):
        result = await self.mapper.mapChatMessageFragmentType(ApiChatMessageFragmentType.GIF)
        assert result == LocalChatMessageFragmentType.GIF

    @pytest.mark.asyncio
    async def test_mapChatMessageFragmentType_withMention(self):
        result = await self.mapper.mapChatMessageFragmentType(ApiChatMessageFragmentType.MENTION)
        assert result == LocalChatMessageFragmentType.MENTION

    @pytest.mark.asyncio
    async def test_mapChatMessageFragmentType_withNone(self):
        result = await self.mapper.mapChatMessageFragmentType(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_mapChatMessageFragmentType_withText(self):
        result = await self.mapper.mapChatMessageFragmentType(ApiChatMessageFragmentType.TEXT)
        assert result == LocalChatMessageFragmentType.TEXT

    @pytest.mark.asyncio
    async def test_mapEmoteImageFormat_withAll(self):
        results: set[LocalEmoteImageFormat | None] = set()

        for emoteImageFormat in ApiEmoteImageFormat:
            result = await self.mapper.mapEmoteImageFormat(emoteImageFormat)
            results.add(result)

        assert len(results) == len(LocalEmoteImageFormat)

    @pytest.mark.asyncio
    async def test_mapEmoteImageFormat_withAnimated(self):
        result = await self.mapper.mapEmoteImageFormat(ApiEmoteImageFormat.ANIMATED)
        assert result == LocalEmoteImageFormat.ANIMATED

    @pytest.mark.asyncio
    async def test_mapEmoteImageFormat_withStatic(self):
        result = await self.mapper.mapEmoteImageFormat(ApiEmoteImageFormat.STATIC)
        assert result == LocalEmoteImageFormat.STATIC

    @pytest.mark.asyncio
    async def test_requireEmoteImageFormat_withAnimated(self):
        result = await self.mapper.requireEmoteImageFormat(ApiEmoteImageFormat.ANIMATED)
        assert result == LocalEmoteImageFormat.ANIMATED

    @pytest.mark.asyncio
    async def test_requireEmoteImageFormat_withNone(self):
        result: LocalEmoteImageFormat | None = None

        with pytest.raises(ValueError):
            await self.mapper.requireEmoteImageFormat(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireEmoteImageFormat_withStatic(self):
        result = await self.mapper.requireEmoteImageFormat(ApiEmoteImageFormat.STATIC)
        assert result == LocalEmoteImageFormat.STATIC

    def test_sanity(self):
        assert self.mapper is not None
        assert isinstance(self.mapper, TwitchLocalModelsMapper)
        assert isinstance(self.mapper, TwitchLocalModelsMapperInterface)
