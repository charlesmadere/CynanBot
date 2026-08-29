from typing import Final

import pytest
from frozenlist import FrozenList

from src.twitch.api.models.twitchBitsUseType import TwitchBitsUseType as ApiBitsUseType
from src.twitch.api.models.twitchChatMessageFragment import \
    TwitchChatMessageFragment as ApiChatMessageFragment
from src.twitch.api.models.twitchChatMessageFragmentCheermote import \
    TwitchChatMessageFragmentCheermote as ApiChatMessageFragmentCheermote
from src.twitch.api.models.twitchChatMessageFragmentEmote import \
    TwitchChatMessageFragmentEmote as ApiChatMessageFragmentEmote
from src.twitch.api.models.twitchChatMessageFragmentGif import TwitchChatMessageFragmentGif as ApiChatMessageFragmentGif
from src.twitch.api.models.twitchChatMessageFragmentMention import \
    TwitchChatMessageFragmentMention as ApiChatMessageFragmentMention
from src.twitch.api.models.twitchChatMessageFragmentType import \
    TwitchChatMessageFragmentType as ApiChatMessageFragmentType
from src.twitch.api.models.twitchCheerMetadata import TwitchCheerMetadata as ApiCheerMetadata
from src.twitch.api.models.twitchCommunitySubGift import TwitchCommunitySubGift as ApiCommunitySubGift
from src.twitch.api.models.twitchCustomPowerUp import TwitchCustomPowerUp as ApiCustomPowerUp
from src.twitch.api.models.twitchCustomPowerUpData import TwitchCustomPowerUpData as ApiCustomPowerUpData
from src.twitch.api.models.twitchEmoteImageFormat import TwitchEmoteImageFormat as ApiEmoteImageFormat
from src.twitch.api.models.twitchHypeTrainType import TwitchHypeTrainType as ApiHypeTrainType
from src.twitch.api.models.twitchPollChoice import TwitchPollChoice as ApiPollChoice
from src.twitch.api.models.twitchPollStatus import TwitchPollStatus as ApiPollStatus
from src.twitch.api.models.twitchResubscriptionMessage import TwitchResubscriptionMessage as ApiResubscriptionMessage
from src.twitch.api.models.twitchResubscriptionMessageEmote import \
    TwitchResubscriptionMessageEmote as ApiResubscriptionMessageEmote
from src.twitch.api.models.twitchSubscriberTier import TwitchSubscriberTier as ApiSubscriberTier
from src.twitch.api.models.twitchWatchStreak import TwitchWatchStreak as ApiWatchStreak
from src.twitch.api.models.twitchWebsocketSubscriptionType import \
    TwitchWebsocketSubscriptionType as ApiWebsocketSubscriptionType
from src.twitch.localModels.mapper.twitchLocalModelsMapper import TwitchLocalModelsMapper
from src.twitch.localModels.mapper.twitchLocalModelsMapperInterface import TwitchLocalModelsMapperInterface
from src.twitch.localModels.twitchBitsUseType import TwitchBitsUseType as LocalBitsUseType
from src.twitch.localModels.twitchChatMessageFragment import \
    TwitchChatMessageFragment as LocalChatMessageFragment
from src.twitch.localModels.twitchChatMessageFragmentCheermote import \
    TwitchChatMessageFragmentCheermote as LocalChatMessageFragmentCheermote
from src.twitch.localModels.twitchChatMessageFragmentEmote import \
    TwitchChatMessageFragmentEmote as LocalChatMessageFragmentEmote
from src.twitch.localModels.twitchChatMessageFragmentGif import \
    TwitchChatMessageFragmentGif as LocalChatMessageFragmentGif
from src.twitch.localModels.twitchChatMessageFragmentMention import \
    TwitchChatMessageFragmentMention as LocalChatMessageFragmentMention
from src.twitch.localModels.twitchChatMessageFragmentType import \
    TwitchChatMessageFragmentType as LocalChatMessageFragmentType
from src.twitch.localModels.twitchCheerMetadata import TwitchCheerMetadata as LocalCheerMetadata
from src.twitch.localModels.twitchCommunitySubGift import TwitchCommunitySubGift as LocalCommunitySubGift
from src.twitch.localModels.twitchCustomPowerUp import TwitchCustomPowerUp as LocalCustomPowerUp
from src.twitch.localModels.twitchCustomPowerUpData import TwitchCustomPowerUpData as LocalCustomPowerUpData
from src.twitch.localModels.twitchEmoteImageFormat import TwitchEmoteImageFormat as LocalEmoteImageFormat
from src.twitch.localModels.twitchHypeTrainState import TwitchHypeTrainState as LocalHypeTrainState
from src.twitch.localModels.twitchHypeTrainType import TwitchHypeTrainType as LocalHypeTrainType
from src.twitch.localModels.twitchPollChoice import TwitchPollChoice as LocalPollChoice
from src.twitch.localModels.twitchPollStatus import TwitchPollStatus as LocalPollStatus
from src.twitch.localModels.twitchResubscriptionMessage import TwitchResubscriptionMessage as LocalResubscriptionMessage
from src.twitch.localModels.twitchResubscriptionMessageEmote import \
    TwitchResubscriptionMessageEmote as LocalResubscriptionMessageEmote
from src.twitch.localModels.twitchSubscriberTier import TwitchSubscriberTier as LocalSubscriberTier
from src.twitch.localModels.twitchWatchStreak import TwitchWatchStreak as LocalWatchStreak


class TestTwitchLocalModelsMapper:

    mapper: Final[TwitchLocalModelsMapperInterface] = TwitchLocalModelsMapper()

    @pytest.mark.asyncio
    async def  test_mapBitsUseType_withAll(self):
        results: set[LocalBitsUseType | None] = set()

        for bitsUseType in ApiBitsUseType:
            result = await self.mapper.mapBitsUseType(bitsUseType)
            results.add(result)

        assert len(results) == len(LocalBitsUseType)
        assert None not in results

    @pytest.mark.asyncio
    async def  test_mapBitsUseType_withCheer(self):
        result = await self.mapper.mapBitsUseType(ApiBitsUseType.CHEER)
        assert result is LocalBitsUseType.CHEER

    @pytest.mark.asyncio
    async def  test_mapBitsUseType_withCustomPowerUp(self):
        result = await self.mapper.mapBitsUseType(ApiBitsUseType.CUSTOM_POWER_UP)
        assert result is LocalBitsUseType.CUSTOM_POWER_UP

    @pytest.mark.asyncio
    async def  test_mapBitsUseType_withPowerUp(self):
        result = await self.mapper.mapBitsUseType(ApiBitsUseType.POWER_UP)
        assert result is LocalBitsUseType.POWER_UP

    @pytest.mark.asyncio
    async def test_mapBitsUseType_withNone(self):
        result = await self.mapper.mapBitsUseType(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_mapChatMessageFragment(self):
        apiFragment = ApiChatMessageFragment(
            text = 'Hello, World!',
            cheermote = None,
            emote = None,
            gif = None,
            mention = ApiChatMessageFragmentMention(
                userId = 'abc123',
                userLogin = 'stashiocat',
                userName = 'stashiocat',
            ),
            fragmentType = ApiChatMessageFragmentType.MENTION,
        )

        result = await self.mapper.mapChatMessageFragment(apiFragment)
        assert isinstance(result, LocalChatMessageFragment)
        assert result.text == apiFragment.text
        assert result.cheermote == await self.mapper.mapChatMessageFragmentCheermote(apiFragment.cheermote)
        assert result.emote == await self.mapper.mapChatMessageFragmentEmote(apiFragment.emote)
        assert result.gif == await self.mapper.mapChatMessageFragmentGif(apiFragment.gif)
        assert result.mention == await self.mapper.mapChatMessageFragmentMention(apiFragment.mention)
        assert result.fragmentType is await self.mapper.mapChatMessageFragmentType(apiFragment.fragmentType)

    @pytest.mark.asyncio
    async def test_mapChatMessageFragment_withNone(self):
        result = await self.mapper.mapChatMessageFragment(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_mapChatMessageFragments(self):
        apiFragment = ApiChatMessageFragment(
            text = 'Hello, World!',
            cheermote = None,
            emote = None,
            gif = None,
            mention = None,
            fragmentType = ApiChatMessageFragmentType.TEXT,
        )

        result = await self.mapper.mapChatMessageFragments([ apiFragment ])
        assert isinstance(result, FrozenList)
        assert len(result) == 1
        assert result.frozen

        assert result[0] == await self.mapper.requireChatMessageFragment(apiFragment)

    @pytest.mark.asyncio
    async def test_mapChatMessageFragments_withEmptyList(self):
        result = await self.mapper.mapChatMessageFragments(list())
        assert isinstance(result, FrozenList)
        assert len(result) == 0
        assert result.frozen

    @pytest.mark.asyncio
    async def test_mapChatMessageFragments_withNone(self):
        result = await self.mapper.mapChatMessageFragments(None)
        assert isinstance(result, FrozenList)
        assert len(result) == 0
        assert result.frozen

    @pytest.mark.asyncio
    async def test_mapChatMessageFragmentCheermote(self):
        apiFragmentCheermote = ApiChatMessageFragmentCheermote(
            bits = 100,
            tier = 1,
            prefix = 'samus',
        )

        result = await self.mapper.mapChatMessageFragmentCheermote(apiFragmentCheermote)
        assert isinstance(result, LocalChatMessageFragmentCheermote)
        assert result.bits == apiFragmentCheermote.bits
        assert result.tier == apiFragmentCheermote.tier
        assert result.prefix == apiFragmentCheermote.prefix

    @pytest.mark.asyncio
    async def test_mapChatMessageFragmentCheermote_withNone(self):
        result = await self.mapper.mapChatMessageFragmentCheermote(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_mapChatMessageFragmentEmote(self):
        apiFragmentEmote = ApiChatMessageFragmentEmote(
            imageFormats = frozenset({ ApiEmoteImageFormat.ANIMATED, ApiEmoteImageFormat.STATIC }),
            emoteId = 'emoteId',
            emoteSetId = 'emoteSetId',
            ownerId = 'ownerId',
        )

        result = await self.mapper.mapChatMessageFragmentEmote(apiFragmentEmote)
        assert isinstance(result, LocalChatMessageFragmentEmote)
        assert result.emoteId == apiFragmentEmote.emoteId
        assert result.emoteSetId == apiFragmentEmote.emoteSetId
        assert result.ownerId == apiFragmentEmote.ownerId

        assert len(result.imageFormats) == len(apiFragmentEmote.imageFormats)
        assert LocalEmoteImageFormat.ANIMATED in result.imageFormats
        assert LocalEmoteImageFormat.STATIC in result.imageFormats

    @pytest.mark.asyncio
    async def test_mapChatMessageFragmentEmote_withNone(self):
        result = await self.mapper.mapChatMessageFragmentEmote(None)
        assert result is None

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
    async def test_mapChatMessageFragmentMention(self):
        apiFragmentMention = ApiChatMessageFragmentMention(
            userId = 'abc123',
            userLogin = 'stashiocat',
            userName = 'stashiocat',
        )

        result = await self.mapper.mapChatMessageFragmentMention(apiFragmentMention)
        assert isinstance(result, LocalChatMessageFragmentMention)
        assert result.userId == apiFragmentMention.userId
        assert result.userLogin == apiFragmentMention.userLogin
        assert result.userName == apiFragmentMention.userName

    @pytest.mark.asyncio
    async def test_mapChatMessageFragmentMention_withNone(self):
        result = await self.mapper.mapChatMessageFragmentMention(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_mapChatMessageFragmentType_withAll(self):
        results: set[LocalChatMessageFragmentType | None] = set()

        for chatMessageFragmentType in ApiChatMessageFragmentType:
            result = await self.mapper.mapChatMessageFragmentType(chatMessageFragmentType)
            results.add(result)

        assert len(results) == len(LocalChatMessageFragmentType)
        assert None not in results

    @pytest.mark.asyncio
    async def test_mapChatMessageFragmentType_withCheermote(self):
        result = await self.mapper.mapChatMessageFragmentType(ApiChatMessageFragmentType.CHEERMOTE)
        assert result is LocalChatMessageFragmentType.CHEERMOTE

    @pytest.mark.asyncio
    async def test_mapChatMessageFragmentType_withEmote(self):
        result = await self.mapper.mapChatMessageFragmentType(ApiChatMessageFragmentType.EMOTE)
        assert result is LocalChatMessageFragmentType.EMOTE

    @pytest.mark.asyncio
    async def test_mapChatMessageFragmentType_withGif(self):
        result = await self.mapper.mapChatMessageFragmentType(ApiChatMessageFragmentType.GIF)
        assert result is LocalChatMessageFragmentType.GIF

    @pytest.mark.asyncio
    async def test_mapChatMessageFragmentType_withMention(self):
        result = await self.mapper.mapChatMessageFragmentType(ApiChatMessageFragmentType.MENTION)
        assert result is LocalChatMessageFragmentType.MENTION

    @pytest.mark.asyncio
    async def test_mapChatMessageFragmentType_withNone(self):
        result = await self.mapper.mapChatMessageFragmentType(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_mapChatMessageFragmentType_withText(self):
        result = await self.mapper.mapChatMessageFragmentType(ApiChatMessageFragmentType.TEXT)
        assert result is LocalChatMessageFragmentType.TEXT

    @pytest.mark.asyncio
    async def test_mapCheerMetadata(self):
        apiCheerMetadata = ApiCheerMetadata(
            bits = 100,
        )

        result = await self.mapper.mapCheerMetadata(apiCheerMetadata)
        assert isinstance(result, LocalCheerMetadata)
        assert result.bits == apiCheerMetadata.bits

    @pytest.mark.asyncio
    async def test_mapCheerMetadata_withNone(self):
        result = await self.mapper.mapCheerMetadata(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_mapCommunitySubGift(self):
        apiCommunitySubGift = ApiCommunitySubGift(
            cumulativeTotal = 25,
            total = 5,
            communitySubGiftId = 'abc123',
            subTier = ApiSubscriberTier.TIER_ONE,
        )

        result = await self.mapper.mapCommunitySubGift(apiCommunitySubGift)
        assert isinstance(result, LocalCommunitySubGift)
        assert result.cumulativeTotal == apiCommunitySubGift.cumulativeTotal
        assert result.total == apiCommunitySubGift.total
        assert result.communitySubGiftId == apiCommunitySubGift.communitySubGiftId

        subTier = await self.mapper.mapSubscriberTier(apiCommunitySubGift.subTier)
        assert result.subTier is subTier

    @pytest.mark.asyncio
    async def test_mapCommunitySubGift_withNone(self):
        result = await self.mapper.mapCommunitySubGift(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_mapCustomPowerUp(self):
        apiCustomPowerUp = ApiCustomPowerUp(
            bits = 100,
            powerUpId = 'powerUpId',
            prompt = 'prompt',
            title = 'title',
        )

        result = await self.mapper.mapCustomPowerUp(apiCustomPowerUp)
        assert isinstance(result, LocalCustomPowerUp)
        assert result.bits == apiCustomPowerUp.bits
        assert result.powerUpId == apiCustomPowerUp.powerUpId
        assert result.prompt == apiCustomPowerUp.prompt
        assert result.title == apiCustomPowerUp.title

    @pytest.mark.asyncio
    async def test_mapCustomPowerUp_withNone(self):
        result = await self.mapper.mapCustomPowerUp(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_mapCustomPowerUpData(self):
        apiCustomPowerUpData = ApiCustomPowerUpData(
            rewardId = 'rewardId',
            title = 'title',
        )

        result = await self.mapper.mapCustomPowerUpData(apiCustomPowerUpData)
        assert isinstance(result, LocalCustomPowerUpData)
        assert result.rewardId == apiCustomPowerUpData.rewardId
        assert result.title == apiCustomPowerUpData.title

    @pytest.mark.asyncio
    async def test_mapCustomPowerUpData_withNone(self):
        result = await self.mapper.mapCustomPowerUpData(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_mapEmoteImageFormat_withAll(self):
        results: set[LocalEmoteImageFormat | None] = set()

        for emoteImageFormat in ApiEmoteImageFormat:
            result = await self.mapper.mapEmoteImageFormat(emoteImageFormat)
            results.add(result)

        assert len(results) == len(LocalEmoteImageFormat)
        assert None not in results

    @pytest.mark.asyncio
    async def test_mapEmoteImageFormat_withAnimated(self):
        result = await self.mapper.mapEmoteImageFormat(ApiEmoteImageFormat.ANIMATED)
        assert result is LocalEmoteImageFormat.ANIMATED

    @pytest.mark.asyncio
    async def test_mapEmoteImageFormat_withNone(self):
        result = await self.mapper.mapEmoteImageFormat(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_mapEmoteImageFormat_withStatic(self):
        result = await self.mapper.mapEmoteImageFormat(ApiEmoteImageFormat.STATIC)
        assert result is LocalEmoteImageFormat.STATIC

    @pytest.mark.asyncio
    async def test_mapHypeTrainState_withAll(self):
        results: set[LocalHypeTrainState | None] = set()

        for subscriptionType in ApiWebsocketSubscriptionType:
            result = await self.mapper.mapHypeTrainState(subscriptionType)
            results.add(result)

        for hypeTrainState in LocalHypeTrainState:
            assert hypeTrainState in results

        assert None in results

    @pytest.mark.asyncio
    async def test_mapHypeTrainState_withChannelHypeTrainBegin(self):
        result = await self.mapper.mapHypeTrainState(ApiWebsocketSubscriptionType.CHANNEL_HYPE_TRAIN_BEGIN)
        assert result is LocalHypeTrainState.BEGIN

    @pytest.mark.asyncio
    async def test_mapHypeTrainState_withChannelHypeTrainEnd(self):
        result = await self.mapper.mapHypeTrainState(ApiWebsocketSubscriptionType.CHANNEL_HYPE_TRAIN_END)
        assert result is LocalHypeTrainState.END

    @pytest.mark.asyncio
    async def test_mapHypeTrainState_withChannelHypeTrainProgress(self):
        result = await self.mapper.mapHypeTrainState(ApiWebsocketSubscriptionType.CHANNEL_HYPE_TRAIN_PROGRESS)
        assert result is LocalHypeTrainState.PROGRESS

    @pytest.mark.asyncio
    async def test_mapHypeTrainState_withNone(self):
        result = await self.mapper.mapHypeTrainState(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_mapHypeTrainType_withAll(self):
        results: set[LocalHypeTrainType | None] = set()

        for hypeTrainType in ApiHypeTrainType:
            result = await self.mapper.mapHypeTrainType(hypeTrainType)
            results.add(result)

        assert len(results) == len(LocalHypeTrainType)
        assert None not in results

    @pytest.mark.asyncio
    async def test_mapHypeTrainType_withGoldenKappa(self):
        result = await self.mapper.mapHypeTrainType(ApiHypeTrainType.GOLDEN_KAPPA)
        assert result is LocalHypeTrainType.GOLDEN_KAPPA

    @pytest.mark.asyncio
    async def test_mapHypeTrainType_withNone(self):
        result = await self.mapper.mapHypeTrainType(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_mapHypeTrainType_withRegular(self):
        result = await self.mapper.mapHypeTrainType(ApiHypeTrainType.REGULAR)
        assert result is LocalHypeTrainType.REGULAR

    @pytest.mark.asyncio
    async def test_mapHypeTrainType_withTreasure(self):
        result = await self.mapper.mapHypeTrainType(ApiHypeTrainType.TREASURE)
        assert result is LocalHypeTrainType.TREASURE

    @pytest.mark.asyncio
    async def test_mapPollChoice(self):
        apiPollChoice = ApiPollChoice(
            channelPointsVotes = 100,
            votes = 5,
            choiceId = 'abc123',
            title = 'Hello, World!',
        )

        result = await self.mapper.mapPollChoice(apiPollChoice)
        assert isinstance(result, LocalPollChoice)
        assert result.channelPointsVotes == apiPollChoice.channelPointsVotes
        assert result.votes == apiPollChoice.votes
        assert result.choiceId == apiPollChoice.choiceId
        assert result.title == apiPollChoice.title

    @pytest.mark.asyncio
    async def test_mapPollChoice_withNone(self):
        result = await self.mapper.mapPollChoice(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_mapPollChoices(self):
        apiPollChoice = ApiPollChoice(
            channelPointsVotes = 10,
            votes = 3,
            choiceId = 'def456',
            title = 'Hello, World!',
        )

        results = await self.mapper.mapPollChoices([ apiPollChoice ])
        assert isinstance(results, FrozenList)
        assert len(results) == 1
        assert results.frozen

        assert isinstance(results[0], LocalPollChoice)
        assert results[0].channelPointsVotes == apiPollChoice.channelPointsVotes
        assert results[0].votes == apiPollChoice.votes
        assert results[0].choiceId == apiPollChoice.choiceId
        assert results[0].title == apiPollChoice.title

    @pytest.mark.asyncio
    async def test_mapPollChoices_withEmptyList(self):
        result = await self.mapper.mapPollChoices(list())
        assert isinstance(result, FrozenList)
        assert len(result) == 0
        assert result.frozen

    @pytest.mark.asyncio
    async def test_mapPollChoices_withNone(self):
        result = await self.mapper.mapPollChoices(None)
        assert isinstance(result, FrozenList)
        assert len(result) == 0
        assert result.frozen

    @pytest.mark.asyncio
    async def test_mapPollStatus_withAll(self):
        results: set[LocalPollStatus | None] = set()

        for pollStatus in ApiPollStatus:
            result = await self.mapper.mapPollStatus(pollStatus)
            results.add(result)

        assert len(results) == len(LocalPollStatus)
        assert None not in results

    @pytest.mark.asyncio
    async def test_mapPollStatus_withActive(self):
        result = await self.mapper.mapPollStatus(ApiPollStatus.ACTIVE)
        assert result is LocalPollStatus.ACTIVE

    @pytest.mark.asyncio
    async def test_mapPollStatus_withArchived(self):
        result = await self.mapper.mapPollStatus(ApiPollStatus.ARCHIVED)
        assert result is LocalPollStatus.ARCHIVED

    @pytest.mark.asyncio
    async def test_mapPollStatus_withCompleted(self):
        result = await self.mapper.mapPollStatus(ApiPollStatus.COMPLETED)
        assert result is LocalPollStatus.COMPLETED

    @pytest.mark.asyncio
    async def test_mapPollStatus_withInvalid(self):
        result = await self.mapper.mapPollStatus(ApiPollStatus.INVALID)
        assert result is LocalPollStatus.INVALID

    @pytest.mark.asyncio
    async def test_mapPollStatus_withModerated(self):
        result = await self.mapper.mapPollStatus(ApiPollStatus.MODERATED)
        assert result is LocalPollStatus.MODERATED

    @pytest.mark.asyncio
    async def test_mapPollStatus_withTerminated(self):
        result = await self.mapper.mapPollStatus(ApiPollStatus.TERMINATED)
        assert result is LocalPollStatus.TERMINATED

    @pytest.mark.asyncio
    async def test_mapPollStatus_withNone(self):
        result = await self.mapper.mapPollStatus(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_mapResubscriptionMessage(self):
        emotes: FrozenList[ApiResubscriptionMessageEmote] = FrozenList([
            ApiResubscriptionMessageEmote(
                begin = 0,
                end = 1,
                emoteId = 'emoteId',
            ),
        ])
        emotes.freeze()

        resubscriptionMessage = ApiResubscriptionMessage(
            emotes = emotes,
            text = 'Hello, World!',
        )

        result = await self.mapper.mapResubscriptionMessage(resubscriptionMessage)
        assert isinstance(result, LocalResubscriptionMessage)
        assert len(result.emotes) == 1
        assert result.emotes.frozen
        assert result.emotes[0] == await self.mapper.requireResubscriptionMessageEmote(emotes[0])
        assert result.text == resubscriptionMessage.text

    @pytest.mark.asyncio
    async def test_mapResubscriptionMessage_withNone(self):
        result = await self.mapper.mapResubscriptionMessage(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_mapResubscriptionMessageEmote(self):
        messageEmote = ApiResubscriptionMessageEmote(
            begin = 0,
            end = 1,
            emoteId = 'abc123',
        )

        result = await self.mapper.mapResubscriptionMessageEmote(messageEmote)
        assert isinstance(result, LocalResubscriptionMessageEmote)
        assert result.begin == messageEmote.begin
        assert result.end == messageEmote.end
        assert result.emoteId == messageEmote.emoteId

    @pytest.mark.asyncio
    async def test_mapResubscriptionMessageEmote_withNone(self):
        result = await self.mapper.mapResubscriptionMessageEmote(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_mapSubscriberTier_withNone(self):
        result = await self.mapper.mapSubscriberTier(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_mapSubscriberTier_withPrime(self):
        result = await self.mapper.mapSubscriberTier(ApiSubscriberTier.PRIME)
        assert result is LocalSubscriberTier.PRIME

    @pytest.mark.asyncio
    async def test_mapSubscriberTier_withTierOne(self):
        result = await self.mapper.mapSubscriberTier(ApiSubscriberTier.TIER_ONE)
        assert result is LocalSubscriberTier.TIER_ONE

    @pytest.mark.asyncio
    async def test_mapSubscriberTier_withTierTwo(self):
        result = await self.mapper.mapSubscriberTier(ApiSubscriberTier.TIER_TWO)
        assert result is LocalSubscriberTier.TIER_TWO

    @pytest.mark.asyncio
    async def test_mapSubscriberTier_withTierThree(self):
        result = await self.mapper.mapSubscriberTier(ApiSubscriberTier.TIER_THREE)
        assert result is LocalSubscriberTier.TIER_THREE

    @pytest.mark.asyncio
    async def test_mapWatchStreak(self):
        apiWatchStreak = ApiWatchStreak(
            channelPointsAwarded = 250,
            streakCount = 7,
        )

        result = await self.mapper.mapWatchStreak(apiWatchStreak)
        assert isinstance(result, LocalWatchStreak)
        assert result.channelPointsAwarded == apiWatchStreak.channelPointsAwarded
        assert result.streakCount == apiWatchStreak.streakCount

    @pytest.mark.asyncio
    async def test_mapWatchStreak_withNone(self):
        result = await self.mapper.mapWatchStreak(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_requireChatMessageFragment(self):
        apiFragment = ApiChatMessageFragment(
            text = 'Hello, World!',
            cheermote = None,
            emote = ApiChatMessageFragmentEmote(
                imageFormats = frozenset({ ApiEmoteImageFormat.STATIC }),
                emoteId = 'emoteId',
                emoteSetId = 'emoteSetId',
                ownerId = 'ownerId',
            ),
            gif = None,
            mention = None,
            fragmentType = ApiChatMessageFragmentType.EMOTE,
        )

        result = await self.mapper.requireChatMessageFragment(apiFragment)
        assert isinstance(result, LocalChatMessageFragment)
        assert result.text == apiFragment.text
        assert result.cheermote == await self.mapper.mapChatMessageFragmentCheermote(apiFragment.cheermote)
        assert result.emote == await self.mapper.mapChatMessageFragmentEmote(apiFragment.emote)
        assert result.gif == await self.mapper.mapChatMessageFragmentGif(apiFragment.gif)
        assert result.mention == await self.mapper.mapChatMessageFragmentMention(apiFragment.mention)
        assert result.fragmentType is await self.mapper.requireChatMessageFragmentType(apiFragment.fragmentType)

    @pytest.mark.asyncio
    async def test_requireChatMessageFragment_withNone(self):
        result: LocalChatMessageFragment | None = None

        with pytest.raises(ValueError):
            result = await self.mapper.requireChatMessageFragment(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireChatMessageFragmentType_withAll(self):
        results: set[LocalChatMessageFragmentType] = set()

        for chatMessageFragmentType in ApiChatMessageFragmentType:
            result = await self.mapper.requireChatMessageFragmentType(chatMessageFragmentType)
            results.add(result)

        assert len(results) == len(LocalChatMessageFragmentType)
        assert None not in results

    @pytest.mark.asyncio
    async def test_requireChatMessageFragmentType_withCheermote(self):
        result = await self.mapper.requireChatMessageFragmentType(ApiChatMessageFragmentType.CHEERMOTE)
        assert result is LocalChatMessageFragmentType.CHEERMOTE

    @pytest.mark.asyncio
    async def test_requireChatMessageFragmentType_withEmote(self):
        result = await self.mapper.requireChatMessageFragmentType(ApiChatMessageFragmentType.EMOTE)
        assert result is LocalChatMessageFragmentType.EMOTE

    @pytest.mark.asyncio
    async def test_requireChatMessageFragmentType_withGif(self):
        result = await self.mapper.requireChatMessageFragmentType(ApiChatMessageFragmentType.GIF)
        assert result is LocalChatMessageFragmentType.GIF

    @pytest.mark.asyncio
    async def test_requireChatMessageFragmentType_withMention(self):
        result = await self.mapper.requireChatMessageFragmentType(ApiChatMessageFragmentType.MENTION)
        assert result is LocalChatMessageFragmentType.MENTION

    @pytest.mark.asyncio
    async def test_requireChatMessageFragmentType_withNone(self):
        result: LocalChatMessageFragmentType | None = None

        with pytest.raises(ValueError):
            result = await self.mapper.requireChatMessageFragmentType(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireChatMessageFragmentType_withText(self):
        result = await self.mapper.requireChatMessageFragmentType(ApiChatMessageFragmentType.TEXT)
        assert result is LocalChatMessageFragmentType.TEXT

    @pytest.mark.asyncio
    async def test_requireEmoteImageFormat_withAll(self):
        results: set[LocalEmoteImageFormat] = set()

        for emoteImageFormat in ApiEmoteImageFormat:
            result = await self.mapper.requireEmoteImageFormat(emoteImageFormat)
            results.add(result)

        assert len(results) == len(LocalEmoteImageFormat)

    @pytest.mark.asyncio
    async def test_requireEmoteImageFormat_withAnimated(self):
        result = await self.mapper.requireEmoteImageFormat(ApiEmoteImageFormat.ANIMATED)
        assert result is LocalEmoteImageFormat.ANIMATED

    @pytest.mark.asyncio
    async def test_requireEmoteImageFormat_withNone(self):
        result: LocalEmoteImageFormat | None = None

        with pytest.raises(ValueError):
            await self.mapper.requireEmoteImageFormat(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireEmoteImageFormat_withStatic(self):
        result = await self.mapper.requireEmoteImageFormat(ApiEmoteImageFormat.STATIC)
        assert result is LocalEmoteImageFormat.STATIC

    @pytest.mark.asyncio
    async def test_requirePollChoice(self):
        apiPollChoice = ApiPollChoice(
            channelPointsVotes = 100,
            votes = 5,
            choiceId = 'abc123',
            title = 'Hello, World!',
        )

        result = await self.mapper.requirePollChoice(apiPollChoice)
        assert isinstance(result, LocalPollChoice)
        assert result.channelPointsVotes == apiPollChoice.channelPointsVotes
        assert result.votes == apiPollChoice.votes
        assert result.choiceId == apiPollChoice.choiceId
        assert result.title == apiPollChoice.title

    @pytest.mark.asyncio
    async def test_requirePollChoice_withNone(self):
        result: LocalPollChoice | None = None

        with pytest.raises(ValueError):
            result = await self.mapper.requirePollChoice(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireResubscriptionMessageEmote(self):
        messageEmote = ApiResubscriptionMessageEmote(
            begin = 0,
            end = 1,
            emoteId = 'abc123',
        )

        result = await self.mapper.requireResubscriptionMessageEmote(messageEmote)
        assert isinstance(result, LocalResubscriptionMessageEmote)
        assert result.begin == messageEmote.begin
        assert result.end == messageEmote.end
        assert result.emoteId == messageEmote.emoteId

    @pytest.mark.asyncio
    async def test_requireResubscriptionMessageEmote_withNone(self):
        result: LocalResubscriptionMessageEmote | None = None

        with pytest.raises(ValueError):
            result = await self.mapper.requireResubscriptionMessageEmote(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireSubscriberTier_withNone(self):
        result: LocalSubscriberTier | None = None

        with pytest.raises(ValueError):
            result = await self.mapper.requireSubscriberTier(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireSubscriberTier_withPrime(self):
        result = await self.mapper.requireSubscriberTier(ApiSubscriberTier.PRIME)
        assert result is LocalSubscriberTier.PRIME

    @pytest.mark.asyncio
    async def test_requireSubscriberTier_withTierOne(self):
        result = await self.mapper.requireSubscriberTier(ApiSubscriberTier.TIER_ONE)
        assert result is LocalSubscriberTier.TIER_ONE

    @pytest.mark.asyncio
    async def test_requireSubscriberTier_withTierTwo(self):
        result = await self.mapper.requireSubscriberTier(ApiSubscriberTier.TIER_TWO)
        assert result is LocalSubscriberTier.TIER_TWO

    @pytest.mark.asyncio
    async def test_requireSubscriberTier_withTierThree(self):
        result = await self.mapper.requireSubscriberTier(ApiSubscriberTier.TIER_THREE)
        assert result is LocalSubscriberTier.TIER_THREE


    def test_sanity(self):
        assert self.mapper is not None
        assert isinstance(self.mapper, TwitchLocalModelsMapper)
        assert isinstance(self.mapper, TwitchLocalModelsMapperInterface)
