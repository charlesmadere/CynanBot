import pytest

from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.tts.jsonMapper.ttsJsonMapper import TtsJsonMapper
from src.tts.jsonMapper.ttsJsonMapperInterface import TtsJsonMapperInterface
from src.tts.models.shotgun.useAllShotgunParameters import UseAllShotgunParameters
from src.tts.models.shotgun.useExactAmountShotgunParameters import UseExactAmountShotgunParameters
from src.tts.models.shotgun.useRandomAmountShotgunParameters import UseRandomAmountShotgunParameters
from src.tts.models.ttsProvider import TtsProvider


class TestTtsJsonMapper:

    timber: TimberInterface = TimberStub()

    jsonMapper: TtsJsonMapperInterface = TtsJsonMapper(
        timber = timber,
    )

    @pytest.mark.asyncio
    async def test_allTtsProvidersAreParsed(self):
        parsedProviders: set[TtsProvider] = set()

        for ttsProvider in TtsProvider:
            serialized = await self.jsonMapper.asyncSerializeProvider(ttsProvider)
            parsed = await self.jsonMapper.asyncParseProvider(serialized)
            assert parsed is ttsProvider
            parsedProviders.add(parsed)

        assert len(parsedProviders) == len(TtsProvider)

    @pytest.mark.asyncio
    async def test_allTtsProvidersAreSerialized(self):
        serializedProviders: set[str] = set()

        for ttsProvider in TtsProvider:
            serializedProvider = await self.jsonMapper.asyncSerializeProvider(ttsProvider)
            serializedProviders.add(serializedProvider)

        assert len(serializedProviders) == len(TtsProvider)

    @pytest.mark.asyncio
    async def test_asyncParseProvider_withCommodoreSamString(self):
        result = await self.jsonMapper.asyncParseProvider('commodore_sam')
        assert result is TtsProvider.COMMODORE_SAM

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

        result = await self.jsonMapper.asyncParseProvider('googl')
        assert result is TtsProvider.GOOGLE

        result = await self.jsonMapper.asyncParseProvider('goog')
        assert result is TtsProvider.GOOGLE

    @pytest.mark.asyncio
    async def test_asyncParseProvider_withHalfLifeString(self):
        result = await self.jsonMapper.asyncParseProvider('half_life')
        assert result is TtsProvider.HALF_LIFE

        result = await self.jsonMapper.asyncParseProvider('half-life')
        assert result is TtsProvider.HALF_LIFE

        result = await self.jsonMapper.asyncParseProvider('half life')
        assert result is TtsProvider.HALF_LIFE

        result = await self.jsonMapper.asyncParseProvider('halflife')
        assert result is TtsProvider.HALF_LIFE

        result = await self.jsonMapper.asyncParseProvider('hl')
        assert result is TtsProvider.HALF_LIFE

    @pytest.mark.asyncio
    async def test_asyncParseProvider_withMicrosoftString(self):
        result = await self.jsonMapper.asyncParseProvider('microsoft')
        assert result is TtsProvider.MICROSOFT

    @pytest.mark.asyncio
    async def test_asyncParseProvider_withMicrosoftSamString(self):
        result = await self.jsonMapper.asyncParseProvider('microsoft_sam')
        assert result is TtsProvider.MICROSOFT_SAM

    @pytest.mark.asyncio
    async def test_asyncParseProvider_withNone(self):
        result = await self.jsonMapper.asyncParseProvider(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_asyncParseProvider_withRandoTts(self):
        result = await self.jsonMapper.asyncParseProvider('rando_tts')
        assert result is TtsProvider.RANDO_TTS

        result = await self.jsonMapper.asyncParseProvider('rando-tts')
        assert result is TtsProvider.RANDO_TTS

        result = await self.jsonMapper.asyncParseProvider('rando tts')
        assert result is TtsProvider.RANDO_TTS

        result = await self.jsonMapper.asyncParseProvider('randotts')
        assert result is TtsProvider.RANDO_TTS

        result = await self.jsonMapper.asyncParseProvider('rando')
        assert result is TtsProvider.RANDO_TTS

    @pytest.mark.asyncio
    async def test_asyncParseProvider_withShotgunTtsStrings(self):
        result = await self.jsonMapper.asyncParseProvider('shotgun_tts')
        assert result is TtsProvider.SHOTGUN_TTS

        result = await self.jsonMapper.asyncParseProvider('shotgun-tts')
        assert result is TtsProvider.SHOTGUN_TTS

        result = await self.jsonMapper.asyncParseProvider('shotgun tts')
        assert result is TtsProvider.SHOTGUN_TTS

        result = await self.jsonMapper.asyncParseProvider('shotguntts')
        assert result is TtsProvider.SHOTGUN_TTS

        result = await self.jsonMapper.asyncParseProvider('shotgun')
        assert result is TtsProvider.SHOTGUN_TTS

    @pytest.mark.asyncio
    async def test_asyncParseProvider_withSingingDecTalk(self):
        result = await self.jsonMapper.asyncParseProvider('singing_dec_talk')
        assert result is TtsProvider.UNRESTRICTED_DEC_TALK

    @pytest.mark.asyncio
    async def test_asyncParseProvider_withStreamElementsString(self):
        result = await self.jsonMapper.asyncParseProvider('stream_elements')
        assert result is TtsProvider.STREAM_ELEMENTS

        result = await self.jsonMapper.asyncParseProvider('stream-elements')
        assert result is TtsProvider.STREAM_ELEMENTS

        result = await self.jsonMapper.asyncParseProvider('stream elements')
        assert result is TtsProvider.STREAM_ELEMENTS

    @pytest.mark.asyncio
    async def test_asyncParseProvider_withTtsMonsterString(self):
        result = await self.jsonMapper.asyncParseProvider('tts_monster')
        assert result is TtsProvider.TTS_MONSTER

        result = await self.jsonMapper.asyncParseProvider('tts-monster')
        assert result is TtsProvider.TTS_MONSTER

        result = await self.jsonMapper.asyncParseProvider('tts monster')
        assert result is TtsProvider.TTS_MONSTER

    @pytest.mark.asyncio
    async def test_asyncParseProvider_withUnrestrictedDecTalk(self):
        result = await self.jsonMapper.asyncParseProvider('unrestricted_dec_talk')
        assert result is TtsProvider.UNRESTRICTED_DEC_TALK

        result = await self.jsonMapper.asyncParseProvider('unrestricted-dec-talk')
        assert result is TtsProvider.UNRESTRICTED_DEC_TALK

        result = await self.jsonMapper.asyncParseProvider('unrestricted dec talk')
        assert result is TtsProvider.UNRESTRICTED_DEC_TALK

    @pytest.mark.asyncio
    async def test_asyncParseProvider_withWhitespaceString(self):
        result = await self.jsonMapper.asyncParseProvider(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_asyncParseShotgunProviderUseParameters_withEmptyDictionary(self):
        result = await self.jsonMapper.asyncParseShotgunProviderUseParameters(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_asyncParseShotgunProviderUseParameters_withNone(self):
        result = await self.jsonMapper.asyncParseShotgunProviderUseParameters(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_asyncParseShotgunProviderUseParameters_withUseAllParameters(self):
        result = await self.jsonMapper.asyncParseShotgunProviderUseParameters({
            'useAll': True,
        })

        assert isinstance(result, UseAllShotgunParameters)

    @pytest.mark.asyncio
    async def test_asyncParseShotgunProviderUseParameters_withUseExactAmountParameters(self):
        parameters = UseExactAmountShotgunParameters(
            amount = 3,
        )

        result = await self.jsonMapper.asyncParseShotgunProviderUseParameters({
            'amount': parameters.amount,
        })

        assert isinstance(result, UseExactAmountShotgunParameters)
        assert result == parameters
        assert result.amount == parameters.amount

    @pytest.mark.asyncio
    async def test_asyncParseShotgunProviderUseParameters_withUseRandomAmountParameters(self):
        parameters = UseRandomAmountShotgunParameters(
            maxAmount = 5,
            minAmount = 2,
        )

        result = await self.jsonMapper.asyncParseShotgunProviderUseParameters({
            'maxAmount': parameters.maxAmount,
            'minAmount': parameters.minAmount,
        })

        assert isinstance(result, UseRandomAmountShotgunParameters)
        assert result == parameters
        assert result.maxAmount == parameters.maxAmount
        assert result.minAmount == parameters.minAmount

    @pytest.mark.asyncio
    async def test_asyncRequireProvider_withTtsMonster(self):
        result = await self.jsonMapper.asyncRequireProvider('tts_monster')
        assert result is TtsProvider.TTS_MONSTER

        result = await self.jsonMapper.asyncRequireProvider('tts-monster')
        assert result is TtsProvider.TTS_MONSTER

        result = await self.jsonMapper.asyncRequireProvider('tts monster')
        assert result is TtsProvider.TTS_MONSTER

        result = await self.jsonMapper.asyncRequireProvider('ttsmonster')
        assert result is TtsProvider.TTS_MONSTER

    @pytest.mark.asyncio
    async def test_asyncSerializeProvider_withAll(self):
        results: set[str] = set()

        for provider in TtsProvider:
            results.add(await self.jsonMapper.asyncSerializeProvider(provider))

        assert len(results) == len(TtsProvider)

    @pytest.mark.asyncio
    async def test_asyncSerializeProvider_withCommodoreSam(self):
        result = await self.jsonMapper.asyncSerializeProvider(TtsProvider.COMMODORE_SAM)
        assert result == 'commodore_sam'

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
    async def test_asyncSerializeProvider_withMicrosoft(self):
        result = await self.jsonMapper.asyncSerializeProvider(TtsProvider.MICROSOFT)
        assert result == 'microsoft'

    @pytest.mark.asyncio
    async def test_asyncSerializeProvider_withMicrosoftSam(self):
        result = await self.jsonMapper.asyncSerializeProvider(TtsProvider.MICROSOFT_SAM)
        assert result == 'microsoft_sam'

    @pytest.mark.asyncio
    async def test_asyncSerializeProvider_withRandoTts(self):
        result = await self.jsonMapper.asyncSerializeProvider(TtsProvider.RANDO_TTS)
        assert result == 'rando_tts'

    @pytest.mark.asyncio
    async def test_asyncSerializeProvider_withShotgunTts(self):
        result = await self.jsonMapper.asyncSerializeProvider(TtsProvider.SHOTGUN_TTS)
        assert result == 'shotgun_tts'

    @pytest.mark.asyncio
    async def test_asyncSerializeProvider_withStreamElements(self):
        result = await self.jsonMapper.asyncSerializeProvider(TtsProvider.STREAM_ELEMENTS)
        assert result == 'stream_elements'

    @pytest.mark.asyncio
    async def test_asyncSerializeProvider_withTtsMonster(self):
        result = await self.jsonMapper.asyncSerializeProvider(TtsProvider.TTS_MONSTER)
        assert result == 'tts_monster'

    @pytest.mark.asyncio
    async def test_asyncSerializeProvider_withUnrestrictedDecTalk(self):
        result = await self.jsonMapper.asyncSerializeProvider(TtsProvider.UNRESTRICTED_DEC_TALK)
        assert result == 'unrestricted_dec_talk'

    def test_parseProvider_withCommodoreSamString(self):
        result = self.jsonMapper.parseProvider('commodore_sam')
        assert result is TtsProvider.COMMODORE_SAM

    def test_parseProvider_withDecTalkString(self):
        result = self.jsonMapper.parseProvider('dec_talk')
        assert result is TtsProvider.DEC_TALK

    def test_parseProvider_withEmptyString(self):
        result = self.jsonMapper.parseProvider('')
        assert result is None

    def test_parseProvider_withGoogleString(self):
        result = self.jsonMapper.parseProvider('google')
        assert result is TtsProvider.GOOGLE

        result = self.jsonMapper.parseProvider('googl')
        assert result is TtsProvider.GOOGLE

        result = self.jsonMapper.parseProvider('goog')
        assert result is TtsProvider.GOOGLE

    def test_parseProvider_withHalfLifeString(self):
        result = self.jsonMapper.parseProvider('half_life')
        assert result is TtsProvider.HALF_LIFE

    def test_parseProvider_withMicrosoftString(self):
        result = self.jsonMapper.parseProvider('microsoft')
        assert result is TtsProvider.MICROSOFT

    def test_parseProvider_withMicrosoftSamString(self):
        result = self.jsonMapper.parseProvider('microsoft_sam')
        assert result is TtsProvider.MICROSOFT_SAM

    def test_parseProvider_withNone(self):
        result = self.jsonMapper.parseProvider(None)
        assert result is None

    def test_parseProvider_withRandoTtsString(self):
        result = self.jsonMapper.parseProvider('rando_tts')
        assert result is TtsProvider.RANDO_TTS

    def test_parseProvider_withShotgunTtsString(self):
        result = self.jsonMapper.parseProvider('shotgun_tts')
        assert result is TtsProvider.SHOTGUN_TTS

    def test_parseProvider_withSingingDecTalkStrings(self):
        result = self.jsonMapper.parseProvider('singing_dec_talk')
        assert result is TtsProvider.UNRESTRICTED_DEC_TALK

        result = self.jsonMapper.parseProvider('singing-dec-talk')
        assert result is TtsProvider.UNRESTRICTED_DEC_TALK

        result = self.jsonMapper.parseProvider('singing dec talk')
        assert result is TtsProvider.UNRESTRICTED_DEC_TALK

    def test_parseProvider_withStreamElementsStrings(self):
        result = self.jsonMapper.parseProvider('stream_elements')
        assert result is TtsProvider.STREAM_ELEMENTS

        result = self.jsonMapper.parseProvider('stream-elements')
        assert result is TtsProvider.STREAM_ELEMENTS

        result = self.jsonMapper.parseProvider('stream elements')
        assert result is TtsProvider.STREAM_ELEMENTS

        result = self.jsonMapper.parseProvider('streamelements')
        assert result is TtsProvider.STREAM_ELEMENTS

        result = self.jsonMapper.parseProvider('stream_element')
        assert result is TtsProvider.STREAM_ELEMENTS

        result = self.jsonMapper.parseProvider('stream-element')
        assert result is TtsProvider.STREAM_ELEMENTS

        result = self.jsonMapper.parseProvider('stream element')
        assert result is TtsProvider.STREAM_ELEMENTS

        result = self.jsonMapper.parseProvider('streamelement')
        assert result is TtsProvider.STREAM_ELEMENTS

    def test_parseProvider_withTtsMonsterStrings(self):
        result = self.jsonMapper.parseProvider('tts_monster')
        assert result is TtsProvider.TTS_MONSTER

        result = self.jsonMapper.parseProvider('tts-monster')
        assert result is TtsProvider.TTS_MONSTER

        result = self.jsonMapper.parseProvider('tts monster')
        assert result is TtsProvider.TTS_MONSTER

    def test_parseProvider_withUnrestrictedDecTalkStrings(self):
        result = self.jsonMapper.parseProvider('unrestricted_dec_talk')
        assert result is TtsProvider.UNRESTRICTED_DEC_TALK

        result = self.jsonMapper.parseProvider('unrestricted-dec-talk')
        assert result is TtsProvider.UNRESTRICTED_DEC_TALK

        result = self.jsonMapper.parseProvider('unrestricted dec talk')
        assert result is TtsProvider.UNRESTRICTED_DEC_TALK

    def test_parseProvider_withWhitespaceString(self):
        result = self.jsonMapper.parseProvider(' ')
        assert result is None

    def test_requireProvider_withCommodoreSamString(self):
        result = self.jsonMapper.requireProvider('commodore_sam')
        assert result is TtsProvider.COMMODORE_SAM

    def test_requireProvider_withDecTalkString(self):
        result = self.jsonMapper.requireProvider('dec_talk')
        assert result is TtsProvider.DEC_TALK

    def test_requireProvider_withEmptyString(self):
        result: TtsProvider | None = None

        with pytest.raises(ValueError):
            result = self.jsonMapper.requireProvider('')

        assert result is None

    def test_requireProvider_withGoogleString(self):
        result = self.jsonMapper.requireProvider('google')
        assert result is TtsProvider.GOOGLE

        result = self.jsonMapper.requireProvider('googl')
        assert result is TtsProvider.GOOGLE

        result = self.jsonMapper.requireProvider('goog')
        assert result is TtsProvider.GOOGLE

    def test_requireProvider_withHalfLifeString(self):
        result = self.jsonMapper.requireProvider('half_life')
        assert result is TtsProvider.HALF_LIFE

    def test_requireProvider_withMicrosoftString(self):
        result = self.jsonMapper.requireProvider('microsoft')
        assert result is TtsProvider.MICROSOFT

    def test_requireProvider_withMicrosoftSamString(self):
        result = self.jsonMapper.requireProvider('microsoft_sam')
        assert result is TtsProvider.MICROSOFT_SAM

    def test_requireProvider_withNone(self):
        result: TtsProvider | None = None

        with pytest.raises(ValueError):
            result = self.jsonMapper.requireProvider(None)

        assert result is None

    def test_requireProvider_withRandoTtsString(self):
        result = self.jsonMapper.requireProvider('rando_tts')
        assert result is TtsProvider.RANDO_TTS

    def test_requireProvider_withShotgunTtsString(self):
        result = self.jsonMapper.requireProvider('shotgun_tts')
        assert result is TtsProvider.SHOTGUN_TTS

    def test_requireProvider_withSingingDecTalkString(self):
        result = self.jsonMapper.requireProvider('singing_dec_talk')
        assert result is TtsProvider.UNRESTRICTED_DEC_TALK

    def test_requireProvider_withStreamElementsString(self):
        result = self.jsonMapper.requireProvider('stream_elements')
        assert result is TtsProvider.STREAM_ELEMENTS

        result = self.jsonMapper.requireProvider('stream_element')
        assert result is TtsProvider.STREAM_ELEMENTS

    def test_requireProvider_withTtsMonsterString(self):
        result = self.jsonMapper.requireProvider('tts_monster')
        assert result is TtsProvider.TTS_MONSTER

    def test_requireProvider_withUnrestrictedDecTalkString(self):
        result = self.jsonMapper.requireProvider('unrestricted_dec_talk')
        assert result is TtsProvider.UNRESTRICTED_DEC_TALK

    def test_requireProvider_withWhitespaceString(self):
        result: TtsProvider | None = None

        with pytest.raises(ValueError):
            result = self.jsonMapper.requireProvider(' ')

        assert result is None

    def test_sanity(self):
        assert self.jsonMapper is not None
        assert isinstance(self.jsonMapper, TtsJsonMapper)
        assert isinstance(self.jsonMapper, TtsJsonMapperInterface)

    def test_serializeProvider_withAll(self):
        results: set[str] = set()

        for provider in TtsProvider:
            results.add(self.jsonMapper.serializeProvider(provider))

        assert len(results) == len(TtsProvider)

    def test_serializeProvider_withCommodoreSam(self):
        result = self.jsonMapper.serializeProvider(TtsProvider.COMMODORE_SAM)
        assert result == 'commodore_sam'

    def test_serializeProvider_withDecTalk(self):
        result = self.jsonMapper.serializeProvider(TtsProvider.DEC_TALK)
        assert result == 'dec_talk'

    def test_serializeProvider_withGoogle(self):
        result = self.jsonMapper.serializeProvider(TtsProvider.GOOGLE)
        assert result == 'google'

    def test_serializeProvider_withHalfLife(self):
        result = self.jsonMapper.serializeProvider(TtsProvider.HALF_LIFE)
        assert result == 'half_life'

    def test_serializeProvider_withMicrosoft(self):
        result = self.jsonMapper.serializeProvider(TtsProvider.MICROSOFT)
        assert result == 'microsoft'

    def test_serializeProvider_withMicrosoftSam(self):
        result = self.jsonMapper.serializeProvider(TtsProvider.MICROSOFT_SAM)
        assert result == 'microsoft_sam'

    def test_serializeProvider_withRandoTts(self):
        result = self.jsonMapper.serializeProvider(TtsProvider.RANDO_TTS)
        assert result == 'rando_tts'

    def test_serializeProvider_withShotgunTts(self):
        result = self.jsonMapper.serializeProvider(TtsProvider.SHOTGUN_TTS)
        assert result == 'shotgun_tts'

    def test_serializeProvider_withStreamElements(self):
        result = self.jsonMapper.serializeProvider(TtsProvider.STREAM_ELEMENTS)
        assert result == 'stream_elements'

    def test_serializeProvider_withTtsMonster(self):
        result = self.jsonMapper.serializeProvider(TtsProvider.TTS_MONSTER)
        assert result == 'tts_monster'

    def test_serializeProvider_withUnrestrictedDecTalk(self):
        result = self.jsonMapper.serializeProvider(TtsProvider.UNRESTRICTED_DEC_TALK)
        assert result == 'unrestricted_dec_talk'
