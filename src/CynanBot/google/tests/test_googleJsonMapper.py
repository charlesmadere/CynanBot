import pytest

from CynanBot.google.googleJsonMapper import GoogleJsonMapper
from CynanBot.google.googleJsonMapperInterface import GoogleJsonMapperInterface
from CynanBot.google.googleScope import GoogleScope
from CynanBot.google.googleVoiceAudioEncoding import GoogleVoiceAudioEncoding
from CynanBot.google.googleVoiceGender import GoogleVoiceGender
from CynanBot.location.timeZoneRepository import TimeZoneRepository
from CynanBot.location.timeZoneRepositoryInterface import \
    TimeZoneRepositoryInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.timber.timberStub import TimberStub


class TestGoogleJsonMapper():

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
