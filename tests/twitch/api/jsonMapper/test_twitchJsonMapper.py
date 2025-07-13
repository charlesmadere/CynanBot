from datetime import datetime, timedelta
from typing import Any

import pytest
from frozenlist import FrozenList

from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.twitch.api.jsonMapper.twitchJsonMapper import TwitchJsonMapper
from src.twitch.api.jsonMapper.twitchJsonMapperInterface import TwitchJsonMapperInterface
from src.twitch.api.models.twitchApiScope import TwitchApiScope
from src.twitch.api.models.twitchBanRequest import TwitchBanRequest
from src.twitch.api.models.twitchBroadcasterType import TwitchBroadcasterType
from src.twitch.api.models.twitchChannelEditor import TwitchChannelEditor
from src.twitch.api.models.twitchChannelEditorsResponse import TwitchChannelEditorsResponse
from src.twitch.api.models.twitchChatAnnouncementColor import TwitchChatAnnouncementColor
from src.twitch.api.models.twitchChatMessageFragmentType import TwitchChatMessageFragmentType
from src.twitch.api.models.twitchChatMessageType import TwitchChatMessageType
from src.twitch.api.models.twitchChatter import TwitchChatter
from src.twitch.api.models.twitchCheerMetadata import TwitchCheerMetadata
from src.twitch.api.models.twitchConduitRequest import TwitchConduitRequest
from src.twitch.api.models.twitchConduitResponse import TwitchConduitResponse
from src.twitch.api.models.twitchConduitResponseEntry import TwitchConduitResponseEntry
from src.twitch.api.models.twitchConduitShard import TwitchConduitShard
from src.twitch.api.models.twitchContributionType import TwitchContributionType
from src.twitch.api.models.twitchEmoteImageFormat import TwitchEmoteImageFormat
from src.twitch.api.models.twitchEmoteImageScale import TwitchEmoteImageScale
from src.twitch.api.models.twitchEmoteType import TwitchEmoteType
from src.twitch.api.models.twitchEventSubRequest import TwitchEventSubRequest
from src.twitch.api.models.twitchHypeTrainType import TwitchHypeTrainType
from src.twitch.api.models.twitchNoticeType import TwitchNoticeType
from src.twitch.api.models.twitchOutcomeColor import TwitchOutcomeColor
from src.twitch.api.models.twitchPaginationResponse import TwitchPaginationResponse
from src.twitch.api.models.twitchPollStatus import TwitchPollStatus
from src.twitch.api.models.twitchPowerUpEmote import TwitchPowerUpEmote
from src.twitch.api.models.twitchPowerUpType import TwitchPowerUpType
from src.twitch.api.models.twitchPredictionStatus import TwitchPredictionStatus
from src.twitch.api.models.twitchRaid import TwitchRaid
from src.twitch.api.models.twitchRewardRedemptionStatus import TwitchRewardRedemptionStatus
from src.twitch.api.models.twitchSendChatAnnouncementRequest import TwitchSendChatAnnouncementRequest
from src.twitch.api.models.twitchSendChatMessageRequest import TwitchSendChatMessageRequest
from src.twitch.api.models.twitchStartCommercialDetails import TwitchStartCommercialDetails
from src.twitch.api.models.twitchStreamType import TwitchStreamType
from src.twitch.api.models.twitchSubscriberTier import TwitchSubscriberTier
from src.twitch.api.models.twitchUserType import TwitchUserType
from src.twitch.api.models.twitchWebsocketChannelPointsVoting import TwitchWebsocketChannelPointsVoting
from src.twitch.api.models.twitchWebsocketCondition import TwitchWebsocketCondition
from src.twitch.api.models.twitchWebsocketConnectionStatus import TwitchWebsocketConnectionStatus
from src.twitch.api.models.twitchWebsocketMessageType import TwitchWebsocketMessageType
from src.twitch.api.models.twitchWebsocketSub import TwitchWebsocketSub
from src.twitch.api.models.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from src.twitch.api.models.twitchWebsocketTransport import TwitchWebsocketTransport
from src.twitch.api.models.twitchWebsocketTransportMethod import TwitchWebsocketTransportMethod


class TestTwitchJsonMapper:

    timber: TimberInterface = TimberStub()

    timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

    jsonMapper: TwitchJsonMapperInterface = TwitchJsonMapper(
        timber = timber,
        timeZoneRepository = timeZoneRepository
    )

    @pytest.mark.asyncio
    async def test_parseApiScope_withBitsReadString(self):
        result = await self.jsonMapper.parseApiScope('bits:read')
        assert result is TwitchApiScope.BITS_READ

    @pytest.mark.asyncio
    async def test_parseApiScope_withChannelBotString(self):
        result = await self.jsonMapper.parseApiScope('channel:bot')
        assert result is TwitchApiScope.CHANNEL_BOT

    @pytest.mark.asyncio
    async def test_parseApiScope_withChannelEditCommercialString(self):
        result = await self.jsonMapper.parseApiScope('channel:edit:commercial')
        assert result is TwitchApiScope.CHANNEL_EDIT_COMMERCIAL

    @pytest.mark.asyncio
    async def test_parseApiScope_withChannelEditorString(self):
        result = await self.jsonMapper.parseApiScope('channel_editor')
        assert result is TwitchApiScope.CHANNEL_EDITOR

    @pytest.mark.asyncio
    async def test_parseApiScope_withChannelManageAdsString(self):
        result = await self.jsonMapper.parseApiScope('channel:manage:ads')
        assert result is TwitchApiScope.CHANNEL_MANAGE_ADS

    @pytest.mark.asyncio
    async def test_parseApiScope_withChannelManageModeratorsString(self):
        result = await self.jsonMapper.parseApiScope('channel:manage:moderators')
        assert result is TwitchApiScope.CHANNEL_MANAGE_MODERATORS

    @pytest.mark.asyncio
    async def test_parseApiScope_withChannelManagePollsString(self):
        result = await self.jsonMapper.parseApiScope('channel:manage:polls')
        assert result is TwitchApiScope.CHANNEL_MANAGE_POLLS

    @pytest.mark.asyncio
    async def test_parseApiScope_withChannelManagePredictionsString(self):
        result = await self.jsonMapper.parseApiScope('channel:manage:predictions')
        assert result is TwitchApiScope.CHANNEL_MANAGE_PREDICTIONS

    @pytest.mark.asyncio
    async def test_parseApiScope_withChannelManageRedemptionsString(self):
        result = await self.jsonMapper.parseApiScope('channel:manage:redemptions')
        assert result is TwitchApiScope.CHANNEL_MANAGE_REDEMPTIONS

    @pytest.mark.asyncio
    async def test_parseApiScope_withChannelModerateString(self):
        result = await self.jsonMapper.parseApiScope('channel:moderate')
        assert result is TwitchApiScope.CHANNEL_MODERATE

    @pytest.mark.asyncio
    async def test_parseApiScope_withChannelReadAdsString(self):
        result = await self.jsonMapper.parseApiScope('channel:read:ads')
        assert result is TwitchApiScope.CHANNEL_READ_ADS

    @pytest.mark.asyncio
    async def test_parseApiScope_withChannelReadEditorsString(self):
        result = await self.jsonMapper.parseApiScope('channel:read:editors')
        assert result is TwitchApiScope.CHANNEL_READ_EDITORS

    @pytest.mark.asyncio
    async def test_parseApiScope_withChannelReadHypeTrainString(self):
        result = await self.jsonMapper.parseApiScope('channel:read:hype_train')
        assert result is TwitchApiScope.CHANNEL_READ_HYPE_TRAIN

    @pytest.mark.asyncio
    async def test_parseApiScope_withChannelReadPollsString(self):
        result = await self.jsonMapper.parseApiScope('channel:read:polls')
        assert result is TwitchApiScope.CHANNEL_READ_POLLS

    @pytest.mark.asyncio
    async def test_parseApiScope_withChannelReadPredictionsString(self):
        result = await self.jsonMapper.parseApiScope('channel:read:predictions')
        assert result is TwitchApiScope.CHANNEL_READ_PREDICTIONS

    @pytest.mark.asyncio
    async def test_parseApiScope_withChannelReadRedemptionsString(self):
        result = await self.jsonMapper.parseApiScope('channel:read:redemptions')
        assert result is TwitchApiScope.CHANNEL_READ_REDEMPTIONS

    @pytest.mark.asyncio
    async def test_parseApiScope_withChannelReadSubscriptionsString(self):
        result = await self.jsonMapper.parseApiScope('channel:read:subscriptions')
        assert result is TwitchApiScope.CHANNEL_READ_SUBSCRIPTIONS

    @pytest.mark.asyncio
    async def test_parseApiScope_withChannelSubscriptionsString(self):
        result = await self.jsonMapper.parseApiScope('channel_subscriptions')
        assert result is TwitchApiScope.CHANNEL_SUBSCRIPTIONS

    @pytest.mark.asyncio
    async def test_parseApiScope_withChatEditString(self):
        result = await self.jsonMapper.parseApiScope('chat:edit')
        assert result is TwitchApiScope.CHAT_EDIT

    @pytest.mark.asyncio
    async def test_parseApiScope_withChatReadString(self):
        result = await self.jsonMapper.parseApiScope('chat:read')
        assert result is TwitchApiScope.CHAT_READ

    @pytest.mark.asyncio
    async def test_parseApiScope_withEmptyString(self):
        result = await self.jsonMapper.parseApiScope('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseApiScope_withModerationReadString(self):
        result = await self.jsonMapper.parseApiScope('moderation:read')
        assert result is TwitchApiScope.MODERATION_READ

    @pytest.mark.asyncio
    async def test_parseApiScope_withModeratorManageAnnouncementsString(self):
        result = await self.jsonMapper.parseApiScope('moderator:manage:announcements')
        assert result is TwitchApiScope.MODERATOR_MANAGE_ANNOUNCEMENTS

    @pytest.mark.asyncio
    async def test_parseApiScope_withModeratorManageBannedUsersString(self):
        result = await self.jsonMapper.parseApiScope('moderator:manage:banned_users')
        assert result is TwitchApiScope.MODERATOR_MANAGE_BANNED_USERS

    @pytest.mark.asyncio
    async def test_parseApiScope_withModeratorManageChatMessagesString(self):
        result = await self.jsonMapper.parseApiScope('moderator:manage:chat_messages')
        assert result is TwitchApiScope.MODERATOR_MANAGE_CHAT_MESSAGES

    @pytest.mark.asyncio
    async def test_parseApiScope_withModeratorReadChattersString(self):
        result = await self.jsonMapper.parseApiScope('moderator:read:chatters')
        assert result is TwitchApiScope.MODERATOR_READ_CHATTERS

    @pytest.mark.asyncio
    async def test_parseApiScope_withModeratorReadChatSettingsString(self):
        result = await self.jsonMapper.parseApiScope('moderator:read:chat_settings')
        assert result is TwitchApiScope.MODERATOR_READ_CHAT_SETTINGS

    @pytest.mark.asyncio
    async def test_parseApiScope_withModeratorReadFollowersString(self):
        result = await self.jsonMapper.parseApiScope('moderator:read:followers')
        assert result is TwitchApiScope.MODERATOR_READ_FOLLOWERS

    @pytest.mark.asyncio
    async def test_parseApiScope_withModeratorReadModeratorsString(self):
        result = await self.jsonMapper.parseApiScope('moderator:read:moderators')
        assert result is TwitchApiScope.MODERATOR_READ_MODERATORS

    @pytest.mark.asyncio
    async def test_parseApiScope_withNone(self):
        result = await self.jsonMapper.parseApiScope(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseApiScope_withUserBotString(self):
        result = await self.jsonMapper.parseApiScope('user:bot')
        assert result is TwitchApiScope.USER_BOT

    @pytest.mark.asyncio
    async def test_parseApiScope_withUserReadBroadcastString(self):
        result = await self.jsonMapper.parseApiScope('user:read:broadcast')
        assert result is TwitchApiScope.USER_READ_BROADCAST

    @pytest.mark.asyncio
    async def test_parseApiScope_withUserReadChatString(self):
        result = await self.jsonMapper.parseApiScope('user:read:chat')
        assert result is TwitchApiScope.USER_READ_CHAT

    @pytest.mark.asyncio
    async def test_parseApiScope_withUserReadEmotesString(self):
        result = await self.jsonMapper.parseApiScope('user:read:emotes')
        assert result is TwitchApiScope.USER_READ_EMOTES

    @pytest.mark.asyncio
    async def test_parseApiScope_withUserReadFollowsString(self):
        result = await self.jsonMapper.parseApiScope('user:read:follows')
        assert result is TwitchApiScope.USER_READ_FOLLOWS

    @pytest.mark.asyncio
    async def test_parseApiScope_withUserReadSubscriptionsString(self):
        result = await self.jsonMapper.parseApiScope('user:read:subscriptions')
        assert result is TwitchApiScope.USER_READ_SUBSCRIPTIONS

    @pytest.mark.asyncio
    async def test_parseApiScope_withUserSubscriptionsString(self):
        result = await self.jsonMapper.parseApiScope('user_subscriptions')
        assert result is TwitchApiScope.USER_SUBSCRIPTIONS

    @pytest.mark.asyncio
    async def test_parseApiScope_withUserWriteChatString(self):
        result = await self.jsonMapper.parseApiScope('user:write:chat')
        assert result is TwitchApiScope.USER_WRITE_CHAT

    @pytest.mark.asyncio
    async def test_parseApiScope_withWhispersEditString(self):
        result = await self.jsonMapper.parseApiScope('whispers:edit')
        assert result is TwitchApiScope.WHISPERS_EDIT

    @pytest.mark.asyncio
    async def test_parseApiScope_withWhispersReadString(self):
        result = await self.jsonMapper.parseApiScope('whispers:read')
        assert result is TwitchApiScope.WHISPERS_READ

    @pytest.mark.asyncio
    async def test_parseApiScope_withWhitespaceString(self):
        result = await self.jsonMapper.parseApiScope(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseBannedUserResponse_withDataButNoBannedUser(self):
        jsonResponse: dict[str, Any] = {
            'data': [ ]
        }

        result = await self.jsonMapper.parseBannedUserResponse(jsonResponse)
        assert result is not None
        assert result.bannedUser is None

    @pytest.mark.asyncio
    async def test_parseBannedUserResponse_withEmptyDictionary(self):
        result = await self.jsonMapper.parseBannedUserResponse(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseBannedUserResponse_withNone(self):
        result = await self.jsonMapper.parseBannedUserResponse(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseBroadcasterType_withAffiliateString(self):
        result = await self.jsonMapper.parseBroadcasterType('affiliate')
        assert result is TwitchBroadcasterType.AFFILIATE

    @pytest.mark.asyncio
    async def test_parseBroadcasterType_withEmptyString(self):
        result = await self.jsonMapper.parseBroadcasterType('')
        assert result is TwitchBroadcasterType.NORMAL

    @pytest.mark.asyncio
    async def test_parseBroadcasterType_withNone(self):
        result = await self.jsonMapper.parseBroadcasterType(None)
        assert result is TwitchBroadcasterType.NORMAL

    @pytest.mark.asyncio
    async def test_parseBroadcasterType_withPartnerString(self):
        result = await self.jsonMapper.parseBroadcasterType('partner')
        assert result is TwitchBroadcasterType.PARTNER

    @pytest.mark.asyncio
    async def test_parseBroadcasterType_withWhitespaceString(self):
        result = await self.jsonMapper.parseBroadcasterType(' ')
        assert result is TwitchBroadcasterType.NORMAL

    @pytest.mark.asyncio
    async def test_parseChannelEditor(self):
        createdAt = datetime.now(self.timeZoneRepository.getDefault())
        userId = 'abc123'
        userName = 'gaR'

        result = await self.jsonMapper.parseChannelEditor({
            'created_at': createdAt.isoformat(),
            'user_id': userId,
            'user_name': userName
        })

        assert isinstance(result, TwitchChannelEditor)
        assert result.createdAt == createdAt
        assert result.userId == userId
        assert result.userName == userName

    @pytest.mark.asyncio
    async def test_parseChannelEditorsResponse(self):
        now = datetime.now(self.timeZoneRepository.getDefault())
        tsteineCreatedAt = now - timedelta(weeks = 1)
        qbitCreatedAt = now - timedelta(weeks = 2)

        tsteine = TwitchChannelEditor(
            createdAt = tsteineCreatedAt,
            userId = 'abc123',
            userName = 'Tsteine'
        )

        qbit = TwitchChannelEditor(
            createdAt = qbitCreatedAt,
            userId = 'def456',
            userName = 'qbit'
        )

        result = await self.jsonMapper.parseChannelEditorsResponse({
            'data': [
                {
                    'created_at': tsteineCreatedAt.isoformat(),
                    'user_id': tsteine.userId,
                    'user_name': tsteine.userName
                },
                {
                    'created_at': qbitCreatedAt.isoformat(),
                    'user_id': qbit.userId,
                    'user_name': qbit.userName
                }
            ]
        })

        assert isinstance(result, TwitchChannelEditorsResponse)
        assert len(result.editors) == 2

        editor = result.editors[0]
        assert isinstance(editor, TwitchChannelEditor)
        assert editor == tsteine
        assert editor.createdAt == tsteine.createdAt
        assert editor.userId == tsteine.userId
        assert editor.userName == tsteine.userName

        editor = result.editors[1]
        assert isinstance(editor, TwitchChannelEditor)
        assert editor == qbit
        assert editor.createdAt == qbit.createdAt
        assert editor.userId == qbit.userId
        assert editor.userName == qbit.userName

    @pytest.mark.asyncio
    async def test_parseChannelEditorsResponse_withEmptyDictionary(self):
        result = await self.jsonMapper.parseChannelEditorsResponse(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseChannelEditorsResponse_withNone(self):
        result = await self.jsonMapper.parseChannelEditorsResponse(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseChatMessage_withEmptyDictionary(self):
        result = await self.jsonMapper.parseChatMessage(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseChatMessage_withNone(self):
        result = await self.jsonMapper.parseChatMessage(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseChatMessageFragment_withEmptyDictionary(self):
        result = await self.jsonMapper.parseChatMessageFragment(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseChatMessageFragment_withNone(self):
        result = await self.jsonMapper.parseChatMessageFragment(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseChatMessageFragmentCheermote_withEmptyDictionary(self):
        result = await self.jsonMapper.parseChatMessageFragmentCheermote(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseChatMessageFragmentCheermote_withNone(self):
        result = await self.jsonMapper.parseChatMessageFragmentCheermote(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseChatMessageFragmentEmote_withEmptyDictionary(self):
        result = await self.jsonMapper.parseChatMessageFragmentEmote(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseChatMessageFragmentEmote_withNone(self):
        result = await self.jsonMapper.parseChatMessageFragmentEmote(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseChatMessageFragmentMention_withEmptyDictionary(self):
        result = await self.jsonMapper.parseChatMessageFragmentMention(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseChatMessageFragmentMention_withNone(self):
        result = await self.jsonMapper.parseChatMessageFragmentMention(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseChatMessageFragmentType_withCheermoteString(self):
        result = await self.jsonMapper.parseChatMessageFragmentType('cheermote')
        assert result is TwitchChatMessageFragmentType.CHEERMOTE

    @pytest.mark.asyncio
    async def test_parseChatMessageFragmentType_withEmoteString(self):
        result = await self.jsonMapper.parseChatMessageFragmentType('emote')
        assert result is TwitchChatMessageFragmentType.EMOTE

    @pytest.mark.asyncio
    async def test_parseChatMessageFragmentType_withEmptyString(self):
        result = await self.jsonMapper.parseChatMessageFragmentType('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseChatMessageFragmentType_withMentionString(self):
        result = await self.jsonMapper.parseChatMessageFragmentType('mention')
        assert result is TwitchChatMessageFragmentType.MENTION

    @pytest.mark.asyncio
    async def test_parseChatMessageFragmentType_withNone(self):
        result = await self.jsonMapper.parseChatMessageFragmentType(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseChatMessageFragmentType_withTextString(self):
        result = await self.jsonMapper.parseChatMessageFragmentType('text')
        assert result is TwitchChatMessageFragmentType.TEXT

    @pytest.mark.asyncio
    async def test_parseChatMessageFragmentType_withWhitespaceString(self):
        result = await self.jsonMapper.parseChatMessageFragmentType(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseChatMessageType_withChannelPointsHighlighted(self):
        result = await self.jsonMapper.parseChatMessageType('channel_points_highlighted')
        assert result is TwitchChatMessageType.CHANNEL_POINTS_HIGHLIGHTED

    @pytest.mark.asyncio
    async def test_parseChatMessageType_withChannelPointsSubOnly(self):
        result = await self.jsonMapper.parseChatMessageType('channel_points_sub_only')
        assert result is TwitchChatMessageType.CHANNEL_POINTS_SUB_ONLY

    @pytest.mark.asyncio
    async def test_parseChatMessageType_withEmptyString(self):
        result = await self.jsonMapper.parseChatMessageType('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseChatMessageType_withNone(self):
        result = await self.jsonMapper.parseChatMessageType(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseChatMessageType_withPowerUpsGigantifiedEmote(self):
        result = await self.jsonMapper.parseChatMessageType('power_ups_gigantified_emote')
        assert result is TwitchChatMessageType.POWER_UPS_GIGANTIFIED_EMOTE

    @pytest.mark.asyncio
    async def test_parseChatMessageType_withPowerUpsMessageEffect(self):
        result = await self.jsonMapper.parseChatMessageType('power_ups_message_effect')
        assert result is TwitchChatMessageType.POWER_UPS_MESSAGE_EFFECT

    @pytest.mark.asyncio
    async def test_parseChatMessageType_withUserIntro(self):
        result = await self.jsonMapper.parseChatMessageType('user_intro')
        assert result is TwitchChatMessageType.USER_INTRO

    @pytest.mark.asyncio
    async def test_parseChatMessageType_withWhitespaceString(self):
        result = await self.jsonMapper.parseChatMessageType(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseChatter(self):
        userId = 'abc123'
        userLogin = 'stashiocat'
        userName = 'stashiocat'

        result = await self.jsonMapper.parseChatter({
            'user_id': userId,
            'user_login': userLogin,
            'user_name': userName
        })

        assert isinstance(result, TwitchChatter)
        assert result.userId == userId
        assert result.userLogin == userLogin
        assert result.userName == userName

    @pytest.mark.asyncio
    async def test_parseChatter_withEmptyDictionary(self):
        result: TwitchChatter | None = None

        with pytest.raises(Exception):
            result = await self.jsonMapper.parseChatter(dict())

        assert result is None

    @pytest.mark.asyncio
    async def test_parseChatter_withNone(self):
        result: TwitchChatter | None = None

        with pytest.raises(Exception):
            result = await self.jsonMapper.parseChatter(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_parseCheer(self):
        cheerMetadata = TwitchCheerMetadata(
            bits = 250,
        )

        result = await self.jsonMapper.parseCheerMetadata({
            'bits': cheerMetadata.bits,
        })

        assert isinstance(result, TwitchCheerMetadata)
        assert result == cheerMetadata
        assert result.bits == cheerMetadata.bits

    @pytest.mark.asyncio
    async def test_parseCheer_withEmptyDictionary(self):
        result = await self.jsonMapper.parseCheerMetadata(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseCheer_withNone(self):
        result = await self.jsonMapper.parseCheerMetadata(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseCondition_withEmptyDictionary(self):
        result = await self.jsonMapper.parseCondition(dict())
        assert isinstance(result, TwitchWebsocketCondition)
        assert result.broadcasterUserId is None
        assert result.broadcasterUserLogin is None
        assert result.broadcasterUserName is None
        assert result.clientId is None
        assert result.fromBroadcasterUserId is None
        assert result.fromBroadcasterUserLogin is None
        assert result.fromBroadcasterUserName is None
        assert result.moderatorUserId is None
        assert result.moderatorUserLogin is None
        assert result.moderatorUserName is None
        assert result.rewardId is None
        assert result.toBroadcasterUserId is None
        assert result.toBroadcasterUserLogin is None
        assert result.toBroadcasterUserName is None
        assert result.userId is None
        assert result.userLogin is None
        assert result.userName is None

        broadcasterUserId: str | None = None

        with pytest.raises(Exception):
            broadcasterUserId = result.requireBroadcasterUserId()

        assert broadcasterUserId is None

    @pytest.mark.asyncio
    async def test_parseCondition_withNone(self):
        result = await self.jsonMapper.parseCondition(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseConduitResponse(self):
        entry = TwitchConduitResponseEntry(
            shardCount = 5,
            shardId = 'abc123',
        )

        data: FrozenList[TwitchConduitResponseEntry] = FrozenList()
        data.append(entry)
        data.freeze()

        response = TwitchConduitResponse(
            data = data,
        )

        result = await self.jsonMapper.parseConduitResponse({
            'data': [
                {
                    'id': entry.shardId,
                    'shard_count': entry.shardCount,
                },
            ],
        })

        assert isinstance(result, TwitchConduitResponse)
        assert result == response
        assert len(result.data) == 1

        resultEntry = result.data[0]
        assert isinstance(resultEntry, TwitchConduitResponseEntry)
        assert resultEntry == entry
        assert resultEntry.shardCount == entry.shardCount
        assert resultEntry.shardId == entry.shardId

    @pytest.mark.asyncio
    async def test_parseConduitResponse_withEmptyDictionary(self):
        result = await self.jsonMapper.parseConduitResponse(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseConduitResponse_withNone(self):
        result = await self.jsonMapper.parseConduitResponse(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseConduitResponseEntry(self):
        entry = TwitchConduitResponseEntry(
            shardCount = 5,
            shardId = 'abc123',
        )

        result = await self.jsonMapper.parseConduitResponseEntry({
            'shard_count': entry.shardCount,
            'id': entry.shardId,
        })

        assert isinstance(result, TwitchConduitResponseEntry)
        assert result == entry
        assert result.shardCount == entry.shardCount
        assert result.shardId == entry.shardId

    @pytest.mark.asyncio
    async def test_parseConduitResponseEntry_withNone(self):
        result = await self.jsonMapper.parseConduitResponseEntry(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseConduitShard(self):
        conduitShard = TwitchConduitShard(
            conduitId = "abc123",
            shard = "42",
        )

        result = await self.jsonMapper.parseConduitShard({
            'conduit_id': conduitShard.conduitId,
            'shard': conduitShard.shard,
        })

        assert isinstance(result, TwitchConduitShard)
        assert result == conduitShard
        assert result.conduitId == conduitShard.conduitId
        assert result.shard == conduitShard.shard

    @pytest.mark.asyncio
    async def test_parseConduitShard_withNone(self):
        result = await self.jsonMapper.parseConduitShard(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseConnectionStatus_withAuthorizationRevokedString(self):
        result = await self.jsonMapper.parseConnectionStatus('authorization_revoked')
        assert result is TwitchWebsocketConnectionStatus.REVOKED

    @pytest.mark.asyncio
    async def test_parseConnectionStatus_withEmptyString(self):
        result = await self.jsonMapper.parseConnectionStatus('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseConnectionStatus_withConnectedString(self):
        result = await self.jsonMapper.parseConnectionStatus('connected')
        assert result is TwitchWebsocketConnectionStatus.CONNECTED

    @pytest.mark.asyncio
    async def test_parseConnectionStatus_withEnabledString(self):
        result = await self.jsonMapper.parseConnectionStatus('enabled')
        assert result is TwitchWebsocketConnectionStatus.ENABLED

    @pytest.mark.asyncio
    async def test_parseConnectionStatus_withNone(self):
        result = await self.jsonMapper.parseConnectionStatus(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseConnectionStatus_withReconnectingString(self):
        result = await self.jsonMapper.parseConnectionStatus('reconnecting')
        assert result is TwitchWebsocketConnectionStatus.RECONNECTING

    @pytest.mark.asyncio
    async def test_parseConnectionStatus_withUserRemovedString(self):
        result = await self.jsonMapper.parseConnectionStatus('user_removed')
        assert result is TwitchWebsocketConnectionStatus.USER_REMOVED

    @pytest.mark.asyncio
    async def test_parseConnectionStatus_withVersionRemovedString(self):
        result = await self.jsonMapper.parseConnectionStatus('version_removed')
        assert result is TwitchWebsocketConnectionStatus.VERSION_REMOVED

    @pytest.mark.asyncio
    async def test_parseConnectionStatus_withWebhookCallbackVerificationPendingString(self):
        result = await self.jsonMapper.parseConnectionStatus('webhook_callback_verification_pending')
        assert result is TwitchWebsocketConnectionStatus.WEBHOOK_CALLBACK_VERIFICATION_PENDING

    @pytest.mark.asyncio
    async def test_parseConnectionStatus_withWhitespaceString(self):
        result = await self.jsonMapper.parseConnectionStatus(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseContribution_withEmptyDictionary(self):
        result = await self.jsonMapper.parseContribution(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseContribution_withNone(self):
        result = await self.jsonMapper.parseContribution(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseContributionType_withBits(self):
        result = await self.jsonMapper.parseContributionType('bits')
        assert result is TwitchContributionType.BITS

    @pytest.mark.asyncio
    async def test_parseContributionType_withEmptyString(self):
        result = await self.jsonMapper.parseContributionType('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseContributionType_withNone(self):
        result = await self.jsonMapper.parseContributionType(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseContributionType_withOther(self):
        result = await self.jsonMapper.parseContributionType('other')
        assert result is TwitchContributionType.OTHER

    @pytest.mark.asyncio
    async def test_parseContributionType_withSubscription(self):
        result = await self.jsonMapper.parseContributionType('subscription')
        assert result is TwitchContributionType.SUBSCRIPTION

    @pytest.mark.asyncio
    async def test_parseContributionType_withWhitespaceString(self):
        result = await self.jsonMapper.parseContributionType(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseEmoteFormat_withAnimatedString(self):
        result = await self.jsonMapper.parseEmoteImageFormat('animated')
        assert result is TwitchEmoteImageFormat.ANIMATED

    @pytest.mark.asyncio
    async def test_parseEmoteFormat_withEmptyString(self):
        result = await self.jsonMapper.parseEmoteImageFormat('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseEmoteFormat_withNone(self):
        result = await self.jsonMapper.parseEmoteImageFormat(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseEmoteFormat_withStaticString(self):
        result = await self.jsonMapper.parseEmoteImageFormat('static')
        assert result is TwitchEmoteImageFormat.STATIC

    @pytest.mark.asyncio
    async def test_parseEmoteFormat_withWhitespaceString(self):
        result = await self.jsonMapper.parseEmoteImageFormat(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseEmoteImageScale_withEmptyString(self):
        result = await self.jsonMapper.parseEmoteImageScale('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseEmoteImageScale_withNone(self):
        result = await self.jsonMapper.parseEmoteImageScale(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseEmoteImageScale_withWhitespaceString(self):
        result = await self.jsonMapper.parseEmoteImageScale(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseEmoteImageScale_withUrl_1xString(self):
        result = await self.jsonMapper.parseEmoteImageScale('url_1x')
        assert result is TwitchEmoteImageScale.SMALL

    @pytest.mark.asyncio
    async def test_parseEmoteImageScale_withUrl_2xString(self):
        result = await self.jsonMapper.parseEmoteImageScale('url_2x')
        assert result is TwitchEmoteImageScale.MEDIUM

    @pytest.mark.asyncio
    async def test_parseEmoteImageScale_withUrl_4xString(self):
        result = await self.jsonMapper.parseEmoteImageScale('url_4x')
        assert result is TwitchEmoteImageScale.LARGE

    @pytest.mark.asyncio
    async def test_parseEmoteImageScale_with1_0String(self):
        result = await self.jsonMapper.parseEmoteImageScale('1.0')
        assert result is TwitchEmoteImageScale.SMALL

    @pytest.mark.asyncio
    async def test_parseEmoteImageScale_with2_0String(self):
        result = await self.jsonMapper.parseEmoteImageScale('2.0')
        assert result is TwitchEmoteImageScale.MEDIUM

    @pytest.mark.asyncio
    async def test_parseEmoteImageScale_with3_0String(self):
        result = await self.jsonMapper.parseEmoteImageScale('3.0')
        assert result is TwitchEmoteImageScale.LARGE

    @pytest.mark.asyncio
    async def test_parseEmoteType_withBitstierString(self):
        result = await self.jsonMapper.parseEmoteType('bitstier')
        assert result is TwitchEmoteType.BITS

    @pytest.mark.asyncio
    async def test_parseEmoteType_withEmptyString(self):
        result = await self.jsonMapper.parseEmoteType('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseEmoteType_withFollowerString(self):
        result = await self.jsonMapper.parseEmoteType('follower')
        assert result is TwitchEmoteType.FOLLOWER

    @pytest.mark.asyncio
    async def test_parseEmoteType_withNone(self):
        result = await self.jsonMapper.parseEmoteType(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseEmoteType_withSubscriptionsString(self):
        result = await self.jsonMapper.parseEmoteType('subscriptions')
        assert result is TwitchEmoteType.SUBSCRIPTIONS

    @pytest.mark.asyncio
    async def test_parseEmoteType_withWhitespaceString(self):
        result = await self.jsonMapper.parseEmoteType(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseHypeTrainType_withEmptyString(self):
        result = await self.jsonMapper.parseHypeTrainType('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseHypeTrainType_withGoldenKappa(self):
        result = await self.jsonMapper.parseHypeTrainType('golden_kappa')
        assert result is TwitchHypeTrainType.GOLDEN_KAPPA

    @pytest.mark.asyncio
    async def test_parseHypeTrainType_withNone(self):
        result = await self.jsonMapper.parseHypeTrainType(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseHypeTrainType_withRegular(self):
        result = await self.jsonMapper.parseHypeTrainType('regular')
        assert result is TwitchHypeTrainType.REGULAR

    @pytest.mark.asyncio
    async def test_parseHypeTrainType_withTreasure(self):
        result = await self.jsonMapper.parseHypeTrainType('treasure')
        assert result is TwitchHypeTrainType.TREASURE

    @pytest.mark.asyncio
    async def test_parseHypeTrainType_withWhitespaceString(self):
        result = await self.jsonMapper.parseHypeTrainType(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseNoticeType_withAnnouncementString(self):
        result = await self.jsonMapper.parseNoticeType('announcement')
        assert result is TwitchNoticeType.ANNOUNCEMENT

    @pytest.mark.asyncio
    async def test_parseNoticeType_withBitsBadgeTierString(self):
        result = await self.jsonMapper.parseNoticeType('bits_badge_tier')
        assert result is TwitchNoticeType.BITS_BADGE_TIER

    @pytest.mark.asyncio
    async def test_parseNoticeType_withCharityDonationString(self):
        result = await self.jsonMapper.parseNoticeType('charity_donation')
        assert result is TwitchNoticeType.CHARITY_DONATION

    @pytest.mark.asyncio
    async def test_parseNoticeType_withCommunitySubGiftString(self):
        result = await self.jsonMapper.parseNoticeType('community_sub_gift')
        assert result is TwitchNoticeType.COMMUNITY_SUB_GIFT

    @pytest.mark.asyncio
    async def test_parseNoticeType_withGiftPaidUpgradeString(self):
        result = await self.jsonMapper.parseNoticeType('gift_paid_upgrade')
        assert result is TwitchNoticeType.GIFT_PAID_UPGRADE

    @pytest.mark.asyncio
    async def test_parseNoticeType_withEmptyString(self):
        result = await self.jsonMapper.parseNoticeType('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseNoticeType_withNone(self):
        result = await self.jsonMapper.parseNoticeType(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseNoticeType_withPayItForwardString(self):
        result = await self.jsonMapper.parseNoticeType('pay_it_forward')
        assert result is TwitchNoticeType.PAY_IT_FORWARD

    @pytest.mark.asyncio
    async def test_parseNoticeType_withPrimePaidUpgradeString(self):
        result = await self.jsonMapper.parseNoticeType('prime_paid_upgrade')
        assert result is TwitchNoticeType.PRIME_PAID_UPGRADE

    @pytest.mark.asyncio
    async def test_parseNoticeType_withRaidString(self):
        result = await self.jsonMapper.parseNoticeType('raid')
        assert result is TwitchNoticeType.RAID

    @pytest.mark.asyncio
    async def test_parseNoticeType_withResubString(self):
        result = await self.jsonMapper.parseNoticeType('resub')
        assert result is TwitchNoticeType.RE_SUB

    @pytest.mark.asyncio
    async def test_parseNoticeType_withSubString(self):
        result = await self.jsonMapper.parseNoticeType('sub')
        assert result is TwitchNoticeType.SUB

    @pytest.mark.asyncio
    async def test_parseNoticeType_withSubGiftString(self):
        result = await self.jsonMapper.parseNoticeType('sub_gift')
        assert result is TwitchNoticeType.SUB_GIFT

    @pytest.mark.asyncio
    async def test_parseNoticeType_withUnraidString(self):
        result = await self.jsonMapper.parseNoticeType('unraid')
        assert result is TwitchNoticeType.UN_RAID

    @pytest.mark.asyncio
    async def test_parseNoticeType_withWhitespaceString(self):
        result = await self.jsonMapper.parseNoticeType(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseOutcomeColor_withBlue(self):
        result = await self.jsonMapper.parseOutcomeColor('blue')
        assert result is TwitchOutcomeColor.BLUE

    @pytest.mark.asyncio
    async def test_parseOutcomeColor_withEmptyString(self):
        result = await self.jsonMapper.parseOutcomeColor('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseOutcomeColor_withNone(self):
        result = await self.jsonMapper.parseOutcomeColor(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseOutcomeColor_withPink(self):
        result = await self.jsonMapper.parseOutcomeColor('pink')
        assert result is TwitchOutcomeColor.PINK

    @pytest.mark.asyncio
    async def test_parseOutcomeColor_withWhitespaceString(self):
        result = await self.jsonMapper.parseOutcomeColor(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parsePaginationResponse(self):
        cursor = 'abc123'

        result = await self.jsonMapper.parsePaginationResponse({
            'cursor': cursor
        })

        assert isinstance(result, TwitchPaginationResponse)
        assert result.cursor == 'abc123'

    @pytest.mark.asyncio
    async def test_parsePaginationResponse_withBlankCursor(self):
        cursor = ''

        result = await self.jsonMapper.parsePaginationResponse({
            'cursor': cursor
        })

        assert result is None

    @pytest.mark.asyncio
    async def test_parsePaginationResponse_withEmptyDictionary(self):
        result = await self.jsonMapper.parsePaginationResponse(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parsePaginationResponse_withNone(self):
        result = await self.jsonMapper.parsePaginationResponse(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parsePaginationResponse_withNoneCursor(self):
        cursor: str | None = None

        result = await self.jsonMapper.parsePaginationResponse({
            'cursor': cursor
        })

        assert result is None

    @pytest.mark.asyncio
    async def test_parsePollStatus_withActive(self):
        result = await self.jsonMapper.parsePollStatus('active')
        assert result is TwitchPollStatus.ACTIVE

    @pytest.mark.asyncio
    async def test_parsePollStatus_withArchived(self):
        result = await self.jsonMapper.parsePollStatus('archived')
        assert result is TwitchPollStatus.ARCHIVED

    @pytest.mark.asyncio
    async def test_parsePollStatus_withCompleted(self):
        result = await self.jsonMapper.parsePollStatus('completed')
        assert result is TwitchPollStatus.COMPLETED

    @pytest.mark.asyncio
    async def test_parsePollStatus_withEmptyString(self):
        result = await self.jsonMapper.parsePollStatus('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parsePollStatus_withInvalid(self):
        result = await self.jsonMapper.parsePollStatus('invalid')
        assert result is TwitchPollStatus.INVALID

    @pytest.mark.asyncio
    async def test_parsePollStatus_withModerated(self):
        result = await self.jsonMapper.parsePollStatus('moderated')
        assert result is TwitchPollStatus.MODERATED

    @pytest.mark.asyncio
    async def test_parsePollStatus_withNone(self):
        result = await self.jsonMapper.parsePollStatus(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parsePollStatus_withTerminated(self):
        result = await self.jsonMapper.parsePollStatus('terminated')
        assert result is TwitchPollStatus.TERMINATED

    @pytest.mark.asyncio
    async def test_parsePollStatus_withWhitespaceString(self):
        result = await self.jsonMapper.parsePollStatus(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parsePowerUp_withEmptyDictionary(self):
        result = await self.jsonMapper.parsePowerUp(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parsePowerUp_withNone(self):
        result = await self.jsonMapper.parsePowerUp(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parsePowerUpEmote(self):
        powerUpEmote = TwitchPowerUpEmote(
            emoteId = 'abc123',
            emoteName = 'samusWow',
        )

        result = await self.jsonMapper.parsePowerUpEmote({
            'id': powerUpEmote.emoteId,
            'name': powerUpEmote.emoteName,
        })

        assert isinstance(result, TwitchPowerUpEmote)
        assert result == powerUpEmote
        assert result.emoteId == powerUpEmote.emoteId
        assert result.emoteName == powerUpEmote.emoteName

    @pytest.mark.asyncio
    async def test_parsePowerUpEmote_withEmptyDictionary(self):
        result = await self.jsonMapper.parsePowerUpEmote(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parsePowerUpEmote_withNone(self):
        result = await self.jsonMapper.parsePowerUpEmote(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parsePowerUpType_withCelebration(self):
        result = await self.jsonMapper.parsePowerUpType('celebration')
        assert result is TwitchPowerUpType.CELEBRATION

    @pytest.mark.asyncio
    async def test_parsePowerUpType_withEmptyString(self):
        result = await self.jsonMapper.parsePowerUpType('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parsePowerUpType_withGigantifyAnEmote(self):
        result = await self.jsonMapper.parsePowerUpType('gigantify_an_emote')
        assert result is TwitchPowerUpType.GIGANTIFY_AN_EMOTE

    @pytest.mark.asyncio
    async def test_parsePowerUpType_withMessageEffect(self):
        result = await self.jsonMapper.parsePowerUpType('message_effect')
        assert result is TwitchPowerUpType.MESSAGE_EFFECT

    @pytest.mark.asyncio
    async def test_parsePowerUpType_withNone(self):
        result = await self.jsonMapper.parsePowerUpType(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parsePowerUpType_withWhitespaceString(self):
        result = await self.jsonMapper.parsePowerUpType(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parsePredictionStatus_withActive(self):
        result = await self.jsonMapper.parsePredictionStatus('active')
        assert result is TwitchPredictionStatus.ACTIVE

    @pytest.mark.asyncio
    async def test_parsePredictionStatus_withCanceled(self):
        result = await self.jsonMapper.parsePredictionStatus('canceled')
        assert result is TwitchPredictionStatus.CANCELED

    @pytest.mark.asyncio
    async def test_parsePredictionStatus_withLocked(self):
        result = await self.jsonMapper.parsePredictionStatus('locked')
        assert result is TwitchPredictionStatus.LOCKED

    @pytest.mark.asyncio
    async def test_parsePredictionStatus_withResolved(self):
        result = await self.jsonMapper.parsePredictionStatus('resolved')
        assert result is TwitchPredictionStatus.RESOLVED

    @pytest.mark.asyncio
    async def test_parsePredictionStatus_withWhitespaceString(self):
        result = await self.jsonMapper.parsePredictionStatus(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseRaid(self):
        userId = 'abc123'
        userLogin = 'smcharles'
        userName = 'smCharles'
        profileImageUrl = 'https://joinmastodon.org/'
        viewerCount = 100

        result = await self.jsonMapper.parseRaid({
            'profile_image_url': profileImageUrl,
            'user_id': userId,
            'user_login': userLogin,
            'user_name': userName,
            'viewer_count': viewerCount
        })

        assert isinstance(result, TwitchRaid)
        assert result.profileImageUrl == profileImageUrl
        assert result.userId == userId
        assert result.userLogin == userLogin
        assert result.userName == userName
        assert result.viewerCount == viewerCount

    @pytest.mark.asyncio
    async def test_parseRaid_withEmptyDictionary(self):
        result = await self.jsonMapper.parseRaid(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseRaid_withNone(self):
        result = await self.jsonMapper.parseRaid(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseResub_withEmptyDictionary(self):
        result = await self.jsonMapper.parseResub(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseResub_withNone(self):
        result = await self.jsonMapper.parseResub(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseReward_withEmptyDictionary(self):
        result = await self.jsonMapper.parseReward(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseReward_withNone(self):
        result = await self.jsonMapper.parseReward(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseRewardRedemptionStatus_withCanceled(self):
        result = await self.jsonMapper.parseRewardRedemptionStatus('canceled')
        assert result is TwitchRewardRedemptionStatus.CANCELED

    @pytest.mark.asyncio
    async def test_parseRewardRedemptionStatus_withFulfilledString(self):
        result = await self.jsonMapper.parseRewardRedemptionStatus('fulfilled')
        assert result is TwitchRewardRedemptionStatus.FULFILLED

    @pytest.mark.asyncio
    async def test_parseRewardRedemptionStatus_withEmptyString(self):
        result = await self.jsonMapper.parseRewardRedemptionStatus('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseRewardRedemptionStatus_withNone(self):
        result = await self.jsonMapper.parseRewardRedemptionStatus(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseRewardRedemptionStatus_withUnfulfilledString(self):
        result = await self.jsonMapper.parseRewardRedemptionStatus('unfulfilled')
        assert result is TwitchRewardRedemptionStatus.UNFULFILLED

    @pytest.mark.asyncio
    async def test_parseRewardRedemptionStatus_withUnknownString(self):
        result = await self.jsonMapper.parseRewardRedemptionStatus('unknown')
        assert result is TwitchRewardRedemptionStatus.UNKNOWN

    @pytest.mark.asyncio
    async def test_parseRewardRedemptionStatus_withWhitespaceString(self):
        result = await self.jsonMapper.parseRewardRedemptionStatus(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseStartCommercialDetails(self):
        length = 120
        retryAfter = 600
        message = 'Commercial started!'

        jsonResponse: dict[str, Any] = {
            'length': length,
            'retry_after': retryAfter,
            'message': message
        }

        result = await self.jsonMapper.parseStartCommercialDetails(jsonResponse)
        assert isinstance(result, TwitchStartCommercialDetails)
        assert result.length == length
        assert result.retryAfter == retryAfter
        assert result.message == message

    @pytest.mark.asyncio
    async def test_parseStartCommercialDetails_withEmptyDictionary(self):
        result = await self.jsonMapper.parseStartCommercialDetails(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseStartCommercialDetails_withNone(self):
        result = await self.jsonMapper.parseStartCommercialDetails(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseStartCommercialDetails_withNoneMessage(self):
        length = 120
        retryAfter = 600

        jsonResponse: dict[str, Any] = {
            'length': length,
            'retry_after': retryAfter
        }

        result = await self.jsonMapper.parseStartCommercialDetails(jsonResponse)
        assert isinstance(result, TwitchStartCommercialDetails)
        assert result.length == length
        assert result.retryAfter == retryAfter
        assert result.message is None

    @pytest.mark.asyncio
    async def test_parseStartCommercialDetails_withNoneRetryAfterAndNoneMessage(self):
        length = 60

        jsonResponse: dict[str, Any] = {
            'length': length
        }

        result = await self.jsonMapper.parseStartCommercialDetails(jsonResponse)
        assert isinstance(result, TwitchStartCommercialDetails)
        assert result.length == length
        assert result.retryAfter is None
        assert result.message is None

    @pytest.mark.asyncio
    async def test_parseStreamType_withEmptyString(self):
        result = await self.jsonMapper.parseStreamType('')
        assert result is TwitchStreamType.UNKNOWN

    @pytest.mark.asyncio
    async def test_parseStreamType_withLive(self):
        result = await self.jsonMapper.parseStreamType('live')
        assert result is TwitchStreamType.LIVE

    @pytest.mark.asyncio
    async def test_parseStreamType_withNone(self):
        result = await self.jsonMapper.parseStreamType(None)
        assert result is TwitchStreamType.UNKNOWN

    @pytest.mark.asyncio
    async def test_parseStreamType_withWhitespaceString(self):
        result = await self.jsonMapper.parseStreamType(' ')
        assert result is TwitchStreamType.UNKNOWN

    @pytest.mark.asyncio
    async def test_parseSubscriberTier_withPrimeString(self):
        result = await self.jsonMapper.parseSubscriberTier('prime')
        assert result is TwitchSubscriberTier.PRIME

    @pytest.mark.asyncio
    async def test_parseSubscriberTier_with1000String(self):
        result = await self.jsonMapper.parseSubscriberTier('1000')
        assert result is TwitchSubscriberTier.TIER_ONE

    @pytest.mark.asyncio
    async def test_parseSubscriberTier_with2000String(self):
        result = await self.jsonMapper.parseSubscriberTier('2000')
        assert result is TwitchSubscriberTier.TIER_TWO

    @pytest.mark.asyncio
    async def test_parseSubscriberTier_with3000String(self):
        result = await self.jsonMapper.parseSubscriberTier('3000')
        assert result is TwitchSubscriberTier.TIER_THREE

    @pytest.mark.asyncio
    async def test_parseSubscriberTier_withEmptyString(self):
        result = await self.jsonMapper.parseSubscriberTier('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseSubscriberTier_withNone(self):
        result = await self.jsonMapper.parseSubscriberTier(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseSubscriberTier_withWhitespaceString(self):
        result = await self.jsonMapper.parseSubscriberTier(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseSubscriptionType_withChannelChatMessage(self):
        result = await self.jsonMapper.parseSubscriptionType('channel.chat.message')
        assert result is TwitchWebsocketSubscriptionType.CHANNEL_CHAT_MESSAGE

    @pytest.mark.asyncio
    async def test_parseSubscriptionType_withChannelCheerString(self):
        result = await self.jsonMapper.parseSubscriptionType('channel.cheer')
        assert result is TwitchWebsocketSubscriptionType.CHEER

    @pytest.mark.asyncio
    async def test_parseSubscriptionType_withChannelPollBeginString(self):
        result = await self.jsonMapper.parseSubscriptionType('channel.poll.begin')
        assert result is TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN

    @pytest.mark.asyncio
    async def test_parseSubscriptionType_withChannelPollEndString(self):
        result = await self.jsonMapper.parseSubscriptionType('channel.poll.end')
        assert result is TwitchWebsocketSubscriptionType.CHANNEL_POLL_END

    @pytest.mark.asyncio
    async def test_parseSubscriptionType_withChannelProgressString(self):
        result = await self.jsonMapper.parseSubscriptionType('channel.poll.progress')
        assert result is TwitchWebsocketSubscriptionType.CHANNEL_POLL_PROGRESS

    @pytest.mark.asyncio
    async def test_parseSubscriptionType_withChannelFollowString(self):
        result = await self.jsonMapper.parseSubscriptionType('channel.follow')
        assert result is TwitchWebsocketSubscriptionType.FOLLOW

    @pytest.mark.asyncio
    async def test_parseSubscriptionType_withChannelPredictionBeginString(self):
        result = await self.jsonMapper.parseSubscriptionType('channel.prediction.begin')
        assert result is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN

    @pytest.mark.asyncio
    async def test_parseSubscriptionType_withChannelRaidString(self):
        result = await self.jsonMapper.parseSubscriptionType('channel.raid')
        assert result is TwitchWebsocketSubscriptionType.RAID

    @pytest.mark.asyncio
    async def test_parseSubscriptionType_withChannelSubscribeString(self):
        result = await self.jsonMapper.parseSubscriptionType('channel.subscribe')
        assert result is TwitchWebsocketSubscriptionType.SUBSCRIBE

    @pytest.mark.asyncio
    async def test_parseSubscriptionType_withChannelSubscriptionGiftString(self):
        result = await self.jsonMapper.parseSubscriptionType('channel.subscription.gift')
        assert result is TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT

    @pytest.mark.asyncio
    async def test_parseSubscriptionType_withChannelSubscriptionMessageString(self):
        result = await self.jsonMapper.parseSubscriptionType('channel.subscription.message')
        assert result is TwitchWebsocketSubscriptionType.SUBSCRIPTION_MESSAGE

    @pytest.mark.asyncio
    async def test_parseSubscriptionType_withEmptyString(self):
        result = await self.jsonMapper.parseSubscriptionType('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseSubscriptionType_withNone(self):
        result = await self.jsonMapper.parseSubscriptionType(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseSubscriptionType_withStreamOfflineString(self):
        result = await self.jsonMapper.parseSubscriptionType('stream.offline')
        assert result is TwitchWebsocketSubscriptionType.STREAM_OFFLINE

    @pytest.mark.asyncio
    async def test_parseSubscriptionType_withStreamOnlineString(self):
        result = await self.jsonMapper.parseSubscriptionType('stream.online')
        assert result is TwitchWebsocketSubscriptionType.STREAM_ONLINE

    @pytest.mark.asyncio
    async def test_parseSubscriptionType_withUserUpdateString(self):
        result = await self.jsonMapper.parseSubscriptionType('user.update')
        assert result is TwitchWebsocketSubscriptionType.USER_UPDATE

    @pytest.mark.asyncio
    async def test_parseSubscriptionType_withWhitespaceString(self):
        result = await self.jsonMapper.parseSubscriptionType(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTransportMethod_withEmptyString(self):
        result = await self.jsonMapper.parseTransportMethod('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTransportMethod_withNone(self):
        result = await self.jsonMapper.parseTransportMethod(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTransportMethod_withConduit(self):
        result = await self.jsonMapper.parseTransportMethod('conduit')
        assert result is TwitchWebsocketTransportMethod.CONDUIT

    @pytest.mark.asyncio
    async def test_parseTransportMethod_withWebhook(self):
        result = await self.jsonMapper.parseTransportMethod('webhook')
        assert result is TwitchWebsocketTransportMethod.WEBHOOK

    @pytest.mark.asyncio
    async def test_parseTransportMethod_withWebsocket(self):
        result = await self.jsonMapper.parseTransportMethod('websocket')
        assert result is TwitchWebsocketTransportMethod.WEBSOCKET

    @pytest.mark.asyncio
    async def test_parseTransportMethod_withWhitespaceString(self):
        result = await self.jsonMapper.parseTransportMethod(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseUserType_withAdminString(self):
        result = await self.jsonMapper.parseUserType('admin')
        assert result is TwitchUserType.ADMIN

    @pytest.mark.asyncio
    async def test_parseUserType_withEmptyString(self):
        result = await self.jsonMapper.parseUserType('')
        assert result is TwitchUserType.NORMAL

    @pytest.mark.asyncio
    async def test_parseUserType_withGlobalModString(self):
        result = await self.jsonMapper.parseUserType('global_mod')
        assert result is TwitchUserType.GLOBAL_MOD

    @pytest.mark.asyncio
    async def test_parseUserType_withNone(self):
        result = await self.jsonMapper.parseUserType(None)
        assert result is TwitchUserType.NORMAL

    @pytest.mark.asyncio
    async def test_parseUserType_withStaffString(self):
        result = await self.jsonMapper.parseUserType('staff')
        assert result is TwitchUserType.STAFF

    @pytest.mark.asyncio
    async def test_parseUserType_withWhitespaceString(self):
        result = await self.jsonMapper.parseUserType(' ')
        assert result is TwitchUserType.NORMAL

    @pytest.mark.asyncio
    async def test_parseWebsocketChannelPointsVoting(self):
        isEnabled = True
        amountPerVote = 100

        result = await self.jsonMapper.parseWebsocketChannelPointsVoting({
            'is_enabled': isEnabled,
            'amount_per_vote': amountPerVote
        })

        assert isinstance(result, TwitchWebsocketChannelPointsVoting)
        assert result.isEnabled == isEnabled
        assert result.amountPerVote == amountPerVote

    @pytest.mark.asyncio
    async def test_parseWebsocketChannelPointsVoting_withEmptyDictionary(self):
        result = await self.jsonMapper.parseWebsocketChannelPointsVoting(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketChannelPointsVoting_withNone(self):
        result = await self.jsonMapper.parseWebsocketChannelPointsVoting(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketMessageType_withEmptyString(self):
        result = await self.jsonMapper.parseWebsocketMessageType('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketMessageType_withNone(self):
        result = await self.jsonMapper.parseWebsocketMessageType(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketMessageType_withNotificationString(self):
        result = await self.jsonMapper.parseWebsocketMessageType('notification')
        assert result is TwitchWebsocketMessageType.NOTIFICATION

    @pytest.mark.asyncio
    async def test_parseWebsocketMessageType_withRevocationString(self):
        result = await self.jsonMapper.parseWebsocketMessageType('revocation')
        assert result is TwitchWebsocketMessageType.REVOCATION

    @pytest.mark.asyncio
    async def test_parseWebsocketMessageType_withSessionKeepAliveString(self):
        result = await self.jsonMapper.parseWebsocketMessageType('session_keepalive')
        assert result is TwitchWebsocketMessageType.KEEP_ALIVE

    @pytest.mark.asyncio
    async def test_parseWebsocketMessageType_withSessionReconnectString(self):
        result = await self.jsonMapper.parseWebsocketMessageType('session_reconnect')
        assert result is TwitchWebsocketMessageType.RECONNECT

    @pytest.mark.asyncio
    async def test_parseWebsocketMessageType_withSessionWelcomeString(self):
        result = await self.jsonMapper.parseWebsocketMessageType('session_welcome')
        assert result is TwitchWebsocketMessageType.WELCOME

    @pytest.mark.asyncio
    async def test_parseWebsocketMessageType_withWhitespaceString(self):
        result = await self.jsonMapper.parseWebsocketMessageType(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketMetadata_withEmptyDictionary(self):
        result = await self.jsonMapper.parseWebsocketMetadata(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketMetadata_withNone(self):
        result = await self.jsonMapper.parseWebsocketMetadata(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketSub(self):
        isPrime = False
        durationMonths = 12
        subTier = '1000'

        result = await self.jsonMapper.parseWebsocketSub({
            'is_prime': isPrime,
            'duration_months': durationMonths,
            'sub_tier': subTier
        })

        assert isinstance(result, TwitchWebsocketSub)
        assert result.isPrime == isPrime
        assert result.durationMonths == durationMonths
        assert result.subTier is TwitchSubscriberTier.TIER_ONE

    @pytest.mark.asyncio
    async def test_parseWebsocketSub_withEmptyDictionary(self):
        result = await self.jsonMapper.parseWebsocketSub(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketSub_withNone(self):
        result = await self.jsonMapper.parseWebsocketSub(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_requireChatMessageFragmentType_withCheermoteString(self):
        result = await self.jsonMapper.requireChatMessageFragmentType('cheermote')
        assert result is TwitchChatMessageFragmentType.CHEERMOTE

    @pytest.mark.asyncio
    async def test_requireChatMessageFragmentType_withEmoteString(self):
        result = await self.jsonMapper.requireChatMessageFragmentType('emote')
        assert result is TwitchChatMessageFragmentType.EMOTE

    @pytest.mark.asyncio
    async def test_requireChatMessageFragmentType_withEmptyString(self):
        result: TwitchChatMessageFragmentType | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.requireChatMessageFragmentType('')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireChatMessageFragmentType_withMentionString(self):
        result = await self.jsonMapper.requireChatMessageFragmentType('mention')
        assert result is TwitchChatMessageFragmentType.MENTION

    @pytest.mark.asyncio
    async def test_requireChatMessageFragmentType_withNone(self):
        result: TwitchChatMessageFragmentType | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.requireChatMessageFragmentType(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireChatMessageFragmentType_withTextString(self):
        result = await self.jsonMapper.requireChatMessageFragmentType('text')
        assert result is TwitchChatMessageFragmentType.TEXT

    @pytest.mark.asyncio
    async def test_requireChatMessageFragmentType_withWhitespaceString(self):
        result: TwitchChatMessageFragmentType | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.requireChatMessageFragmentType(' ')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireConnectionStatus_withAuthorizationRevokedString(self):
        result = await self.jsonMapper.requireConnectionStatus('authorization_revoked')
        assert result is TwitchWebsocketConnectionStatus.REVOKED

    @pytest.mark.asyncio
    async def test_requireConnectionStatus_withEmptyString(self):
        result: TwitchWebsocketConnectionStatus | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.requireConnectionStatus('')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireConnectionStatus_withConnectedString(self):
        result = await self.jsonMapper.requireConnectionStatus('connected')
        assert result is TwitchWebsocketConnectionStatus.CONNECTED

    @pytest.mark.asyncio
    async def test_requireConnectionStatus_withEnabledString(self):
        result = await self.jsonMapper.requireConnectionStatus('enabled')
        assert result is TwitchWebsocketConnectionStatus.ENABLED

    @pytest.mark.asyncio
    async def test_requireConnectionStatus_withNone(self):
        result: TwitchWebsocketConnectionStatus | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.requireConnectionStatus(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireConnectionStatus_withReconnectingString(self):
        result = await self.jsonMapper.requireConnectionStatus('reconnecting')
        assert result is TwitchWebsocketConnectionStatus.RECONNECTING

    @pytest.mark.asyncio
    async def test_requireConnectionStatus_withUserRemovedString(self):
        result = await self.jsonMapper.requireConnectionStatus('user_removed')
        assert result is TwitchWebsocketConnectionStatus.USER_REMOVED

    @pytest.mark.asyncio
    async def test_requireConnectionStatus_withVersionRemovedString(self):
        result = await self.jsonMapper.requireConnectionStatus('version_removed')
        assert result is TwitchWebsocketConnectionStatus.VERSION_REMOVED

    @pytest.mark.asyncio
    async def test_requireConnectionStatus_withWhitespaceString(self):
        result: TwitchWebsocketConnectionStatus | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.requireConnectionStatus(' ')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireContributionType_withBits(self):
        result = await self.jsonMapper.requireContributionType('bits')
        assert result is TwitchContributionType.BITS

    @pytest.mark.asyncio
    async def test_requireContributionType_withEmptyString(self):
        result: TwitchContributionType | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.requireContributionType('')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireContributionType_withNone(self):
        result: TwitchContributionType | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.requireContributionType(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireContributionType_withOther(self):
        result = await self.jsonMapper.requireContributionType('other')
        assert result is TwitchContributionType.OTHER

    @pytest.mark.asyncio
    async def test_requireContributionType_withSubscription(self):
        result = await self.jsonMapper.requireContributionType('subscription')
        assert result is TwitchContributionType.SUBSCRIPTION

    @pytest.mark.asyncio
    async def test_requireContributionType_withWhitespaceString(self):
        result: TwitchContributionType | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.requireContributionType(' ')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireNoticeType_withAnnouncementString(self):
        result = await self.jsonMapper.requireNoticeType('announcement')
        assert result is TwitchNoticeType.ANNOUNCEMENT

    @pytest.mark.asyncio
    async def test_requireNoticeType_withBitsBadgeTierString(self):
        result = await self.jsonMapper.requireNoticeType('bits_badge_tier')
        assert result is TwitchNoticeType.BITS_BADGE_TIER

    @pytest.mark.asyncio
    async def test_requireNoticeType_withCharityDonationString(self):
        result = await self.jsonMapper.requireNoticeType('charity_donation')
        assert result is TwitchNoticeType.CHARITY_DONATION

    @pytest.mark.asyncio
    async def test_requireNoticeType_withCommunitySubGiftString(self):
        result = await self.jsonMapper.requireNoticeType('community_sub_gift')
        assert result is TwitchNoticeType.COMMUNITY_SUB_GIFT

    @pytest.mark.asyncio
    async def test_requireNoticeType_withGiftPaidUpgradeString(self):
        result = await self.jsonMapper.requireNoticeType('gift_paid_upgrade')
        assert result is TwitchNoticeType.GIFT_PAID_UPGRADE

    @pytest.mark.asyncio
    async def test_requireNoticeType_withEmptyString(self):
        result: TwitchNoticeType | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.requireNoticeType('')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireNoticeType_withNone(self):
        result: TwitchNoticeType | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.requireNoticeType(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireNoticeType_withPayItForwardString(self):
        result = await self.jsonMapper.requireNoticeType('pay_it_forward')
        assert result is TwitchNoticeType.PAY_IT_FORWARD

    @pytest.mark.asyncio
    async def test_requireNoticeType_withPrimePaidUpgradeString(self):
        result = await self.jsonMapper.requireNoticeType('prime_paid_upgrade')
        assert result is TwitchNoticeType.PRIME_PAID_UPGRADE

    @pytest.mark.asyncio
    async def test_requireNoticeType_withRaidString(self):
        result = await self.jsonMapper.requireNoticeType('raid')
        assert result is TwitchNoticeType.RAID

    @pytest.mark.asyncio
    async def test_requireNoticeType_withResubString(self):
        result = await self.jsonMapper.requireNoticeType('resub')
        assert result is TwitchNoticeType.RE_SUB

    @pytest.mark.asyncio
    async def test_requireNoticeType_withSubString(self):
        result = await self.jsonMapper.requireNoticeType('sub')
        assert result is TwitchNoticeType.SUB

    @pytest.mark.asyncio
    async def test_requireNoticeType_withSubGiftString(self):
        result = await self.jsonMapper.requireNoticeType('sub_gift')
        assert result is TwitchNoticeType.SUB_GIFT

    @pytest.mark.asyncio
    async def test_requireNoticeType_withUnraidString(self):
        result = await self.jsonMapper.requireNoticeType('unraid')
        assert result is TwitchNoticeType.UN_RAID

    @pytest.mark.asyncio
    async def test_requireNoticeType_withWhitespaceString(self):
        result: TwitchNoticeType | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.requireNoticeType(' ')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireOutcomeColor_withBlue(self):
        result = await self.jsonMapper.requireOutcomeColor('blue')
        assert result is TwitchOutcomeColor.BLUE

    @pytest.mark.asyncio
    async def test_requireOutcomeColor_withEmptyString(self):
        result: TwitchOutcomeColor | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.requireOutcomeColor('')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireOutcomeColor_withNone(self):
        result: TwitchOutcomeColor | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.requireOutcomeColor(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireOutcomeColor_withPink(self):
        result = await self.jsonMapper.requireOutcomeColor('pink')
        assert result is TwitchOutcomeColor.PINK

    @pytest.mark.asyncio
    async def test_requireOutcomeColor_withWhitespaceString(self):
        result: TwitchOutcomeColor | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.requireOutcomeColor(' ')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireSubscriberTier_withPrimeString(self):
        result = await self.jsonMapper.requireSubscriberTier('prime')
        assert result is TwitchSubscriberTier.PRIME

    @pytest.mark.asyncio
    async def test_requireSubscriberTier_with1000String(self):
        result = await self.jsonMapper.requireSubscriberTier('1000')
        assert result is TwitchSubscriberTier.TIER_ONE

    @pytest.mark.asyncio
    async def test_requireSubscriberTier_with2000String(self):
        result = await self.jsonMapper.requireSubscriberTier('2000')
        assert result is TwitchSubscriberTier.TIER_TWO

    @pytest.mark.asyncio
    async def test_requireSubscriberTier_with3000String(self):
        result = await self.jsonMapper.requireSubscriberTier('3000')
        assert result is TwitchSubscriberTier.TIER_THREE

    @pytest.mark.asyncio
    async def test_requireSubscriberTier_withEmptyString(self):
        result: TwitchSubscriberTier | None = None

        with pytest.raises(Exception):
            result = await self.jsonMapper.requireSubscriberTier('')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireSubscriberTier_withNone(self):
        result: TwitchSubscriberTier | None = None

        with pytest.raises(Exception):
            result = await self.jsonMapper.requireSubscriberTier(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireSubscriberTier_withWhitespaceString(self):
        result: TwitchSubscriberTier | None = None

        with pytest.raises(Exception):
            result = await self.jsonMapper.requireSubscriberTier(' ')

        assert result is None

    @pytest.mark.asyncio
    async def test_parseValidationResponse_withEmptyDictionary(self):
        result = await self.jsonMapper.parseValidationResponse(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseValidationResponse_withNone(self):
        result = await self.jsonMapper.parseValidationResponse(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_requireSubscriptionType_withChannelCheerString(self):
        result = await self.jsonMapper.requireSubscriptionType('channel.cheer')
        assert result is TwitchWebsocketSubscriptionType.CHEER

    @pytest.mark.asyncio
    async def test_requireSubscriptionType_withChannelRaidString(self):
        result = await self.jsonMapper.requireSubscriptionType('channel.raid')
        assert result is TwitchWebsocketSubscriptionType.RAID

    @pytest.mark.asyncio
    async def test_requireSubscriptionType_withNone(self):
        result: TwitchWebsocketSubscriptionType | None = None

        with pytest.raises(Exception):
            result = await self.jsonMapper.requireSubscriptionType(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireTransportMethod_withConduit(self):
        result = await self.jsonMapper.requireTransportMethod('conduit')
        assert result is TwitchWebsocketTransportMethod.CONDUIT

    @pytest.mark.asyncio
    async def test_requireTransportMethod_withEmptyString(self):
        result: TwitchWebsocketTransportMethod | None = None

        with pytest.raises(Exception):
            result = await self.jsonMapper.requireTransportMethod('')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireTransportMethod_withNone(self):
        result: TwitchWebsocketTransportMethod | None = None

        with pytest.raises(Exception):
            result = await self.jsonMapper.requireTransportMethod(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireTransportMethod_withWebhook(self):
        result = await self.jsonMapper.requireTransportMethod('webhook')
        assert result is TwitchWebsocketTransportMethod.WEBHOOK

    @pytest.mark.asyncio
    async def test_requireTransportMethod_withWebsocket(self):
        result = await self.jsonMapper.requireTransportMethod('websocket')
        assert result is TwitchWebsocketTransportMethod.WEBSOCKET

    @pytest.mark.asyncio
    async def test_requireTransportMethod_withWhitespaceString(self):
        result: TwitchWebsocketTransportMethod | None = None

        with pytest.raises(Exception):
            result = await self.jsonMapper.requireTransportMethod(' ')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireWebsocketMessageType_withEmptyString(self):
        result: TwitchWebsocketMessageType | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.requireWebsocketMessageType('')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireWebsocketMessageType_withNone(self):
        result: TwitchWebsocketMessageType | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.requireWebsocketMessageType(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireWebsocketMessageType_withNotificationString(self):
        result = await self.jsonMapper.requireWebsocketMessageType('notification')
        assert result is TwitchWebsocketMessageType.NOTIFICATION

    @pytest.mark.asyncio
    async def test_requireWebsocketMessageType_withRevocationString(self):
        result = await self.jsonMapper.requireWebsocketMessageType('revocation')
        assert result is TwitchWebsocketMessageType.REVOCATION

    @pytest.mark.asyncio
    async def test_requireWebsocketMessageType_withSessionKeepAliveString(self):
        result = await self.jsonMapper.requireWebsocketMessageType('session_keepalive')
        assert result is TwitchWebsocketMessageType.KEEP_ALIVE

    @pytest.mark.asyncio
    async def test_requireWebsocketMessageType_withSessionReconnectString(self):
        result = await self.jsonMapper.requireWebsocketMessageType('session_reconnect')
        assert result is TwitchWebsocketMessageType.RECONNECT

    @pytest.mark.asyncio
    async def test_requireWebsocketMessageType_withSessionWelcomeString(self):
        result = await self.jsonMapper.requireWebsocketMessageType('session_welcome')
        assert result is TwitchWebsocketMessageType.WELCOME

    @pytest.mark.asyncio
    async def test_requireWebsocketMessageType_withWhitespaceString(self):
        result: TwitchWebsocketMessageType | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.requireWebsocketMessageType(' ')

        assert result is None

    def test_sanity(self):
        assert self.jsonMapper is not None
        assert isinstance(self.jsonMapper, TwitchJsonMapper)
        assert isinstance(self.jsonMapper, TwitchJsonMapperInterface)

    @pytest.mark.asyncio
    async def test_serializeBanRequest(self):
        request = TwitchBanRequest(
            duration = None,
            broadcasterUserId = 'abc123',
            moderatorUserId = 'def456',
            reason = None,
            userIdToBan = 'xyz'
        )

        result = await self.jsonMapper.serializeBanRequest(request)
        assert isinstance(result, dict)
        assert len(result) == 1
        assert 'data' in result and isinstance(result['data'], dict)

        data: dict[str, Any] = result['data']
        assert len(data) == 1
        assert data['user_id'] == request.userIdToBan

    @pytest.mark.asyncio
    async def test_serializeBanRequest_withDuration(self):
        request = TwitchBanRequest(
            duration = 60,
            broadcasterUserId = 'abc123',
            moderatorUserId = 'def456',
            reason = None,
            userIdToBan = 'xyz'
        )

        result = await self.jsonMapper.serializeBanRequest(request)
        assert isinstance(result, dict)
        assert len(result) == 1
        assert 'data' in result and isinstance(result['data'], dict)

        data: dict[str, Any] = result['data']
        assert len(data) == 2
        assert data['duration'] == request.duration
        assert data['user_id'] == request.userIdToBan

    @pytest.mark.asyncio
    async def test_serializeBanRequest_withDurationAndReason(self):
        request = TwitchBanRequest(
            duration = 60,
            broadcasterUserId = 'abc123',
            moderatorUserId = 'def456',
            reason = 'Hello, World!',
            userIdToBan = 'xyz'
        )

        result = await self.jsonMapper.serializeBanRequest(request)
        assert isinstance(result, dict)
        assert len(result) == 1
        assert 'data' in result and isinstance(result['data'], dict)

        data: dict[str, Any] = result['data']
        assert len(data) == 3
        assert data['duration'] == request.duration
        assert data['reason'] == request.reason
        assert data['user_id'] == request.userIdToBan

    @pytest.mark.asyncio
    async def test_serializeBanRequest_withReason(self):
        request = TwitchBanRequest(
            duration = None,
            broadcasterUserId = 'abc123',
            moderatorUserId = 'def456',
            reason = 'Hello, World!',
            userIdToBan = 'xyz'
        )

        result = await self.jsonMapper.serializeBanRequest(request)
        assert isinstance(result, dict)
        assert len(result) == 1
        assert 'data' in result and isinstance(result['data'], dict)

        data: dict[str, Any] = result['data']
        assert len(data) == 2
        assert data['reason'] == request.reason
        assert data['user_id'] == request.userIdToBan

    @pytest.mark.asyncio
    async def test_serializeChatAnnouncementColor_withAll(self):
        results: set[str] = set()

        for announcementColor in TwitchChatAnnouncementColor:
            results.add(await self.jsonMapper.serializeChatAnnouncementColor(announcementColor))

        assert len(results) == len(TwitchChatAnnouncementColor)

    @pytest.mark.asyncio
    async def test_serializeChatAnnouncementColor_withBlue(self):
        result = await self.jsonMapper.serializeChatAnnouncementColor(TwitchChatAnnouncementColor.BLUE)
        assert result == 'blue'

    @pytest.mark.asyncio
    async def test_serializeChatAnnouncementColor_withGreen(self):
        result = await self.jsonMapper.serializeChatAnnouncementColor(TwitchChatAnnouncementColor.GREEN)
        assert result == 'green'

    @pytest.mark.asyncio
    async def test_serializeChatAnnouncementColor_withOrange(self):
        result = await self.jsonMapper.serializeChatAnnouncementColor(TwitchChatAnnouncementColor.ORANGE)
        assert result == 'orange'

    @pytest.mark.asyncio
    async def test_serializeChatAnnouncementColor_withPrimary(self):
        result = await self.jsonMapper.serializeChatAnnouncementColor(TwitchChatAnnouncementColor.PRIMARY)
        assert result == 'primary'

    @pytest.mark.asyncio
    async def test_serializeChatAnnouncementColor_withPurple(self):
        result = await self.jsonMapper.serializeChatAnnouncementColor(TwitchChatAnnouncementColor.PURPLE)
        assert result == 'purple'

    @pytest.mark.asyncio
    async def test_serializeConduitRequest(self):
        conduitRequest = TwitchConduitRequest(shardCount = 5)
        result = await self.jsonMapper.serializeConduitRequest(conduitRequest)
        assert isinstance(result, dict)
        assert len(result) == 1
        assert result['shard_count'] == conduitRequest.shardCount

    @pytest.mark.asyncio
    async def test_serializeEventSubRequest1(self):
        condition = TwitchWebsocketCondition(
            broadcasterUserId = 'abc123',
        )

        subscriptionType = TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION

        transport = TwitchWebsocketTransport(
            connectedAt = None,
            disconnectedAt = None,
            callbackUrl = 'https://twitch.tv/',
            conduitId = None,
            secret = None,
            sessionId = 'sessionId',
            method = TwitchWebsocketTransportMethod.WEBSOCKET,
        )

        request = TwitchEventSubRequest(
            twitchChannel = 'smCharles',
            twitchChannelId = condition.requireBroadcasterUserId(),
            condition = condition,
            subscriptionType = subscriptionType,
            transport = transport,
        )

        dictionary = await self.jsonMapper.serializeEventSubRequest(request)
        assert isinstance(dictionary, dict)

        assert 'condition' in dictionary
        assert 'broadcaster_user_id' in dictionary['condition']
        assert condition.broadcasterUserId == dictionary['condition']['broadcaster_user_id']
        assert 'client_id' not in dictionary['condition']
        assert 'from_broadcaster_user_id' not in dictionary['condition']
        assert 'moderator_user_id' not in dictionary['condition']
        assert 'reward_id' not in dictionary['condition']
        assert 'to_broadcaster_user_id' not in dictionary['condition']
        assert 'user_id' not in dictionary['condition']

        assert 'transport' in dictionary
        assert 'method' in dictionary['transport']
        assert dictionary['transport']['method'] == await self.jsonMapper.serializeTransportMethod(transport.method)
        assert 'session_id' in dictionary['transport']
        assert dictionary['transport']['session_id'] == transport.sessionId

        assert 'type' in dictionary
        assert dictionary['type'] == await self.jsonMapper.serializeSubscriptionType(subscriptionType)

        assert 'version' in dictionary
        assert dictionary['version'] == subscriptionType.version

    @pytest.mark.asyncio
    async def test_serializeEventSubRequest2(self):
        condition = TwitchWebsocketCondition(
            broadcasterUserId = 'def987'
        )

        subscriptionType = TwitchWebsocketSubscriptionType.SUBSCRIBE

        transport = TwitchWebsocketTransport(
            connectedAt = None,
            disconnectedAt = None,
            callbackUrl = None,
            conduitId = None,
            secret = None,
            sessionId = 'def456',
            method = TwitchWebsocketTransportMethod.WEBSOCKET
        )

        request = TwitchEventSubRequest(
            twitchChannel = 'smCharles',
            twitchChannelId = condition.requireBroadcasterUserId(),
            condition = condition,
            subscriptionType = subscriptionType,
            transport = transport
        )

        dictionary = await self.jsonMapper.serializeEventSubRequest(request)
        assert isinstance(dictionary, dict)

        assert 'condition' in dictionary
        assert 'broadcaster_user_id' in dictionary['condition']
        assert condition.broadcasterUserId == dictionary['condition']['broadcaster_user_id']
        assert 'client_id' not in dictionary['condition']
        assert 'from_broadcaster_user_id' not in dictionary['condition']
        assert 'moderator_user_id' not in dictionary['condition']
        assert 'reward_id' not in dictionary['condition']
        assert 'to_broadcaster_user_id' not in dictionary['condition']
        assert 'user_id' not in dictionary['condition']

        assert 'transport' in dictionary
        assert 'method' in dictionary['transport']
        assert dictionary['transport']['method'] == await self.jsonMapper.serializeTransportMethod(transport.method)
        assert 'session_id' in dictionary['transport']
        assert dictionary['transport']['session_id'] == transport.sessionId

        assert 'type' in dictionary
        assert dictionary['type'] == await self.jsonMapper.serializeSubscriptionType(subscriptionType)

        assert 'version' in dictionary
        assert dictionary['version'] == subscriptionType.version

    @pytest.mark.asyncio
    async def test_serializeEventSubRequest3(self):
        condition = TwitchWebsocketCondition(
            broadcasterUserId = 'foo',
            moderatorUserId = 'bar'
        )

        subscriptionType = TwitchWebsocketSubscriptionType.SUBSCRIBE

        transport = TwitchWebsocketTransport(
            connectedAt = None,
            disconnectedAt = None,
            callbackUrl = None,
            conduitId = None,
            secret = None,
            sessionId = 'qwerty',
            method = TwitchWebsocketTransportMethod.WEBSOCKET
        )

        request = TwitchEventSubRequest(
            twitchChannel = 'smCharles',
            twitchChannelId = condition.requireBroadcasterUserId(),
            condition = condition,
            subscriptionType = subscriptionType,
            transport = transport
        )

        dictionary = await self.jsonMapper.serializeEventSubRequest(request)
        assert isinstance(dictionary, dict)

        assert 'condition' in dictionary
        assert 'broadcaster_user_id' in dictionary['condition']
        assert condition.broadcasterUserId == dictionary['condition']['broadcaster_user_id']
        assert 'client_id' not in dictionary['condition']
        assert 'from_broadcaster_user_id' not in dictionary['condition']
        assert 'moderator_user_id' in dictionary['condition']
        assert condition.moderatorUserId == dictionary['condition']['moderator_user_id']
        assert 'reward_id' not in dictionary['condition']
        assert 'to_broadcaster_user_id' not in dictionary['condition']
        assert 'user_id' not in dictionary['condition']

        assert 'transport' in dictionary
        assert 'method' in dictionary['transport']
        assert dictionary['transport']['method'] == await self.jsonMapper.serializeTransportMethod(transport.method)
        assert 'session_id' in dictionary['transport']
        assert dictionary['transport']['session_id'] == transport.sessionId

        assert 'type' in dictionary
        assert dictionary['type'] == await self.jsonMapper.serializeSubscriptionType(subscriptionType)

        assert 'version' in dictionary
        assert dictionary['version'] == subscriptionType.version

    @pytest.mark.asyncio
    async def test_serializeSendChatAnnouncementRequest_withColorPurple(self):
        request = TwitchSendChatAnnouncementRequest(
            broadcasterId = 'abc123',
            message = 'Hello, World!',
            moderatorId = 'def456',
            color = TwitchChatAnnouncementColor.PURPLE
        )

        result = await self.jsonMapper.serializeSendChatAnnouncementRequest(request)
        assert isinstance(result, dict)
        assert len(result) == 2

        assert result['color'] == 'purple'
        assert result['message'] == request.message

    @pytest.mark.asyncio
    async def test_serializeSendChatAnnouncementRequest_withoutColor(self):
        request = TwitchSendChatAnnouncementRequest(
            broadcasterId = 'abc123',
            message = 'Hello, World!',
            moderatorId = 'def456',
            color = None
        )

        result = await self.jsonMapper.serializeSendChatAnnouncementRequest(request)
        assert isinstance(result, dict)
        assert len(result) == 1

        assert 'color' not in result
        assert result['message'] == request.message

    @pytest.mark.asyncio
    async def test_serializeSendChatMessageRequest(self):
        request = TwitchSendChatMessageRequest(
            broadcasterId = 'abc123',
            message = 'Hello, World!',
            replyParentMessageId = None,
            senderId = 'def456'
        )

        result = await self.jsonMapper.serializeSendChatMessageRequest(request)
        assert isinstance(result, dict)
        assert len(result) == 3

        assert result['broadcaster_id'] == request.broadcasterId
        assert result['message'] == request.message
        assert result['sender_id'] == request.senderId

    @pytest.mark.asyncio
    async def test_serializeSendChatMessageRequest_withReplyParentMessageId(self):
        request = TwitchSendChatMessageRequest(
            broadcasterId = 'abc123',
            message = 'Hello, World!',
            replyParentMessageId = 'xyz',
            senderId = 'def456'
        )

        result = await self.jsonMapper.serializeSendChatMessageRequest(request)
        assert isinstance(result, dict)
        assert len(result) == 4

        assert result['broadcaster_id'] == request.broadcasterId
        assert result['message'] == request.message
        assert result['reply_parent_message_id'] == request.replyParentMessageId
        assert result['sender_id'] == request.senderId

    @pytest.mark.asyncio
    async def test_serializeSubscriptionType_withAll(self):
        results: set[str] = set()

        for subscriptionType in TwitchWebsocketSubscriptionType:
            results.add(await self.jsonMapper.serializeSubscriptionType(subscriptionType))

        assert len(results) == len(TwitchWebsocketSubscriptionType)

    @pytest.mark.asyncio
    async def test_serializeSubscriptionType_withChannelChatMessage(self):
        string = await self.jsonMapper.serializeSubscriptionType(TwitchWebsocketSubscriptionType.CHANNEL_CHAT_MESSAGE)
        assert string == 'channel.chat.message'

    @pytest.mark.asyncio
    async def test_serializeSubscriptionType_withChannelPointsRedemption(self):
        string = await self.jsonMapper.serializeSubscriptionType(TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION)
        assert string == 'channel.channel_points_custom_reward_redemption.add'

    @pytest.mark.asyncio
    async def test_serializeSubscriptionType_withChannelPollBegin(self):
        string = await self.jsonMapper.serializeSubscriptionType(TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN)
        assert string == 'channel.poll.begin'

    @pytest.mark.asyncio
    async def test_serializeSubscriptionType_withChannelPollEnd(self):
        string = await self.jsonMapper.serializeSubscriptionType(TwitchWebsocketSubscriptionType.CHANNEL_POLL_END)
        assert string == 'channel.poll.end'

    @pytest.mark.asyncio
    async def test_serializeSubscriptionType_withChannelPollProgress(self):
        string = await self.jsonMapper.serializeSubscriptionType(TwitchWebsocketSubscriptionType.CHANNEL_POLL_PROGRESS)
        assert string == 'channel.poll.progress'

    @pytest.mark.asyncio
    async def test_serializeSubscriptionType_withChannelPredictionBegin(self):
        string = await self.jsonMapper.serializeSubscriptionType(TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN)
        assert string == 'channel.prediction.begin'

    @pytest.mark.asyncio
    async def test_serializeSubscriptionType_withChannelPredictionEnd(self):
        string = await self.jsonMapper.serializeSubscriptionType(TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END)
        assert string == 'channel.prediction.end'

    @pytest.mark.asyncio
    async def test_serializeSubscriptionType_withChannelPredictionLock(self):
        string = await self.jsonMapper.serializeSubscriptionType(TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK)
        assert string == 'channel.prediction.lock'

    @pytest.mark.asyncio
    async def test_serializeSubscriptionType_withChannelPredictionProgress(self):
        string = await self.jsonMapper.serializeSubscriptionType(TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS)
        assert string == 'channel.prediction.progress'

    @pytest.mark.asyncio
    async def test_serializeSubscriptionType_withCheer(self):
        string = await self.jsonMapper.serializeSubscriptionType(TwitchWebsocketSubscriptionType.CHEER)
        assert string == 'channel.cheer'

    @pytest.mark.asyncio
    async def test_serializeSubscriptionType_withFollow(self):
        string = await self.jsonMapper.serializeSubscriptionType(TwitchWebsocketSubscriptionType.FOLLOW)
        assert string == 'channel.follow'

    @pytest.mark.asyncio
    async def test_serializeSubscriptionType_withRaid(self):
        string = await self.jsonMapper.serializeSubscriptionType(TwitchWebsocketSubscriptionType.RAID)
        assert string == 'channel.raid'

    @pytest.mark.asyncio
    async def test_serializeSubscriptionType_withStreamOffline(self):
        string = await self.jsonMapper.serializeSubscriptionType(TwitchWebsocketSubscriptionType.STREAM_OFFLINE)
        assert string == 'stream.offline'

    @pytest.mark.asyncio
    async def test_serializeSubscriptionType_withStreamOnline(self):
        string = await self.jsonMapper.serializeSubscriptionType(TwitchWebsocketSubscriptionType.STREAM_ONLINE)
        assert string == 'stream.online'

    @pytest.mark.asyncio
    async def test_serializeSubscriptionType_withSubscribe(self):
        string = await self.jsonMapper.serializeSubscriptionType(TwitchWebsocketSubscriptionType.SUBSCRIBE)
        assert string == 'channel.subscribe'

    @pytest.mark.asyncio
    async def test_serializeSubscriptionType_withSubscriptionGift(self):
        string = await self.jsonMapper.serializeSubscriptionType(TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT)
        assert string == 'channel.subscription.gift'

    @pytest.mark.asyncio
    async def test_serializeSubscriptionType_withSubscriptionMessage(self):
        string = await self.jsonMapper.serializeSubscriptionType(TwitchWebsocketSubscriptionType.SUBSCRIPTION_MESSAGE)
        assert string == 'channel.subscription.message'

    @pytest.mark.asyncio
    async def test_serializeSubscriptionType_withUserUpdate(self):
        string = await self.jsonMapper.serializeSubscriptionType(TwitchWebsocketSubscriptionType.USER_UPDATE)
        assert string == 'user.update'

    @pytest.mark.asyncio
    async def test_serializeTransport_withConduitTransportMethod(self):
        transport = TwitchWebsocketTransport(
            connectedAt = None,
            disconnectedAt = None,
            callbackUrl = None,
            conduitId = 'abc123',
            secret = None,
            sessionId = None,
            method = TwitchWebsocketTransportMethod.CONDUIT,
        )

        result = await self.jsonMapper.serializeTransport(transport)
        assert isinstance(result, dict)
        assert len(result) == 2

        assert result['conduit_id'] == transport.requireConduitId()
        assert result['method'] == await self.jsonMapper.serializeTransportMethod(transport.method)

    @pytest.mark.asyncio
    async def test_serializeTransport_withWebhookTransportMethod(self):
        transport = TwitchWebsocketTransport(
            connectedAt = None,
            disconnectedAt = None,
            callbackUrl = 'https://www.google.com/',
            conduitId = None,
            secret = 'def456',
            sessionId = None,
            method = TwitchWebsocketTransportMethod.WEBHOOK,
        )

        result = await self.jsonMapper.serializeTransport(transport)
        assert isinstance(result, dict)
        assert len(result) == 3

        assert result['callback'] == transport.requireCallbackUrl()
        assert result['method'] == await self.jsonMapper.serializeTransportMethod(transport.method)
        assert result['secret'] == transport.requireSecret()

    @pytest.mark.asyncio
    async def test_serializeTransport_withWebsocketTransportMethod(self):
        transport = TwitchWebsocketTransport(
            connectedAt = None,
            disconnectedAt = None,
            callbackUrl = None,
            conduitId = None,
            secret = None,
            sessionId = 'xyz789',
            method = TwitchWebsocketTransportMethod.WEBSOCKET,
        )

        result = await self.jsonMapper.serializeTransport(transport)
        assert isinstance(result, dict)
        assert len(result) == 2

        assert result['method'] == await self.jsonMapper.serializeTransportMethod(transport.method)
        assert result['session_id'] == transport.requireSessionId()

    @pytest.mark.asyncio
    async def test_serializeTransportMethod_withAll(self):
        results: set[str] = set()

        for transportMethod in TwitchWebsocketTransportMethod:
            results.add(await self.jsonMapper.serializeTransportMethod(transportMethod))

        assert len(results) == len(TwitchWebsocketTransportMethod)

    @pytest.mark.asyncio
    async def test_serializeTransportMethod_withConduit(self):
        string = await self.jsonMapper.serializeTransportMethod(TwitchWebsocketTransportMethod.CONDUIT)
        assert string == 'conduit'

    @pytest.mark.asyncio
    async def test_serializeTransportMethod_withWebhook(self):
        string = await self.jsonMapper.serializeTransportMethod(TwitchWebsocketTransportMethod.WEBHOOK)
        assert string == 'webhook'

    @pytest.mark.asyncio
    async def test_serializeTransportMethod_withWebsocket(self):
        string = await self.jsonMapper.serializeTransportMethod(TwitchWebsocketTransportMethod.WEBSOCKET)
        assert string == 'websocket'
