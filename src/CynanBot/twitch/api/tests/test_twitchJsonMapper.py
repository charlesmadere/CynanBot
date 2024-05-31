import pytest

from CynanBot.location.timeZoneRepository import TimeZoneRepository
from CynanBot.location.timeZoneRepositoryInterface import \
    TimeZoneRepositoryInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.timber.timberStub import TimberStub
from CynanBot.twitch.api.twitchApiScope import TwitchApiScope
from CynanBot.twitch.api.twitchJsonMapper import TwitchJsonMapper
from CynanBot.twitch.api.twitchJsonMapperInterface import \
    TwitchJsonMapperInterface
from CynanBot.twitch.api.twitchSubscriberTier import TwitchSubscriberTier


class TestTwitchJsonMapper():

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
