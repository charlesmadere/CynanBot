import pytest

from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.tts.ttsJsonMapper import TtsJsonMapper
from src.tts.ttsJsonMapperInterface import TtsJsonMapperInterface
from src.tts.ttsProvider import TtsProvider


class TestTtsJsonMapper:

    timber: TimberInterface = TimberStub()

    jsonMapper: TtsJsonMapperInterface = TtsJsonMapper(
        timber = timber
    )

    @pytest.mark.asyncio
    async def test_parseProvider_withDecTalkString(self):
        result = await self.jsonMapper.parseProvider('dec_talk')
        assert result is TtsProvider.DEC_TALK

    @pytest.mark.asyncio
    async def test_parseProvider_withEmptyString(self):
        result = await self.jsonMapper.parseProvider('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseProvider_withGoogleString(self):
        result = await self.jsonMapper.parseProvider('google')
        assert result is TtsProvider.GOOGLE

    @pytest.mark.asyncio
    async def test_parseProvider_withNone(self):
        result = await self.jsonMapper.parseProvider(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseProvider_withStreamElementsString(self):
        result = await self.jsonMapper.parseProvider('stream_elements')
        assert result is TtsProvider.STREAM_ELEMENTS

    @pytest.mark.asyncio
    async def test_parseProvider_withTtsMonsterString(self):
        result = await self.jsonMapper.parseProvider('tts_monster')
        assert result is TtsProvider.TTS_MONSTER

    @pytest.mark.asyncio
    async def test_parseProvider_withWhitespaceString(self):
        result = await self.jsonMapper.parseProvider(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_requireProvider_withDecTalkString(self):
        result = await self.jsonMapper.requireProvider('dec_talk')
        assert result is TtsProvider.DEC_TALK

    @pytest.mark.asyncio
    async def test_requireProvider_withEmptyString(self):
        result: TtsProvider | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.requireProvider('')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireProvider_withGoogleString(self):
        result = await self.jsonMapper.requireProvider('google')
        assert result is TtsProvider.GOOGLE

    @pytest.mark.asyncio
    async def test_requireProvider_withNone(self):
        result: TtsProvider | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.requireProvider(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireProvider_withTtsMonsterString(self):
        result = await self.jsonMapper.requireProvider('tts_monster')
        assert result is TtsProvider.TTS_MONSTER

    @pytest.mark.asyncio
    async def test_requireProvider_withWhitespaceString(self):
        result: TtsProvider | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.requireProvider(' ')

        assert result is None

    @pytest.mark.asyncio
    async def test_serializeProvider_withDecTalk(self):
        result = await self.jsonMapper.serializeProvider(TtsProvider.DEC_TALK)
        assert result == 'dec_talk'

    @pytest.mark.asyncio
    async def test_serializeProvider_withGoogle(self):
        result = await self.jsonMapper.serializeProvider(TtsProvider.GOOGLE)
        assert result == 'google'

    @pytest.mark.asyncio
    async def test_serializeProvider_withStreamElements(self):
        result = await self.jsonMapper.serializeProvider(TtsProvider.STREAM_ELEMENTS)
        assert result == 'stream_elements'

    @pytest.mark.asyncio
    async def test_serializeProvider_withTtsMonster(self):
        result = await self.jsonMapper.serializeProvider(TtsProvider.TTS_MONSTER)
        assert result == 'tts_monster'
