import json
from typing import Final

import pytest

from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.twitch.api.jsonMapper.twitchJsonMapper import TwitchJsonMapper
from src.twitch.api.jsonMapper.twitchJsonMapperInterface import TwitchJsonMapperInterface
from src.twitch.websocket.twitchWebsocketJsonLoggingLevel import TwitchWebsocketJsonLoggingLevel
from src.twitch.websocket.twitchWebsocketJsonMapper import TwitchWebsocketJsonMapper
from src.twitch.websocket.twitchWebsocketJsonMapperInterface import TwitchWebsocketJsonMapperInterface


class TestTwitchWebsocketJsonMapper:

    timber: Final[TimberInterface] = TimberStub()

    timeZoneRepository: Final[TimeZoneRepositoryInterface] = TimeZoneRepository()

    jsonMapper: Final[TwitchJsonMapperInterface] = TwitchJsonMapper(
        timber = timber,
        timeZoneRepository = timeZoneRepository,
    )

    websocketJsonMapper: Final[TwitchWebsocketJsonMapperInterface] = TwitchWebsocketJsonMapper(
        timber = timber,
        twitchJsonMapper = jsonMapper,
    )

    @pytest.mark.asyncio
    async def test_parseLoggingLevel_withAllString(self):
        result = await self.websocketJsonMapper.parseLoggingLevel('all')
        assert result is TwitchWebsocketJsonLoggingLevel.ALL

    @pytest.mark.asyncio
    async def test_parseLoggingLevel_withLimitedString(self):
        result = await self.websocketJsonMapper.parseLoggingLevel('limited')
        assert result is TwitchWebsocketJsonLoggingLevel.LIMITED

    @pytest.mark.asyncio
    async def test_parseLoggingLevel_withNoneString(self):
        result = await self.websocketJsonMapper.parseLoggingLevel('none')
        assert result is TwitchWebsocketJsonLoggingLevel.NONE

    @pytest.mark.asyncio
    async def test_parseWebsocketDataBundle_withEmptyDictionary(self):
        result = await self.websocketJsonMapper.parseWebsocketDataBundle(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketDataBundle_withNone(self):
        result = await self.websocketJsonMapper.parseWebsocketDataBundle(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketDataBundle_withKazekiiMessage(self):
        dataBundleJson = json.loads('{"metadata":{"message_id":"nuiX1bDhmBpjVldi7rcQr0AA-HbONk1BEbe4rl6TjTo=","message_type":"notification","message_timestamp":"2026-04-24T05:56:01.402225886Z","subscription_type":"channel.chat.notification","subscription_version":"1"},"payload":{"subscription":{"id":"91e92830-2c67-4de5-9f15-b03d0277d148","status":"enabled","type":"channel.chat.notification","version":"1","condition":{"broadcaster_user_id":"62963382","user_id":"62963382"},"transport":{"method":"websocket","session_id":"AgoQdsb6IWR3SpCK47fUqOnQ0RIGY2VsbC1h"},"created_at":"2026-04-24T04:48:49.311928996Z","cost":0},"event":{"broadcaster_user_id":"62963382","broadcaster_user_login":"kazekii","broadcaster_user_name":"Kazekii","source_broadcaster_user_id":null,"source_broadcaster_user_login":null,"source_broadcaster_user_name":null,"chatter_user_id":"183348638","chatter_user_login":"otterpopito","chatter_user_name":"OtterPopito","chatter_is_anonymous":false,"color":"#FF69B4","badges":[{"set_id":"subscriber","id":"3","info":"3"},{"set_id":"final-fantasy-xiv-fan-festival-2026-na---fat-cat-chat","id":"1","info":""}],"source_badges":null,"system_message":"OtterPopito subscribed with Prime. They\'ve subscribed for 3 months!","message_id":"02caac43-58f7-4023-9110-12aafb174d3c","source_message_id":null,"is_source_only":null,"message":{"text":"I got the fat fuck badge kazeki4Point","fragments":[{"type":"text","text":"I got the fat fuck badge ","cheermote":null,"emote":null,"mention":null},{"type":"emote","text":"kazeki4Point","cheermote":null,"emote":{"id":"emotesv2_f6dd28aae7ce44cfadd5faf499ba40f9","emote_set_id":"456291166","owner_id":"62963382","format":["static"]},"mention":null}]},"notice_type":"resub","sub":null,"resub":{"cumulative_months":3,"duration_months":1,"streak_months":null,"sub_tier":"1000","is_prime":true,"is_gift":false,"gifter_is_anonymous":null,"gifter_user_id":null,"gifter_user_name":null,"gifter_user_login":null},"sub_gift":null,"community_sub_gift":null,"gift_paid_upgrade":null,"prime_paid_upgrade":null,"pay_it_forward":null,"raid":null,"unraid":null,"announcement":null,"bits_badge_tier":null,"charity_donation":null,"watch_streak":null,"shared_chat_sub":null,"shared_chat_resub":null,"shared_chat_sub_gift":null,"shared_chat_community_sub_gift":null,"shared_chat_gift_paid_upgrade":null,"shared_chat_prime_paid_upgrade":null,"shared_chat_pay_it_forward":null,"shared_chat_raid":null,"shared_chat_announcement":null}}}')
        result = await self.websocketJsonMapper.parseWebsocketDataBundle(dataBundleJson)
        assert result is not None

    @pytest.mark.asyncio
    async def test_parseWebsocketEvent_withEmptyDictionary(self):
        result = await self.websocketJsonMapper.parseWebsocketEvent(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketEvent_withNone(self):
        result = await self.websocketJsonMapper.parseWebsocketEvent(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketPayload_withEmptyDictionary(self):
        result = await self.websocketJsonMapper.parseWebsocketPayload(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketPayload_withNone(self):
        result = await self.websocketJsonMapper.parseWebsocketPayload(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketSession_withEmptyDictionary(self):
        result = await self.websocketJsonMapper.parseWebsocketSession(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketSession_withNone(self):
        result = await self.websocketJsonMapper.parseWebsocketSession(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketSubscription_withEmptyDictionary(self):
        result = await self.websocketJsonMapper.parseWebsocketSubscription(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketSubscription_withNone(self):
        result = await self.websocketJsonMapper.parseWebsocketSubscription(None)
        assert result is None

    def test_sanity(self):
        assert self.websocketJsonMapper is not None
        assert isinstance(self.websocketJsonMapper, TwitchWebsocketJsonMapper)
        assert isinstance(self.websocketJsonMapper, TwitchWebsocketJsonMapperInterface)

    @pytest.mark.asyncio
    async def test_serializeLoggingLevel(self):
        results: set[str] = set()

        for loggingLevel in TwitchWebsocketJsonLoggingLevel:
            results.add(await self.websocketJsonMapper.serializeLoggingLevel(loggingLevel))

        assert len(results) == len(TwitchWebsocketJsonLoggingLevel)

    @pytest.mark.asyncio
    async def test_serializeLoggingLevel_withAll(self):
        result = await self.websocketJsonMapper.serializeLoggingLevel(TwitchWebsocketJsonLoggingLevel.ALL)
        assert result == 'all'

    @pytest.mark.asyncio
    async def test_serializeLoggingLevel_withLimited(self):
        result = await self.websocketJsonMapper.serializeLoggingLevel(TwitchWebsocketJsonLoggingLevel.LIMITED)
        assert result == 'limited'

    @pytest.mark.asyncio
    async def test_serializeLoggingLevel_withNone(self):
        result = await self.websocketJsonMapper.serializeLoggingLevel(TwitchWebsocketJsonLoggingLevel.NONE)
        assert result == 'none'
