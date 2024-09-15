from typing import Any

import pytest

from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.ttsMonster.mapper.ttsMonsterJsonMapper import TtsMonsterJsonMapper
from src.ttsMonster.mapper.ttsMonsterJsonMapperInterface import TtsMonsterJsonMapperInterface
from src.ttsMonster.mapper.ttsMonsterWebsiteVoiceMapper import TtsMonsterWebsiteVoiceMapper
from src.ttsMonster.mapper.ttsMonsterWebsiteVoiceMapperInterface import TtsMonsterWebsiteVoiceMapperInterface
from src.ttsMonster.models.ttsMonsterTtsRequest import TtsMonsterTtsRequest
from src.ttsMonster.models.ttsMonsterTtsResponse import TtsMonsterTtsResponse


class TestTtsMonsterJsonMapper:

    timber: TimberInterface = TimberStub()

    websiteVoiceMapper: TtsMonsterWebsiteVoiceMapperInterface = TtsMonsterWebsiteVoiceMapper()

    mapper: TtsMonsterJsonMapperInterface = TtsMonsterJsonMapper(
        timber = timber,
        websiteVoiceMapper = websiteVoiceMapper
    )

    @pytest.mark.asyncio
    async def test_parseTtsResponse_withCharacterUsage(self):
        characterUsage = 512
        status = 200
        url = 'https://storage.tts.monster/tts/12345678981.wav'

        jsonContents: dict[str, Any] = {
            'characterUsage': characterUsage,
            'status': status,
            'url': url
        }

        result = await self.mapper.parseTtsResponse(jsonContents)
        assert isinstance(result, TtsMonsterTtsResponse)
        assert result.characterUsage == characterUsage
        assert result.status == status
        assert result.url == url

    @pytest.mark.asyncio
    async def test_parseTtsResponse_withoutCharacterUsage(self):
        status = 200
        url = 'https://storage.tts.monster/tts/12345678981.wav'

        jsonContents: dict[str, Any] = {
            'status': status,
            'url': url
        }

        result = await self.mapper.parseTtsResponse(jsonContents)
        assert isinstance(result, TtsMonsterTtsResponse)
        assert result.characterUsage is None
        assert result.status == status
        assert result.url == url

    @pytest.mark.asyncio
    async def test_parseTtsResponse_withEmptyDictionary(self):
        result = await self.mapper.parseTtsResponse(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTtsResponse_withNone(self):
        result = await self.mapper.parseTtsResponse(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseUser_withEmptyDictionary(self):
        result = await self.mapper.parseUser(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseUser_withNone(self):
        result = await self.mapper.parseUser(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoice_withEmptyDictionary(self):
        result = await self.mapper.parseVoice(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoice_withNone(self):
        result = await self.mapper.parseVoice(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoicesResponse_withEmptyDictionary(self):
        result = await self.mapper.parseVoicesResponse(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoicesResponse_withNone(self):
        result = await self.mapper.parseVoicesResponse(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_serializeTtsRequest_withReturnUsage(self):
        request = TtsMonsterTtsRequest(
            returnUsage = True,
            message = 'Hello, World!',
            voiceId = 'xyz123'
        )

        result = await self.mapper.serializeTtsRequest(request)
        assert isinstance(result, dict)
        assert len(result) == 3

        assert result['message'] == request.message
        assert result['return_usage'] == request.returnUsage
        assert result['voice_id'] == request.voiceId

    @pytest.mark.asyncio
    async def test_serializeTtsRequest_withoutReturnUsage(self):
        request = TtsMonsterTtsRequest(
            returnUsage = False,
            message = 'Hello, World!',
            voiceId = 'abc123'
        )

        result = await self.mapper.serializeTtsRequest(request)
        assert isinstance(result, dict)
        assert len(result) == 2

        assert result['message'] == request.message
        assert result['voice_id'] == request.voiceId
