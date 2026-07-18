from typing import Final

import pytest

from src.twitch.api.models.twitchChatMessageFragmentType import \
    TwitchChatMessageFragmentType as ApiChatMessageFragmentType
from src.twitch.localModels.mapper.twitchLocalModelsMapper import TwitchLocalModelsMapper
from src.twitch.localModels.mapper.twitchLocalModelsMapperInterface import TwitchLocalModelsMapperInterface
from src.twitch.localModels.twitchChatMessageFragmentType import \
    TwitchChatMessageFragmentType as LocalChatMessageFragmentType


class TestTwitchLocalModelsMapper:

    mapper: Final[TwitchLocalModelsMapperInterface] = TwitchLocalModelsMapper()

    @pytest.mark.asyncio
    async def test_mapChatMessageFragmentType_withAll(self):
        results: set[LocalChatMessageFragmentType | None] = set()

        for chatMessageFragmentType in ApiChatMessageFragmentType:
            result = await self.mapper.mapChatMessageFragmentType(chatMessageFragmentType)
            results.add(result)

        assert len(results) == len(LocalChatMessageFragmentType)

    @pytest.mark.asyncio
    async def test_mapChatMessageFragmentType_withNone(self):
        result = await self.mapper.mapChatMessageFragmentType(None)
        assert result is None

    def test_sanity(self):
        assert self.mapper is not None
        assert isinstance(self.mapper, TwitchLocalModelsMapper)
        assert isinstance(self.mapper, TwitchLocalModelsMapperInterface)
