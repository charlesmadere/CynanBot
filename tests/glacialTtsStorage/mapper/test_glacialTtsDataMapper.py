import pytest

from src.glacialTtsStorage.mapper.glacialTtsDataMapper import GlacialTtsDataMapper
from src.glacialTtsStorage.mapper.glacialTtsDataMapperInterface import GlacialTtsDataMapperInterface
from src.tts.models.ttsProvider import TtsProvider


class TestGlacialTtsDataMapper:

    mapper: GlacialTtsDataMapperInterface = GlacialTtsDataMapper()

    @pytest.mark.asyncio
    async def test_fromDatabaseName_withCommodoreSam(self):
        result = await self.mapper.fromDatabaseName('commodore_sam')
        assert result is TtsProvider.COMMODORE_SAM

    @pytest.mark.asyncio
    async def test_fromDatabaseName_withDecTalk(self):
        result = await self.mapper.fromDatabaseName('dec_talk')
        assert result is TtsProvider.DEC_TALK

    @pytest.mark.asyncio
    async def test_fromDatabaseName_withGoogle(self):
        result = await self.mapper.fromDatabaseName('google')
        assert result is TtsProvider.GOOGLE

    @pytest.mark.asyncio
    async def test_fromDatabaseName_withHalfLife(self):
        result = await self.mapper.fromDatabaseName('half_life')
        assert result is TtsProvider.HALF_LIFE

    @pytest.mark.asyncio
    async def test_fromDatabaseName_withMicrosoftSam(self):
        result = await self.mapper.fromDatabaseName('microsoft_sam')
        assert result is TtsProvider.MICROSOFT_SAM

    @pytest.mark.asyncio
    async def test_fromDatabaseName_withSingingDecTalk(self):
        result = await self.mapper.fromDatabaseName('singing_dec_talk')
        assert result is TtsProvider.SINGING_DEC_TALK

    @pytest.mark.asyncio
    async def test_fromDatabaseName_withStreamElements(self):
        result = await self.mapper.fromDatabaseName('stream_elements')
        assert result is TtsProvider.STREAM_ELEMENTS

    @pytest.mark.asyncio
    async def test_fromDatabaseName_withTtsMonster(self):
        result = await self.mapper.fromDatabaseName('tts_monster')
        assert result is TtsProvider.TTS_MONSTER

    @pytest.mark.asyncio
    async def test_toDatabaseName_withCommodoreSam(self):
        result = await self.mapper.toDatabaseName(TtsProvider.COMMODORE_SAM)
        assert result == 'commodore_sam'

    @pytest.mark.asyncio
    async def test_toDatabaseName_withDecTalk(self):
        result = await self.mapper.toDatabaseName(TtsProvider.DEC_TALK)
        assert result == 'dec_talk'

    @pytest.mark.asyncio
    async def test_toDatabaseName_withGoogle(self):
        result = await self.mapper.toDatabaseName(TtsProvider.GOOGLE)
        assert result == 'google'

    @pytest.mark.asyncio
    async def test_toDatabaseName_withHalfLife(self):
        result = await self.mapper.toDatabaseName(TtsProvider.HALF_LIFE)
        assert result == 'half_life'

    @pytest.mark.asyncio
    async def test_toDatabaseName_withMicrosoftSam(self):
        result = await self.mapper.toDatabaseName(TtsProvider.MICROSOFT_SAM)
        assert result == 'microsoft_sam'

    @pytest.mark.asyncio
    async def test_toDatabaseName_withSingingDecTalk(self):
        result = await self.mapper.toDatabaseName(TtsProvider.SINGING_DEC_TALK)
        assert result == 'singing_dec_talk'

    @pytest.mark.asyncio
    async def test_toDatabaseName_withStreamElements(self):
        result = await self.mapper.toDatabaseName(TtsProvider.STREAM_ELEMENTS)
        assert result == 'stream_elements'

    @pytest.mark.asyncio
    async def test_toDatabaseName_withTtsMonster(self):
        result = await self.mapper.toDatabaseName(TtsProvider.TTS_MONSTER)
        assert result == 'tts_monster'

    @pytest.mark.asyncio
    async def test_toFolderName_withCommodoreSam(self):
        result = await self.mapper.toFolderName(TtsProvider.COMMODORE_SAM)
        assert result == 'commodore_sam'

    @pytest.mark.asyncio
    async def test_toFolderName_withDecTalk(self):
        result = await self.mapper.toFolderName(TtsProvider.DEC_TALK)
        assert result == 'dec_talk'

    @pytest.mark.asyncio
    async def test_toFolderName_withGoogle(self):
        result = await self.mapper.toFolderName(TtsProvider.GOOGLE)
        assert result == 'google'

    @pytest.mark.asyncio
    async def test_toFolderName_withHalfLife(self):
        result = await self.mapper.toFolderName(TtsProvider.HALF_LIFE)
        assert result == 'half_life'

    @pytest.mark.asyncio
    async def test_toFolderName_withMicrosoftSam(self):
        result = await self.mapper.toFolderName(TtsProvider.MICROSOFT_SAM)
        assert result == 'microsoft_sam'

    @pytest.mark.asyncio
    async def test_toFolderName_withSingingDecTalk(self):
        result = await self.mapper.toFolderName(TtsProvider.SINGING_DEC_TALK)
        assert result == 'singing_dec_talk'

    @pytest.mark.asyncio
    async def test_toFolderName_withStreamElements(self):
        result = await self.mapper.toFolderName(TtsProvider.STREAM_ELEMENTS)
        assert result == 'stream_elements'

    @pytest.mark.asyncio
    async def test_toFolderName_withTtsMonster(self):
        result = await self.mapper.toFolderName(TtsProvider.TTS_MONSTER)
        assert result == 'tts_monster'

    def test_sanity(self):
        assert self.mapper is not None
        assert isinstance(self.mapper, GlacialTtsDataMapper)
        assert isinstance(self.mapper, GlacialTtsDataMapperInterface)
