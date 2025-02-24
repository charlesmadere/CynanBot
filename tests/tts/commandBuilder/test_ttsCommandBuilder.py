import pytest

from src.tts.commandBuilder.ttsCommandBuilder import TtsCommandBuilder
from src.tts.commandBuilder.ttsCommandBuilderInterface import TtsCommandBuilderInterface
from src.tts.ttsCheerDonation import TtsCheerDonation
from src.tts.ttsEvent import TtsEvent
from src.tts.ttsProvider import TtsProvider
from src.tts.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from src.tts.ttsSubscriptionDonation import TtsSubscriptionDonation
from src.twitch.api.models.twitchSubscriberTier import TwitchSubscriberTier


class TestTtsCommandBuilder:

    commandBuilder: TtsCommandBuilderInterface = TtsCommandBuilder()

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
    async def test_buildDonationPrefix_withSubscriptionDonation(self):
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

    def test_sanity(self):
        assert self.commandBuilder is not None
        assert isinstance(self.commandBuilder, TtsCommandBuilder)
        assert isinstance(self.commandBuilder, TtsCommandBuilderInterface)
