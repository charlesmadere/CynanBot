import pytest

from src.deepL.deepLJsonMapper import DeepLJsonMapper
from src.deepL.deepLJsonMapperInterface import DeepLJsonMapperInterface
from src.deepL.deepLTranslationRequest import DeepLTranslationRequest
from src.language.languagesRepository import LanguagesRepository
from src.language.languagesRepositoryInterface import LanguagesRepositoryInterface
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub


class TestDeepLJsonMapper:

    languagesRepository: LanguagesRepositoryInterface = LanguagesRepository()
    timber: TimberInterface = TimberStub()

    jsonMapper: DeepLJsonMapperInterface = DeepLJsonMapper(
        languagesRepository = languagesRepository,
        timber = timber
    )

    @pytest.mark.asyncio
    async def test_parseTranslationResponse_withEmptyDictionary(self):
        result = await self.jsonMapper.parseTranslationResponse(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTranslationResponse_withNone(self):
        result = await self.jsonMapper.parseTranslationResponse(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTranslationResponses_withEmptyDictionary(self):
        result = await self.jsonMapper.parseTranslationResponses(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTranslationResponses_withNone(self):
        result = await self.jsonMapper.parseTranslationResponses(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_serializeTranslationRequest(self):
        japaneseLanguageEntry = await self.languagesRepository.requireLanguageForCommand(command = 'ja')

        request = DeepLTranslationRequest(
            targetLanguage = japaneseLanguageEntry,
            text = 'Hello, World!'
        )

        result = await self.jsonMapper.serializeTranslationRequest(request)
        assert isinstance(result, dict)
        assert len(result) == 2
        assert result['target_lang'] == 'ja'

        text: list[str] = result['text']
        assert isinstance(text, list)
        assert len(text) == 1
        assert text[0] == 'Hello, World!'
