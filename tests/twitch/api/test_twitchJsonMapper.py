from typing import Any

import pytest

from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.twitch.api.twitchApiScope import TwitchApiScope
from src.twitch.api.twitchBanRequest import TwitchBanRequest
from src.twitch.api.twitchBroadcasterType import TwitchBroadcasterType
from src.twitch.api.twitchEmoteImageFormat import TwitchEmoteImageFormat
from src.twitch.api.twitchEmoteImageScale import TwitchEmoteImageScale
from src.twitch.api.twitchEmoteType import TwitchEmoteType
from src.twitch.api.twitchJsonMapper import TwitchJsonMapper
from src.twitch.api.twitchJsonMapperInterface import TwitchJsonMapperInterface
from src.twitch.api.twitchOutcomeColor import TwitchOutcomeColor
from src.twitch.api.twitchPaginationResponse import TwitchPaginationResponse
from src.twitch.api.twitchPollStatus import TwitchPollStatus
from src.twitch.api.twitchSendChatMessageRequest import TwitchSendChatMessageRequest
from src.twitch.api.twitchSubscriberTier import TwitchSubscriberTier
from src.twitch.api.twitchUserType import TwitchUserType


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
