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
    async def test_asyncParseProvider_withDecTalkString(self):
        result = await self.jsonMapper.asyncParseProvider('dec_talk')
        assert result is TtsProvider.DEC_TALK

    @pytest.mark.asyncio
    async def test_asyncParseProvider_withEmptyString(self):
        result = await self.jsonMapper.asyncParseProvider('')
        assert result is None

    @pytest.mark.asyncio
    async def test_asyncSerializeProvider_withDecTalk(self):
        result = await self.jsonMapper.asyncParseProvider(TtsProvider.DEC_TALK)
        assert result == 'dec_talk'

    async def test_parseProvider_withDecTalkString(self):
        result = self.jsonMapper.parseProvider('dec_talk')
        assert result is TtsProvider.DEC_TALK

    async def test_parseProvider_withEmptyString(self):
        result = self.jsonMapper.parseProvider('')
        assert result is None

    async def test_parseProvider_withGoogleString(self):
        result = self.jsonMapper.parseProvider('google')
        assert result is TtsProvider.GOOGLE

    async def test_parseProvider_withNone(self):
        result = self.jsonMapper.parseProvider(None)
        assert result is None

    async def test_parseProvider_withStreamElementsString(self):
        result = self.jsonMapper.parseProvider('stream_elements')
        assert result is TtsProvider.STREAM_ELEMENTS

    async def test_parseProvider_withTtsMonsterString(self):
        result = self.jsonMapper.parseProvider('ttsmonster')
        assert result is TtsProvider.TTS_MONSTER

    async def test_parseProvider_withWhitespaceString(self):
        result = self.jsonMapper.parseProvider(' ')
        assert result is None

    async def test_requireProvider_withDecTalkString(self):
        result = self.jsonMapper.requireProvider('dec_talk')
        assert result is TtsProvider.DEC_TALK

    async def test_requireProvider_withEmptyString(self):
        result: TtsProvider | None = None

        with pytest.raises(ValueError):
            result = self.jsonMapper.requireProvider('')

        assert result is None

    async def test_requireProvider_withGoogleString(self):
        result = self.jsonMapper.requireProvider('google')
        assert result is TtsProvider.GOOGLE

    async def test_requireProvider_withNone(self):
        result: TtsProvider | None = None

        with pytest.raises(ValueError):
            result = self.jsonMapper.requireProvider(None)

        assert result is None

    async def test_requireProvider_withTtsMonsterString(self):
        result = self.jsonMapper.requireProvider('tts_monster')
        assert result is TtsProvider.TTS_MONSTER

    async def test_requireProvider_withWhitespaceString(self):
        result: TtsProvider | None = None

        with pytest.raises(ValueError):
            result = self.jsonMapper.requireProvider(' ')

        assert result is None

    async def test_serializeProvider_withDecTalk(self):
        result = self.jsonMapper.serializeProvider(TtsProvider.DEC_TALK)
        assert result == 'dec_talk'

    async def test_serializeProvider_withGoogle(self):
        result = self.jsonMapper.serializeProvider(TtsProvider.GOOGLE)
        assert result == 'google'

    async def test_serializeProvider_withStreamElements(self):
        result = self.jsonMapper.serializeProvider(TtsProvider.STREAM_ELEMENTS)
        assert result == 'stream_elements'

    async def test_serializeProvider_withTtsMonster(self):
        result = self.jsonMapper.serializeProvider(TtsProvider.TTS_MONSTER)
        assert result == 'tts_monster'
