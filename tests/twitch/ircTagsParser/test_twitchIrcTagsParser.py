from typing import Any

import pytest
from frozendict import frozendict

from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.twitch.ircTagsParser.exceptions import TwitchIrcTagsAreMalformedException, \
    TwitchIrcTagsAreMissingDisplayNameException, \
    TwitchIrcTagsAreMissingMessageIdException, \
    TwitchIrcTagsAreMissingRoomIdException, \
    TwitchIrcTagsAreMissingUserIdException
from src.twitch.ircTagsParser.twitchIrcTags import TwitchIrcTags
from src.twitch.ircTagsParser.twitchIrcTagsParser import TwitchIrcTagsParser
from src.twitch.ircTagsParser.twitchIrcTagsParserInterface import TwitchIrcTagsParserInterface


class TestTwitchIrcTagsParser:

    timber: TimberInterface = TimberStub()

    parser: TwitchIrcTagsParserInterface = TwitchIrcTagsParser(
        timber = timber
    )

    @pytest.mark.asyncio
    async def test_parseSubscriberTier_withEmptyString(self):
        result = await self.parser.parseSubscriberTier('')
        assert result is TwitchIrcTags.SubscriberTier.NONE

    @pytest.mark.asyncio
    async def test_parseSubscriberTier_withNone(self):
        result = await self.parser.parseSubscriberTier(None)
        assert result is TwitchIrcTags.SubscriberTier.NONE

    @pytest.mark.asyncio
    async def test_parseSubscriberTier_withStreamerString(self):
        result = await self.parser.parseSubscriberTier('broadcaster/1,subscriber/3054,partner/1')
        assert result is TwitchIrcTags.SubscriberTier.TIER_3

    @pytest.mark.asyncio
    async def test_parseSubscriberTier_withTier2String(self):
        result = await self.parser.parseSubscriberTier('moderator/1,subscriber/2036')
        assert result is TwitchIrcTags.SubscriberTier.TIER_2

    @pytest.mark.asyncio
    async def test_parseSubscriberTier_withTier3String(self):
        result = await self.parser.parseSubscriberTier('moderator/1,subscriber/3030')
        assert result is TwitchIrcTags.SubscriberTier.TIER_3

    @pytest.mark.asyncio
    async def test_parseTwitchIrcTags(self):
        displayName = 'stashiocat'
        messageId = '654321'
        twitchChannelId = '1234567890'
        userId = '9876543210'

        rawIrcTags: dict[Any, Any] = {
            '@badge-info': 'subscriber/10',
            'badges': 'vip/1,subscriber/1009,turbo/1',
            'client-nonce': 'abc123',
            'color': '#FF69B4',
            'display-name': displayName,
            'emotes': '',
            'first-msg': '0',
            'flags': '',
            'id': messageId,
            'mod': '0',
            'returning-chatter': '0',
            'room-id': twitchChannelId,
            'subscriber': '1',
            'tmi-sent-ts': '',
            'turbo': '1',
            'user-id': userId,
            'user-type': '',
            'vip': '1'
        }

        result = await self.parser.parseTwitchIrcTags(rawIrcTags)
        assert result.displayName == displayName
        assert result.messageId == messageId
        assert result.rawTags == frozendict(rawIrcTags)
        assert result.subscriberTier is TwitchIrcTags.SubscriberTier.TIER_1
        assert result.twitchChannelId == twitchChannelId
        assert result.userId == userId

    @pytest.mark.asyncio
    async def test_parseTwitchIrcTags_withEmptyDictionary(self):
        result: TwitchIrcTags | None = None

        with pytest.raises(TwitchIrcTagsAreMalformedException):
            result = await self.parser.parseTwitchIrcTags(dict())

        assert result is None

    @pytest.mark.asyncio
    async def test_parseTwitchIrcTags_withMissingDisplayName(self):
        messageId = '654321'
        twitchChannelId = '1234567890'
        userId = '9876543210'

        rawIrcTags: dict[Any, Any] = {
            '@badge-info': 'subscriber/10',
            'badges': 'vip/1,subscriber/3009,turbo/1',
            'client-nonce': 'abc123',
            'color': '#FF69B4',
            'emotes': '',
            'first-msg': '0',
            'flags': '',
            'id': messageId,
            'mod': '0',
            'returning-chatter': '0',
            'room-id': twitchChannelId,
            'subscriber': '1',
            'tmi-sent-ts': '',
            'turbo': '1',
            'user-id': userId,
            'user-type': '',
            'vip': '1'
        }

        result: TwitchIrcTags | None = None

        with pytest.raises(TwitchIrcTagsAreMissingDisplayNameException):
            result = await self.parser.parseTwitchIrcTags(rawIrcTags)

        assert result is None

    @pytest.mark.asyncio
    async def test_parseTwitchIrcTags_withMissingMessageId(self):
        displayName = 'stashiocat'
        twitchChannelId = '1234567890'
        userId = '9876543210'

        rawIrcTags: dict[Any, Any] = {
            '@badge-info': 'subscriber/10',
            'badges': 'vip/1,subscriber/3009,turbo/1',
            'client-nonce': 'abc123',
            'color': '#FF69B4',
            'display-name': displayName,
            'emotes': '',
            'first-msg': '0',
            'flags': '',
            'mod': '0',
            'returning-chatter': '0',
            'room-id': twitchChannelId,
            'subscriber': '1',
            'tmi-sent-ts': '',
            'turbo': '1',
            'user-id': userId,
            'user-type': '',
            'vip': '1'
        }

        result: TwitchIrcTags | None = None

        with pytest.raises(TwitchIrcTagsAreMissingMessageIdException):
            result = await self.parser.parseTwitchIrcTags(rawIrcTags)

        assert result is None

    @pytest.mark.asyncio
    async def test_parseTwitchIrcTags_withMissingRoomId(self):
        displayName = 'stashiocat'
        messageId = '654321'
        userId = '9876543210'

        rawIrcTags: dict[Any, Any] = {
            '@badge-info': 'subscriber/10',
            'badges': 'vip/1,subscriber/3009,turbo/1',
            'client-nonce': 'abc123',
            'color': '#FF69B4',
            'display-name': displayName,
            'emotes': '',
            'first-msg': '0',
            'flags': '',
            'id': messageId,
            'mod': '0',
            'returning-chatter': '0',
            'subscriber': '1',
            'tmi-sent-ts': '',
            'turbo': '1',
            'user-id': userId,
            'user-type': '',
            'vip': '1'
        }

        result: TwitchIrcTags | None = None

        with pytest.raises(TwitchIrcTagsAreMissingRoomIdException):
            result = await self.parser.parseTwitchIrcTags(rawIrcTags)

        assert result is None

    @pytest.mark.asyncio
    async def test_parseTwitchIrcTags_withMissingUserId(self):
        displayName = 'stashiocat'
        messageId = '654321'
        twitchChannelId = '1234567890'

        rawIrcTags: dict[Any, Any] = {
            '@badge-info': 'subscriber/10',
            'badges': 'vip/1,subscriber/3009,turbo/1',
            'client-nonce': 'abc123',
            'color': '#FF69B4',
            'display-name': displayName,
            'emotes': '',
            'first-msg': '0',
            'flags': '',
            'id': messageId,
            'mod': '0',
            'returning-chatter': '0',
            'room-id': twitchChannelId,
            'subscriber': '1',
            'tmi-sent-ts': '',
            'turbo': '1',
            'user-type': '',
            'vip': '1'
        }

        result: TwitchIrcTags | None = None

        with pytest.raises(TwitchIrcTagsAreMissingUserIdException):
            result = await self.parser.parseTwitchIrcTags(rawIrcTags)

        assert result is None

    @pytest.mark.asyncio
    async def test_parseTwitchIrcTags_withNone(self):
        result: TwitchIrcTags | None = None

        with pytest.raises(TwitchIrcTagsAreMalformedException):
            result = await self.parser.parseTwitchIrcTags(None)

        assert result is None

    def test_sanity(self):
        assert self.parser is not None
        assert isinstance(self.parser, TwitchIrcTagsParser)
        assert isinstance(self.parser, TwitchIrcTagsParserInterface)
