from typing import Any

import pytest

from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.ttsMonster.mapper.ttsMonsterPrivateApiJsonMapper import TtsMonsterPrivateApiJsonMapper
from src.ttsMonster.mapper.ttsMonsterPrivateApiJsonMapperInterface import TtsMonsterPrivateApiJsonMapperInterface
from src.ttsMonster.models.ttsMonsterPrivateApiTtsData import TtsMonsterPrivateApiTtsData
from src.ttsMonster.models.ttsMonsterPrivateApiTtsResponse import TtsMonsterPrivateApiTtsResponse
from src.ttsMonster.models.ttsMonsterVoice import TtsMonsterVoice


class TestTtsMonsterPrivateApiJsonMapper:

    timber: TimberInterface = TimberStub()

    mapper: TtsMonsterPrivateApiJsonMapperInterface = TtsMonsterPrivateApiJsonMapper(
        timber = timber
    )

    @pytest.mark.asyncio
    async def test_parseTtsData(self):
        link = 'https://www.google.com/'
        warning = 'This is a warning message!'

        result = await self.mapper.parseTtsData({
            'link': link,
            'warning': warning
        })

        assert isinstance(result, TtsMonsterPrivateApiTtsData)
        assert result.link == link
        assert result.warning == warning

    @pytest.mark.asyncio
    async def test_parseTtsData_withEmptyDictionary(self):
        result = await self.mapper.parseTtsData(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTtsData_withNone(self):
        result = await self.mapper.parseTtsData(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTtsData_withoutLink(self):
        link: str | None = None
        warning = 'This is a warning message!'

        result = await self.mapper.parseTtsData({
            'link': link,
            'warning': warning
        })

        assert result is None

    @pytest.mark.asyncio
    async def test_parseTtsResponse(self):
        status = 200
        google = 'https://www.google.com/'
        warning: str | None = None

        dictionary: dict[str, Any] = {
            'status': status,
            'data': {
                'link': google,
                'warning': warning
            }
        }

        result = await self.mapper.parseTtsResponse(dictionary)
        assert isinstance(result, TtsMonsterPrivateApiTtsResponse)

        assert result.status == status
        assert result.data.link == google
        assert result.data.warning == warning

    @pytest.mark.asyncio
    async def test_parseTtsResponse_withEmptyDictionary(self):
        result = await self.mapper.parseTtsResponse(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTtsResponse_withNone(self):
        result = await self.mapper.parseTtsResponse(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTtsResponse_withStatusButNoData(self):
        status = 200

        result = await self.mapper.parseTtsResponse({
            'status': status
        })

        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoice_withBrian(self):
        result = await self.mapper.parseVoice('brian')
        assert result is TtsMonsterVoice.BRIAN

    @pytest.mark.asyncio
    async def test_parseVoice_withJazz(self):
        result = await self.mapper.parseVoice('jazz')
        assert result is TtsMonsterVoice.JAZZ

    @pytest.mark.asyncio
    async def test_parseVoice_withKkona(self):
        result = await self.mapper.parseVoice('kkona')
        assert result is TtsMonsterVoice.KKONA

    @pytest.mark.asyncio
    async def test_parseVoice_withPirate(self):
        result = await self.mapper.parseVoice('pirate')
        assert result is TtsMonsterVoice.PIRATE

    @pytest.mark.asyncio
    async def test_parseVoice_withShadow(self):
        result = await self.mapper.parseVoice('shadow')
        assert result is TtsMonsterVoice.SHADOW

    @pytest.mark.asyncio
    async def test_parseVoice_withWitch(self):
        result = await self.mapper.parseVoice('witch')
        assert result is TtsMonsterVoice.WITCH

    @pytest.mark.asyncio
    async def test_parseVoice_withZeroTwo(self):
        result = await self.mapper.parseVoice('zero_two')
        assert result is TtsMonsterVoice.ZERO_TWO

    def test_sanity(self):
        assert self.mapper is not None
        assert isinstance(self.mapper, TtsMonsterPrivateApiJsonMapper)
        assert isinstance(self.mapper, TtsMonsterPrivateApiJsonMapperInterface)

    @pytest.mark.asyncio
    async def test_serializeGenerateTtsJsonBody(self):
        key = 'key'
        message = 'Hello, World!'
        userId = 'smCharles'

        jsonBody = await self.mapper.serializeGenerateTtsJsonBody(
            key = key,
            message = message,
            userId = userId
        )

        assert isinstance(jsonBody, dict)
        assert len(jsonBody) == 1

        dataJson: dict[str, Any] | Any | None = jsonBody.get('data', None)
        assert isinstance(dataJson, dict)
        assert len(dataJson) == 5

        assert dataJson['ai'] == True
        assert dataJson['key'] == key
        assert dataJson['message'] == message
        assert dataJson['userId'] == userId

        detailsJson: dict[str, Any] | Any | None = dataJson.get('details', None)
        assert isinstance(detailsJson, dict)
        assert len(detailsJson) == 1

        assert detailsJson['provider'] == 'provider'

    @pytest.mark.asyncio
    async def test_serializeVoice_withBrian(self):
        result = await self.mapper.serializeVoice(TtsMonsterVoice.BRIAN)
        assert result == 'brian'

    @pytest.mark.asyncio
    async def test_serializeVoice_withJazz(self):
        result = await self.mapper.serializeVoice(TtsMonsterVoice.JAZZ)
        assert result == 'jazz'

    @pytest.mark.asyncio
    async def test_serializeVoice_withKkona(self):
        result = await self.mapper.serializeVoice(TtsMonsterVoice.KKONA)
        assert result == 'kkona'

    @pytest.mark.asyncio
    async def test_serializeVoice_withPirate(self):
        result = await self.mapper.serializeVoice(TtsMonsterVoice.PIRATE)
        assert result == 'pirate'

    @pytest.mark.asyncio
    async def test_serializeVoice_withShadow(self):
        result = await self.mapper.serializeVoice(TtsMonsterVoice.SHADOW)
        assert result == 'shadow'

    @pytest.mark.asyncio
    async def test_serializeVoice_withWitch(self):
        result = await self.mapper.serializeVoice(TtsMonsterVoice.WITCH)
        assert result == 'witch'

    @pytest.mark.asyncio
    async def test_serializeVoice_withZeroTwo(self):
        result = await self.mapper.serializeVoice(TtsMonsterVoice.ZERO_TWO)
        assert result == 'zero_two'
