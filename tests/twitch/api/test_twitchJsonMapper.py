from datetime import datetime, timedelta
from typing import Any

import pytest

from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.twitch.api.twitchApiScope import TwitchApiScope
from src.twitch.api.twitchBanRequest import TwitchBanRequest
from src.twitch.api.twitchBroadcasterType import TwitchBroadcasterType
from src.twitch.api.twitchChannelEditor import TwitchChannelEditor
from src.twitch.api.twitchChannelEditorsResponse import TwitchChannelEditorsResponse
from src.twitch.api.twitchEmoteImageFormat import TwitchEmoteImageFormat
from src.twitch.api.twitchEmoteImageScale import TwitchEmoteImageScale
from src.twitch.api.twitchEmoteType import TwitchEmoteType
from src.twitch.api.twitchEventSubRequest import TwitchEventSubRequest
from src.twitch.api.twitchJsonMapper import TwitchJsonMapper
from src.twitch.api.twitchJsonMapperInterface import TwitchJsonMapperInterface
from src.twitch.api.twitchOutcomeColor import TwitchOutcomeColor
from src.twitch.api.twitchPaginationResponse import TwitchPaginationResponse
from src.twitch.api.twitchPollStatus import TwitchPollStatus
from src.twitch.api.twitchPredictionStatus import TwitchPredictionStatus
from src.twitch.api.twitchRewardRedemptionStatus import TwitchRewardRedemptionStatus
from src.twitch.api.twitchSendChatMessageRequest import TwitchSendChatMessageRequest
from src.twitch.api.twitchStreamType import TwitchStreamType
from src.twitch.api.twitchSubscriberTier import TwitchSubscriberTier
from src.twitch.api.twitchUserType import TwitchUserType
from src.twitch.api.websocket.twitchWebsocketCondition import TwitchWebsocketCondition
from src.twitch.api.websocket.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from src.twitch.api.websocket.twitchWebsocketTransport import TwitchWebsocketTransport
from src.twitch.api.websocket.twitchWebsocketTransportMethod import TwitchWebsocketTransportMethod


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
    async def test_parseApiScope_withChannelEditorString(self):
        result = await self.jsonMapper.parseApiScope('channel_editor')
        assert result is TwitchApiScope.CHANNEL_EDITOR

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
    async def test_parseApiScope_withChannelReadEditorsString(self):
        result = await self.jsonMapper.parseApiScope('channel:read:editors')
        assert result is TwitchApiScope.CHANNEL_READ_EDITORS

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
        assert editor == qbit
        assert editor.createdAt == qbit.createdAt
        assert editor.userId == qbit.userId
        assert editor.userName == qbit.userName

        editor = result.editors[1]
        assert isinstance(editor, TwitchChannelEditor)
        assert editor == tsteine
        assert editor.createdAt == tsteine.createdAt
        assert editor.userId == tsteine.userId
        assert editor.userName == tsteine.userName

    @pytest.mark.asyncio
    async def test_parseChannelEditorsResponse_withEmptyDictionary(self):
        result = await self.jsonMapper.parseChannelEditorsResponse(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseChannelEditorsResponse_withNone(self):
        result = await self.jsonMapper.parseChannelEditorsResponse(None)
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
        jsonResponse: dict[str, Any] = {
            'cursor': 'abc123'
        }

        result = await self.jsonMapper.parsePaginationResponse(jsonResponse)
        assert isinstance(result, TwitchPaginationResponse)
        assert result.cursor == 'abc123'

    @pytest.mark.asyncio
    async def test_parsePaginationResponse_withEmptyDictionary(self):
        result = await self.jsonMapper.parsePaginationResponse(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parsePaginationResponse_withNone(self):
        result = await self.jsonMapper.parsePaginationResponse(None)
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
    async def test_serializeEventSubRequest1(self):
        condition = TwitchWebsocketCondition(
            broadcasterUserId = 'abc123'
        )

        subscriptionType = TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION

        transport = TwitchWebsocketTransport(
            method = TwitchWebsocketTransportMethod.WEBSOCKET,
            sessionId = 'qwerty'
        )

        request = TwitchEventSubRequest(
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
        assert dictionary['transport']['method'] == transport.method.toStr()
        assert 'session_id' in dictionary['transport']
        assert dictionary['transport']['session_id'] == transport.sessionId

        assert 'type' in dictionary
        assert dictionary['type'] == subscriptionType.toStr()

        assert 'version' in dictionary
        assert dictionary['version'] == subscriptionType.getVersion()

    @pytest.mark.asyncio
    async def test_serializeEventSubRequest2(self):
        condition = TwitchWebsocketCondition(
            broadcasterUserId = 'def987'
        )

        subscriptionType = TwitchWebsocketSubscriptionType.SUBSCRIBE

        transport = TwitchWebsocketTransport(
            method = TwitchWebsocketTransportMethod.WEBSOCKET,
            sessionId = 'azerty'
        )

        request = TwitchEventSubRequest(
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
        assert dictionary['transport']['method'] == transport.method.toStr()
        assert 'session_id' in dictionary['transport']
        assert dictionary['transport']['session_id'] == transport.sessionId

        assert 'type' in dictionary
        assert dictionary['type'] == subscriptionType.toStr()

        assert 'version' in dictionary
        assert dictionary['version'] == subscriptionType.getVersion()

    @pytest.mark.asyncio
    async def test_serializeEventSubRequest3(self):
        condition = TwitchWebsocketCondition(
            broadcasterUserId = 'foo',
            moderatorUserId = 'bar'
        )

        subscriptionType = TwitchWebsocketSubscriptionType.SUBSCRIBE

        transport = TwitchWebsocketTransport(
            method = TwitchWebsocketTransportMethod.WEBSOCKET,
            sessionId = 'azerty'
        )

        request = TwitchEventSubRequest(
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
        assert dictionary['transport']['method'] == transport.method.toStr()
        assert 'session_id' in dictionary['transport']
        assert dictionary['transport']['session_id'] == transport.sessionId

        assert 'type' in dictionary
        assert dictionary['type'] == subscriptionType.toStr()

        assert 'version' in dictionary
        assert dictionary['version'] == subscriptionType.getVersion()

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
