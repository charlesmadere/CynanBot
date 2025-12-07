from typing import Final

import pytest

from src.tts.commandBuilder.ttsCommandBuilder import TtsCommandBuilder
from src.tts.commandBuilder.ttsCommandBuilderInterface import TtsCommandBuilderInterface
from src.tts.models.ttsCheerDonation import TtsCheerDonation
from src.tts.models.ttsEvent import TtsEvent
from src.tts.models.ttsProvider import TtsProvider
from src.tts.models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from src.tts.models.ttsSubscriptionDonation import TtsSubscriptionDonation
from src.twitch.api.models.twitchSubscriberTier import TwitchSubscriberTier


class TestTtsCommandBuilder:

    commandBuilder: Final[TtsCommandBuilderInterface] = TtsCommandBuilder(
        nickNameHelper = None,
    )

    @pytest.mark.asyncio
    async def test_buildDonationPrefix_withCheerDonation(self):
        donation = TtsCheerDonation(
            bits = 100
        )

        ttsEvent = TtsEvent(
            message = 'Hello, World!',
            twitchChannel = 'smCharles',
            twitchChannelId = 'abc123',
            userId = 'def456',
            userName = 'stashiocat',
            donation = donation,
            provider = TtsProvider.DEC_TALK,
            providerOverridableStatus = TtsProviderOverridableStatus.THIS_EVENT_DISABLED,
            raidInfo = None
        )

        result = await self.commandBuilder.buildDonationPrefix(ttsEvent)
        assert result == 'stashiocat cheered 100!'

    @pytest.mark.asyncio
    async def test_buildDonationPrefix_withNoDonation(self):
        ttsEvent = TtsEvent(
            message = 'Hello, World!',
            twitchChannel = 'smCharles',
            twitchChannelId = 'abc123',
            userId = 'def456',
            userName = 'stashiocat',
            donation = None,
            provider = TtsProvider.DEC_TALK,
            providerOverridableStatus = TtsProviderOverridableStatus.THIS_EVENT_DISABLED,
            raidInfo = None
        )

        result = await self.commandBuilder.buildDonationPrefix(ttsEvent)
        assert result is None

    @pytest.mark.asyncio
    async def test_buildDonationPrefix_withNone(self):
        result = await self.commandBuilder.buildDonationPrefix(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_buildDonationPrefix_withResubscriptionDonation(self):
        donation = TtsSubscriptionDonation(
            isAnonymous = False,
            cumulativeMonths = None,
            durationMonths = None,
            numberOfGiftedSubs = None,
            tier = TwitchSubscriberTier.TIER_ONE
        )

        ttsEvent = TtsEvent(
            message = 'Hello, World!',
            twitchChannel = 'smCharles',
            twitchChannelId = 'abc123',
            userId = 'def456',
            userName = 'stashiocat',
            donation = donation,
            provider = TtsProvider.DEC_TALK,
            providerOverridableStatus = TtsProviderOverridableStatus.THIS_EVENT_DISABLED,
            raidInfo = None
        )

        result = await self.commandBuilder.buildDonationPrefix(ttsEvent)
        assert result == 'stashiocat subscribed!'

    @pytest.mark.asyncio
    async def test_buildDonationPrefix_withSubscriptionDonation1(self):
        donation = TtsSubscriptionDonation(
            isAnonymous = False,
            cumulativeMonths = None,
            durationMonths = None,
            numberOfGiftedSubs = 5,
            tier = TwitchSubscriberTier.TIER_TWO
        )

        ttsEvent = TtsEvent(
            message = 'Hello, World!',
            twitchChannel = 'smCharles',
            twitchChannelId = 'abc123',
            userId = 'def456',
            userName = 'stashiocat',
            donation = donation,
            provider = TtsProvider.DEC_TALK,
            providerOverridableStatus = TtsProviderOverridableStatus.THIS_EVENT_DISABLED,
            raidInfo = None
        )

        result = await self.commandBuilder.buildDonationPrefix(ttsEvent)
        assert result == 'stashiocat gifted 5 subs!'

    @pytest.mark.asyncio
    async def test_buildDonationPrefix_withSubscriptionDonation2(self):
        donation = TtsSubscriptionDonation(
            isAnonymous = False,
            cumulativeMonths = None,
            durationMonths = None,
            numberOfGiftedSubs = 1,
            tier = TwitchSubscriberTier.TIER_ONE
        )

        ttsEvent = TtsEvent(
            message = None,
            twitchChannel = 'smCharles',
            twitchChannelId = 'abc123',
            userId = 'def456',
            userName = 'MAERKLiG',
            donation = donation,
            provider = TtsProvider.DEC_TALK,
            providerOverridableStatus = TtsProviderOverridableStatus.THIS_EVENT_DISABLED,
            raidInfo = None
        )

        result = await self.commandBuilder.buildDonationPrefix(ttsEvent)
        assert result == 'MAERKLiG gifted 1 sub!'

    def test_sanity(self):
        assert self.commandBuilder is not None
        assert isinstance(self.commandBuilder, TtsCommandBuilder)
        assert isinstance(self.commandBuilder, TtsCommandBuilderInterface)
