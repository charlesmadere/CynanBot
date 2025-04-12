import pytest

from src.google.jsonMapper.googleJsonMapper import GoogleJsonMapper
from src.google.jsonMapper.googleJsonMapperInterface import GoogleJsonMapperInterface
from src.google.models.googleScope import GoogleScope
from src.google.models.googleTextSynthesisInput import GoogleTextSynthesisInput
from src.google.models.googleTranslateTextTransliterationConfig import GoogleTranslateTextTransliterationConfig
from src.google.models.googleVoiceAudioEncoding import GoogleVoiceAudioEncoding
from src.google.models.googleVoiceGender import GoogleVoiceGender
from src.google.models.googleVoicePreset import GoogleVoicePreset
from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub


class TestGoogleJsonMapper:

    timber: TimberInterface = TimberStub()

    timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

    jsonMapper: GoogleJsonMapperInterface = GoogleJsonMapper(
        timber = timber,
        timeZoneRepository = timeZoneRepository
    )

    @pytest.mark.asyncio
    async def test_parseVoiceAudioEncoding_withAlaw(self):
        result = await self.jsonMapper.parseVoiceAudioEncoding('ALAW')
        assert result is GoogleVoiceAudioEncoding.ALAW

    @pytest.mark.asyncio
    async def test_parseVoiceAudioEncoding_withAudioEncodingUnspecified(self):
        result = await self.jsonMapper.parseVoiceAudioEncoding('AUDIO_ENCODING_UNSPECIFIED')
        assert result is GoogleVoiceAudioEncoding.UNSPECIFIED

    @pytest.mark.asyncio
    async def test_parseVoiceAudioEncoding_withEmptyString(self):
        result = await self.jsonMapper.parseVoiceAudioEncoding('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoiceAudioEncoding_withLinear16(self):
        result = await self.jsonMapper.parseVoiceAudioEncoding('LINEAR16')
        assert result is GoogleVoiceAudioEncoding.LINEAR_16

    @pytest.mark.asyncio
    async def test_parseVoiceAudioEncoding_withMp3(self):
        result = await self.jsonMapper.parseVoiceAudioEncoding('MP3')
        assert result is GoogleVoiceAudioEncoding.MP3

    @pytest.mark.asyncio
    async def test_parseVoiceAudioEncoding_withMulaw(self):
        result = await self.jsonMapper.parseVoiceAudioEncoding('MULAW')
        assert result is GoogleVoiceAudioEncoding.MULAW

    @pytest.mark.asyncio
    async def test_parseVoiceAudioEncoding_withNone(self):
        result = await self.jsonMapper.parseVoiceAudioEncoding(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoiceAudioEncoding_withOggOpus(self):
        result = await self.jsonMapper.parseVoiceAudioEncoding('OGG_OPUS')
        assert result is GoogleVoiceAudioEncoding.OGG_OPUS

    @pytest.mark.asyncio
    async def test_parseVoiceAudioEncoding_withWhitespace(self):
        result = await self.jsonMapper.parseVoiceAudioEncoding(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoiceGender_withEmptyString(self):
        result = await self.jsonMapper.parseVoiceGender('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoiceGender_withFemale(self):
        result = await self.jsonMapper.parseVoiceGender('FEMALE')
        assert result is GoogleVoiceGender.FEMALE

    @pytest.mark.asyncio
    async def test_parseVoiceGender_withMale(self):
        result = await self.jsonMapper.parseVoiceGender('MALE')
        assert result is GoogleVoiceGender.MALE

    @pytest.mark.asyncio
    async def test_parseVoiceGender_withNone(self):
        result = await self.jsonMapper.parseVoiceGender(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoiceGender_withSsmlVoiceGenderUnspecified(self):
        result = await self.jsonMapper.parseVoiceGender('SSML_VOICE_GENDER_UNSPECIFIED')
        assert result is GoogleVoiceGender.UNSPECIFIED

    @pytest.mark.asyncio
    async def test_parseVoiceGender_withWhitespace(self):
        result = await self.jsonMapper.parseVoiceGender(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoicePreset_withJapaneseJpStandardA(self):
        result = await self.jsonMapper.parseVoicePreset('ja-JP-Standard-A')
        assert result is GoogleVoicePreset.JAPANESE_JAPAN_STANDARD_A

    @pytest.mark.asyncio
    async def test_parseVoicePreset_withNone(self):
        result = await self.jsonMapper.parseVoicePreset(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_requireVoiceAudioEncoding_withAlaw(self):
        result = await self.jsonMapper.requireVoiceAudioEncoding('ALAW')
        assert result is GoogleVoiceAudioEncoding.ALAW

    @pytest.mark.asyncio
    async def test_requireVoiceAudioEncoding_withEmptyString(self):
        result: GoogleVoiceAudioEncoding | None = None

        with pytest.raises(Exception):
            result = await self.jsonMapper.requireVoiceAudioEncoding('')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireVoiceAudioEncoding_withLinear16(self):
        result = await self.jsonMapper.requireVoiceAudioEncoding('LINEAR16')
        assert result is GoogleVoiceAudioEncoding.LINEAR_16

    @pytest.mark.asyncio
    async def test_requireVoiceAudioEncoding_withMp3(self):
        result = await self.jsonMapper.requireVoiceAudioEncoding('MP3')
        assert result is GoogleVoiceAudioEncoding.MP3

    @pytest.mark.asyncio
    async def test_requireVoiceAudioEncoding_withMulaw(self):
        result = await self.jsonMapper.requireVoiceAudioEncoding('MULAW')
        assert result is GoogleVoiceAudioEncoding.MULAW

    @pytest.mark.asyncio
    async def test_requireVoiceAudioEncoding_withNone(self):
        result: GoogleVoiceAudioEncoding | None = None

        with pytest.raises(Exception):
            result = await self.jsonMapper.requireVoiceAudioEncoding(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireVoiceAudioEncoding_withOggOpus(self):
        result = await self.jsonMapper.requireVoiceAudioEncoding('OGG_OPUS')
        assert result is GoogleVoiceAudioEncoding.OGG_OPUS

    @pytest.mark.asyncio
    async def test_requireVoiceAudioEncoding_withWhitespaceString(self):
        result: GoogleVoiceAudioEncoding | None = None

        with pytest.raises(Exception):
            result = await self.jsonMapper.requireVoiceAudioEncoding(' ')

        assert result is None

    def test_sanity(self):
        assert self.jsonMapper is not None
        assert isinstance(self.jsonMapper, GoogleJsonMapper)
        assert isinstance(self.jsonMapper, GoogleJsonMapperInterface)

    @pytest.mark.asyncio
    async def test_serializeScope_withCloudTextToSpeech(self):
        result = await self.jsonMapper.serializeScope(GoogleScope.CLOUD_TEXT_TO_SPEECH)
        assert result == 'https://www.googleapis.com/auth/cloud-platform'

    @pytest.mark.asyncio
    async def test_serializeScope_withCloudTranslation(self):
        result = await self.jsonMapper.serializeScope(GoogleScope.CLOUD_TRANSLATION)
        assert result == 'https://www.googleapis.com/auth/cloud-translation'

    @pytest.mark.asyncio
    async def test_serializeScopes_withEmptyList(self):
        result: str | None = None

        with pytest.raises(ValueError):
            result = await self.jsonMapper.serializeScopes(list())

        assert result is None

    @pytest.mark.asyncio
    async def test_serializeScopes_withCloudTextToSpeech(self):
        scope = GoogleScope.CLOUD_TEXT_TO_SPEECH
        result = await self.jsonMapper.serializeScopes([ scope ])
        assert result == await self.jsonMapper.serializeScope(scope)

    @pytest.mark.asyncio
    async def test_serializeScopes_withCloudTextToSpeechAndCloudTranslation(self):
        result = await self.jsonMapper.serializeScopes([
            GoogleScope.CLOUD_TEXT_TO_SPEECH,
            GoogleScope.CLOUD_TRANSLATION
        ])

        textToSpeech = await self.jsonMapper.serializeScope(GoogleScope.CLOUD_TEXT_TO_SPEECH)
        translation = await self.jsonMapper.serializeScope(GoogleScope.CLOUD_TRANSLATION)
        assert result == f'{textToSpeech} {translation}'

    @pytest.mark.asyncio
    async def test_serializeScopes_withCloudTranslation(self):
        scope = GoogleScope.CLOUD_TRANSLATION
        result = await self.jsonMapper.serializeScopes([ scope ])
        assert result == await self.jsonMapper.serializeScope(scope)

    @pytest.mark.asyncio
    async def test_serializeTextSynthesisInput(self):
        input = GoogleTextSynthesisInput(
            text = 'Hello, World!'
        )

        result = await self.jsonMapper.serializeTextSynthesisInput(input)
        assert result['text'] == input.text

    @pytest.mark.asyncio
    async def test_serializeTransliterationConfig_withFalse(self):
        config = GoogleTranslateTextTransliterationConfig(
            enableTransliteration = False
        )

        result = await self.jsonMapper.serializeTransliterationConfig(config)
        assert result['enableTransliteration'] == config.enableTransliteration

    @pytest.mark.asyncio
    async def test_serializeTransliterationConfig_withTrue(self):
        config = GoogleTranslateTextTransliterationConfig(
            enableTransliteration = True
        )

        result = await self.jsonMapper.serializeTransliterationConfig(config)
        assert result['enableTransliteration'] == config.enableTransliteration

    @pytest.mark.asyncio
    async def test_serializeVoiceGender_withFemale(self):
        voiceGender = GoogleVoiceGender.FEMALE
        result = await self.jsonMapper.serializeVoiceGender(voiceGender)
        assert result == 'FEMALE'

    @pytest.mark.asyncio
    async def test_serializeVoiceGender_withMale(self):
        voiceGender = GoogleVoiceGender.MALE
        result = await self.jsonMapper.serializeVoiceGender(voiceGender)
        assert result == 'MALE'

    @pytest.mark.asyncio
    async def test_serializeVoiceGender_withUnspecified(self):
        voiceGender = GoogleVoiceGender.UNSPECIFIED
        result = await self.jsonMapper.serializeVoiceGender(voiceGender)
        assert result == 'SSML_VOICE_GENDER_UNSPECIFIED'

    @pytest.mark.asyncio
    async def test_serializeVoicePreset_withEnglishUsStandardA(self):
        result = await self.jsonMapper.serializeVoicePreset(GoogleVoicePreset.ENGLISH_US_STANDARD_A)
        assert result == 'en-US-Standard-A'
