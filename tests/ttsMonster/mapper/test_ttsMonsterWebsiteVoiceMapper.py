import pytest

from src.ttsMonster.mapper.ttsMonsterWebsiteVoiceMapper import TtsMonsterWebsiteVoiceMapper
from src.ttsMonster.mapper.ttsMonsterWebsiteVoiceMapperInterface import TtsMonsterWebsiteVoiceMapperInterface
from src.ttsMonster.models.ttsMonsterWebsiteVoice import TtsMonsterWebsiteVoice


class TestTtsMonsterWebsiteVoiceMapper:

    mapper: TtsMonsterWebsiteVoiceMapperInterface = TtsMonsterWebsiteVoiceMapper()

    @pytest.mark.asyncio
    async def test_fromApiVoiceId_withBrianVoiceId(self):
        result = await self.mapper.fromApiVoiceId(TtsMonsterWebsiteVoice.BRIAN.voiceId)
        assert result is TtsMonsterWebsiteVoice.BRIAN

    @pytest.mark.asyncio
    async def test_fromApiVoiceId_withEmptyString(self):
        result: TtsMonsterWebsiteVoice | None = None

        with pytest.raises(TypeError):
            result = await self.mapper.fromApiVoiceId('')

        assert result is None

    @pytest.mark.asyncio
    async def test_fromApiVoiceId_withGeraltVoiceId(self):
        result = await self.mapper.fromApiVoiceId(TtsMonsterWebsiteVoice.GERALT.voiceId)
        assert result is TtsMonsterWebsiteVoice.GERALT

    @pytest.mark.asyncio
    async def test_fromApiVoiceId_withHal9000VoiceId(self):
        result = await self.mapper.fromApiVoiceId(TtsMonsterWebsiteVoice.HAL_9000.voiceId)
        assert result is TtsMonsterWebsiteVoice.HAL_9000

    @pytest.mark.asyncio
    async def test_fromApiVoiceId_withJohnnyVoiceId(self):
        result = await self.mapper.fromApiVoiceId(TtsMonsterWebsiteVoice.JOHNNY.voiceId)
        assert result is TtsMonsterWebsiteVoice.JOHNNY

    @pytest.mark.asyncio
    async def test_fromApiVoiceId_withKkonaVoiceId(self):
        result = await self.mapper.fromApiVoiceId(TtsMonsterWebsiteVoice.KKONA.voiceId)
        assert result is TtsMonsterWebsiteVoice.KKONA

    @pytest.mark.asyncio
    async def test_fromApiVoiceId_withMeganVoiceId(self):
        result = await self.mapper.fromApiVoiceId(TtsMonsterWebsiteVoice.MEGAN.voiceId)
        assert result is TtsMonsterWebsiteVoice.MEGAN

    @pytest.mark.asyncio
    async def test_fromApiVoiceId_withNarratorVoiceId(self):
        result = await self.mapper.fromApiVoiceId(TtsMonsterWebsiteVoice.NARRATOR.voiceId)
        assert result is TtsMonsterWebsiteVoice.NARRATOR

    @pytest.mark.asyncio
    async def test_fromApiVoiceId_withNone(self):
        result: TtsMonsterWebsiteVoice | None = None

        with pytest.raises(TypeError):
            # noinspection PyTypeChecker
            result = await self.mapper.fromApiVoiceId(None) # type: ignore

        assert result is None

    @pytest.mark.asyncio
    async def test_fromApiVoiceId_withShadowVoiceId(self):
        result = await self.mapper.fromApiVoiceId(TtsMonsterWebsiteVoice.SHADOW.voiceId)
        assert result is TtsMonsterWebsiteVoice.SHADOW

    @pytest.mark.asyncio
    async def test_fromApiVoiceId_withWhitespaceString(self):
        result: TtsMonsterWebsiteVoice | None = None

        with pytest.raises(TypeError):
            result = await self.mapper.fromApiVoiceId(' ')

        assert result is None

    @pytest.mark.asyncio
    async def test_fromApiVoiceId_withZeroTwoVoiceId(self):
        result = await self.mapper.fromApiVoiceId(TtsMonsterWebsiteVoice.ZERO_TWO.voiceId)
        assert result is TtsMonsterWebsiteVoice.ZERO_TWO

    @pytest.mark.asyncio
    async def test_fromWebsiteName_withBlahBlah(self):
        result: TtsMonsterWebsiteVoice | None = None

        with pytest.raises(ValueError):
            result = await self.mapper.fromWebsiteName('blahblah')

        assert result is None

    @pytest.mark.asyncio
    async def test_fromWebsiteName_withBrian(self):
        result = await self.mapper.fromWebsiteName('brian')
        assert result is TtsMonsterWebsiteVoice.BRIAN

    @pytest.mark.asyncio
    async def test_fromWebsiteName_withEmptyString(self):
        result: TtsMonsterWebsiteVoice | None = None

        with pytest.raises(TypeError):
            result = await self.mapper.fromWebsiteName('')

        assert result is None

    @pytest.mark.asyncio
    async def test_fromWebsiteName_withGeralt(self):
        result = await self.mapper.fromWebsiteName('geralt')
        assert result is TtsMonsterWebsiteVoice.GERALT

    @pytest.mark.asyncio
    async def test_fromWebsiteName_withHal9000(self):
        result = await self.mapper.fromWebsiteName('hal9000')
        assert result is TtsMonsterWebsiteVoice.HAL_9000

    @pytest.mark.asyncio
    async def test_fromWebsiteName_withJohnny(self):
        result = await self.mapper.fromWebsiteName('johnny')
        assert result is TtsMonsterWebsiteVoice.JOHNNY

    @pytest.mark.asyncio
    async def test_fromWebsiteName_withKkona(self):
        result = await self.mapper.fromWebsiteName('kkona')
        assert result is TtsMonsterWebsiteVoice.KKONA

    @pytest.mark.asyncio
    async def test_fromWebsiteName_withMegan(self):
        result = await self.mapper.fromWebsiteName('megan')
        assert result is TtsMonsterWebsiteVoice.MEGAN

    @pytest.mark.asyncio
    async def test_fromWebsiteName_withNarrator(self):
        result = await self.mapper.fromWebsiteName('narrator')
        assert result is TtsMonsterWebsiteVoice.NARRATOR

    @pytest.mark.asyncio
    async def test_fromWebsiteName_withNone(self):
        result: TtsMonsterWebsiteVoice | None = None

        with pytest.raises(TypeError):
            # noinspection PyTypeChecker
            result = await self.mapper.fromWebsiteName(None) # type: ignore

        assert result is None

    @pytest.mark.asyncio
    async def test_fromWebsiteName_withShadow(self):
        result = await self.mapper.fromWebsiteName('shadow')
        assert result is TtsMonsterWebsiteVoice.SHADOW

    @pytest.mark.asyncio
    async def test_fromWebsiteName_withWhitespaceString(self):
        result: TtsMonsterWebsiteVoice | None = None

        with pytest.raises(TypeError):
            result = await self.mapper.fromWebsiteName(' ')

        assert result is None

    @pytest.mark.asyncio
    async def test_fromWebsiteName_withZeroTwo(self):
        result = await self.mapper.fromWebsiteName('zerotwo')
        assert result is TtsMonsterWebsiteVoice.ZERO_TWO
