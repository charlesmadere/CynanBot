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
    async def test_allTtsProvidersAreParsed(self):
        for ttsProvider in TtsProvider:
            serializedTtsProvider = await self.jsonMapper.asyncSerializeProvider(ttsProvider)
            parsedTtsProvider = await self.jsonMapper.asyncParseProvider(serializedTtsProvider)
            assert parsedTtsProvider == ttsProvider

    @pytest.mark.asyncio
    async def test_allTtsProvidersAreSerialized(self):
        serializedTtsProviders: set[str] = set()

        for ttsProvider in TtsProvider:
            serializedTtsProvider = await self.jsonMapper.asyncSerializeProvider(ttsProvider)
            serializedTtsProviders.add(serializedTtsProvider)

        assert len(serializedTtsProviders) == len(list(TtsProvider))

    @pytest.mark.asyncio
    async def test_asyncParseProvider_withDecTalkString(self):
        result = await self.jsonMapper.asyncParseProvider('dec_talk')
        assert result is TtsProvider.DEC_TALK

    @pytest.mark.asyncio
    async def test_asyncParseProvider_withEmptyString(self):
        result = await self.jsonMapper.asyncParseProvider('')
        assert result is None

    @pytest.mark.asyncio
    async def test_asyncParseProvider_withGoogleString(self):
        result = await self.jsonMapper.asyncParseProvider('google')
        assert result is TtsProvider.GOOGLE

    @pytest.mark.asyncio
    async def test_asyncParseProvider_withHalfLifeString(self):
        result = await self.jsonMapper.asyncParseProvider('half_life')
        assert result is TtsProvider.HALF_LIFE

    @pytest.mark.asyncio
    async def test_asyncParseProvider_withMicrosoftSamString(self):
        result = await self.jsonMapper.asyncParseProvider('microsoft_sam')
        assert result is TtsProvider.MICROSOFT_SAM

    @pytest.mark.asyncio
    async def test_asyncParseProvider_withSingingDecTalk(self):
        result = await self.jsonMapper.asyncParseProvider('singing_dec_talk')
        assert result is TtsProvider.SINGING_DEC_TALK

    @pytest.mark.asyncio
    async def test_asyncParseProvider_withStreamElementsString(self):
        result = await self.jsonMapper.asyncParseProvider('stream_elements')
        assert result is TtsProvider.STREAM_ELEMENTS

    @pytest.mark.asyncio
    async def test_asyncParseProvider_withTtsMonsterString(self):
        result = await self.jsonMapper.asyncParseProvider('tts_monster')
        assert result is TtsProvider.TTS_MONSTER

    @pytest.mark.asyncio
    async def test_asyncParseProvider_withWhitespaceString(self):
        result = await self.jsonMapper.asyncParseProvider(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_asyncSerializeProvider_withDecTalk(self):
        result = await self.jsonMapper.asyncSerializeProvider(TtsProvider.DEC_TALK)
        assert result == 'dec_talk'

    @pytest.mark.asyncio
    async def test_asyncSerializeProvider_withGoogle(self):
        result = await self.jsonMapper.asyncSerializeProvider(TtsProvider.GOOGLE)
        assert result == 'google'

    @pytest.mark.asyncio
    async def test_asyncSerializeProvider_withHalfLife(self):
        result = await self.jsonMapper.asyncSerializeProvider(TtsProvider.HALF_LIFE)
        assert result == 'half_life'

    @pytest.mark.asyncio
    async def test_asyncSerializeProvider_withMicrosoftSam(self):
        result = await self.jsonMapper.asyncSerializeProvider(TtsProvider.MICROSOFT_SAM)
        assert result == 'microsoft_sam'

    @pytest.mark.asyncio
    async def test_asyncSerializeProvider_withNone(self):
        result: str | None = None

        with pytest.raises(TypeError):
            result = await self.jsonMapper.asyncSerializeProvider(None) # type: ignore

        assert result is None

    @pytest.mark.asyncio
    async def test_asyncSerializeProvider_withSingingDecTalk(self):
        result = await self.jsonMapper.asyncSerializeProvider(TtsProvider.SINGING_DEC_TALK)
        assert result == 'singing_dec_talk'

    @pytest.mark.asyncio
    async def test_asyncSerializeProvider_withStreamElements(self):
        result = await self.jsonMapper.asyncSerializeProvider(TtsProvider.STREAM_ELEMENTS)
        assert result == 'stream_elements'

    @pytest.mark.asyncio
    async def test_asyncSerializeProvider_withTtsMonster(self):
        result = await self.jsonMapper.asyncSerializeProvider(TtsProvider.TTS_MONSTER)
        assert result == 'tts_monster'

    def test_parseProvider_withDecTalkString(self):
        result = self.jsonMapper.parseProvider('dec_talk')
        assert result is TtsProvider.DEC_TALK

    def test_parseProvider_withEmptyString(self):
        result = self.jsonMapper.parseProvider('')
        assert result is None

    def test_parseProvider_withGoogleString(self):
        result = self.jsonMapper.parseProvider('google')
        assert result is TtsProvider.GOOGLE

    def test_parseProvider_withHalfLifeString(self):
        result = self.jsonMapper.parseProvider('half_life')
        assert result is TtsProvider.HALF_LIFE

    def test_parseProvider_withMicrosoftSamString(self):
        result = self.jsonMapper.parseProvider('microsoft_sam')
        assert result is TtsProvider.MICROSOFT_SAM

    def test_parseProvider_withNone(self):
        result = self.jsonMapper.parseProvider(None)
        assert result is None

    def test_parseProvider_withSingingDecTalkString(self):
        result = self.jsonMapper.parseProvider('singing_dec_talk')
        assert result is TtsProvider.SINGING_DEC_TALK

    def test_parseProvider_withStreamElementsString(self):
        result = self.jsonMapper.parseProvider('stream_elements')
        assert result is TtsProvider.STREAM_ELEMENTS

    def test_parseProvider_withTtsMonsterString(self):
        result = self.jsonMapper.parseProvider('tts_monster')
        assert result is TtsProvider.TTS_MONSTER

    def test_parseProvider_withWhitespaceString(self):
        result = self.jsonMapper.parseProvider(' ')
        assert result is None

    def test_requireProvider_withDecTalkString(self):
        result = self.jsonMapper.requireProvider('dec_talk')
        assert result is TtsProvider.DEC_TALK

    def test_requireProvider_withEmptyString(self):
        result: TtsProvider | None = None

        with pytest.raises(Exception):
            result = self.jsonMapper.requireProvider('')

        assert result is None

    def test_requireProvider_withGoogleString(self):
        result = self.jsonMapper.requireProvider('google')
        assert result is TtsProvider.GOOGLE

    def test_requireProvider_withHalfLifeString(self):
        result = self.jsonMapper.requireProvider('half_life')
        assert result is TtsProvider.HALF_LIFE

    def test_requireProvider_withMicrosoftSamString(self):
        result = self.jsonMapper.requireProvider('microsoft_sam')
        assert result is TtsProvider.MICROSOFT_SAM

    def test_requireProvider_withNone(self):
        result: TtsProvider | None = None

        with pytest.raises(Exception):
            result = self.jsonMapper.requireProvider(None)

        assert result is None

    def test_requireProvider_withSingingDecTalkString(self):
        result = self.jsonMapper.requireProvider('singing_dec_talk')
        assert result is TtsProvider.SINGING_DEC_TALK

    def test_requireProvider_withStreamElementsString(self):
        result = self.jsonMapper.requireProvider('stream_elements')
        assert result is TtsProvider.STREAM_ELEMENTS

    def test_requireProvider_withTtsMonsterString(self):
        result = self.jsonMapper.requireProvider('tts_monster')
        assert result is TtsProvider.TTS_MONSTER

    def test_requireProvider_withWhitespaceString(self):
        result: TtsProvider | None = None

        with pytest.raises(Exception):
            result = self.jsonMapper.requireProvider(' ')

        assert result is None

    def test_serializeProvider_withDecTalk(self):
        result = self.jsonMapper.serializeProvider(TtsProvider.DEC_TALK)
        assert result == 'dec_talk'

    def test_serializeProvider_withGoogle(self):
        result = self.jsonMapper.serializeProvider(TtsProvider.GOOGLE)
        assert result == 'google'

    def test_serializeProvider_withHalfLife(self):
        result = self.jsonMapper.serializeProvider(TtsProvider.HALF_LIFE)
        assert result == 'half_life'

    def test_serializeProvider_withMicrosoftSam(self):
        result = self.jsonMapper.serializeProvider(TtsProvider.MICROSOFT_SAM)
        assert result == 'microsoft_sam'

    def test_serializeProvider_withNone(self):
        result: str | None = None

        with pytest.raises(Exception):
            result = self.jsonMapper.serializeProvider(None) # type: ignore

        assert result is None

    def test_serializeProvider_withSingingDecTalk(self):
        result = self.jsonMapper.serializeProvider(TtsProvider.SINGING_DEC_TALK)
        assert result == 'singing_dec_talk'

    def test_serializeProvider_withStreamElements(self):
        result = self.jsonMapper.serializeProvider(TtsProvider.STREAM_ELEMENTS)
        assert result == 'stream_elements'

    def test_serializeProvider_withTtsMonster(self):
        result = self.jsonMapper.serializeProvider(TtsProvider.TTS_MONSTER)
        assert result == 'tts_monster'
