import random

import pytest
from frozenlist import FrozenList

from src.google.jsonMapper.googleJsonMapper import GoogleJsonMapper
from src.google.jsonMapper.googleJsonMapperInterface import GoogleJsonMapperInterface
from src.google.models.googleMultiSpeakerMarkup import GoogleMultiSpeakerMarkup
from src.google.models.googleMultiSpeakerMarkupTurn import GoogleMultiSpeakerMarkupTurn
from src.google.models.googleMultiSpeakerTextSynthesisInput import GoogleMultiSpeakerTextSynthesisInput
from src.google.models.googleMultiSpeakerVoicePreset import GoogleMultiSpeakerVoicePreset
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

    mapper: GoogleJsonMapperInterface = GoogleJsonMapper(
        timber = timber,
        timeZoneRepository = timeZoneRepository
    )

    @pytest.mark.asyncio
    async def test_parseVoiceAudioEncoding_withAlaw(self):
        result = await self.mapper.parseVoiceAudioEncoding('ALAW')
        assert result is GoogleVoiceAudioEncoding.ALAW

    @pytest.mark.asyncio
    async def test_parseVoiceAudioEncoding_withAudioEncodingUnspecified(self):
        result = await self.mapper.parseVoiceAudioEncoding('AUDIO_ENCODING_UNSPECIFIED')
        assert result is GoogleVoiceAudioEncoding.UNSPECIFIED

    @pytest.mark.asyncio
    async def test_parseVoiceAudioEncoding_withEmptyString(self):
        result = await self.mapper.parseVoiceAudioEncoding('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoiceAudioEncoding_withLinear16(self):
        result = await self.mapper.parseVoiceAudioEncoding('LINEAR16')
        assert result is GoogleVoiceAudioEncoding.LINEAR_16

    @pytest.mark.asyncio
    async def test_parseVoiceAudioEncoding_withMp3(self):
        result = await self.mapper.parseVoiceAudioEncoding('MP3')
        assert result is GoogleVoiceAudioEncoding.MP3

    @pytest.mark.asyncio
    async def test_parseVoiceAudioEncoding_withMulaw(self):
        result = await self.mapper.parseVoiceAudioEncoding('MULAW')
        assert result is GoogleVoiceAudioEncoding.MULAW

    @pytest.mark.asyncio
    async def test_parseVoiceAudioEncoding_withNone(self):
        result = await self.mapper.parseVoiceAudioEncoding(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoiceAudioEncoding_withOggOpus(self):
        result = await self.mapper.parseVoiceAudioEncoding('OGG_OPUS')
        assert result is GoogleVoiceAudioEncoding.OGG_OPUS

    @pytest.mark.asyncio
    async def test_parseVoiceAudioEncoding_withWhitespace(self):
        result = await self.mapper.parseVoiceAudioEncoding(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoiceGender_withEmptyString(self):
        result = await self.mapper.parseVoiceGender('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoiceGender_withFemale(self):
        result = await self.mapper.parseVoiceGender('FEMALE')
        assert result is GoogleVoiceGender.FEMALE

    @pytest.mark.asyncio
    async def test_parseVoiceGender_withMale(self):
        result = await self.mapper.parseVoiceGender('MALE')
        assert result is GoogleVoiceGender.MALE

    @pytest.mark.asyncio
    async def test_parseVoiceGender_withNone(self):
        result = await self.mapper.parseVoiceGender(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoiceGender_withSsmlVoiceGenderUnspecified(self):
        result = await self.mapper.parseVoiceGender('SSML_VOICE_GENDER_UNSPECIFIED')
        assert result is GoogleVoiceGender.UNSPECIFIED

    @pytest.mark.asyncio
    async def test_parseVoiceGender_withWhitespace(self):
        result = await self.mapper.parseVoiceGender(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoicePreset_withEmptyString(self):
        result = await self.mapper.parseVoicePreset('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoicePreset_withEnglishUsStudioMultiSpeakerR(self):
        result = await self.mapper.parseVoicePreset('en-US-Studio-MultiSpeaker')
        assert result is GoogleMultiSpeakerVoicePreset.ENGLISH_US_STUDIO_MULTI_SPEAKER

    @pytest.mark.asyncio
    async def test_parseVoicePreset_withJapaneseJpStandardA(self):
        result = await self.mapper.parseVoicePreset('ja-JP-Standard-A')
        assert result is GoogleVoicePreset.JAPANESE_JAPAN_STANDARD_A

    @pytest.mark.asyncio
    async def test_parseVoicePreset_withNone(self):
        result = await self.mapper.parseVoicePreset(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseVoicePreset_withWhitespaceString(self):
        result = await self.mapper.parseVoicePreset(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_requireVoiceAudioEncoding_withAlaw(self):
        result = await self.mapper.requireVoiceAudioEncoding('ALAW')
        assert result is GoogleVoiceAudioEncoding.ALAW

    @pytest.mark.asyncio
    async def test_requireVoiceAudioEncoding_withEmptyString(self):
        result: GoogleVoiceAudioEncoding | None = None

        with pytest.raises(Exception):
            result = await self.mapper.requireVoiceAudioEncoding('')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireVoiceAudioEncoding_withLinear16(self):
        result = await self.mapper.requireVoiceAudioEncoding('LINEAR16')
        assert result is GoogleVoiceAudioEncoding.LINEAR_16

    @pytest.mark.asyncio
    async def test_requireVoiceAudioEncoding_withMp3(self):
        result = await self.mapper.requireVoiceAudioEncoding('MP3')
        assert result is GoogleVoiceAudioEncoding.MP3

    @pytest.mark.asyncio
    async def test_requireVoiceAudioEncoding_withMulaw(self):
        result = await self.mapper.requireVoiceAudioEncoding('MULAW')
        assert result is GoogleVoiceAudioEncoding.MULAW

    @pytest.mark.asyncio
    async def test_requireVoiceAudioEncoding_withNone(self):
        result: GoogleVoiceAudioEncoding | None = None

        with pytest.raises(Exception):
            result = await self.mapper.requireVoiceAudioEncoding(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireVoiceAudioEncoding_withOggOpus(self):
        result = await self.mapper.requireVoiceAudioEncoding('OGG_OPUS')
        assert result is GoogleVoiceAudioEncoding.OGG_OPUS

    @pytest.mark.asyncio
    async def test_requireVoiceAudioEncoding_withWhitespaceString(self):
        result: GoogleVoiceAudioEncoding | None = None

        with pytest.raises(Exception):
            result = await self.mapper.requireVoiceAudioEncoding(' ')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireVoicePreset_withEnglishUsStudioMultiSpeakerU(self):
        result = await self.mapper.requireVoicePreset('en-US-Studio-MultiSpeaker')
        assert result is GoogleMultiSpeakerVoicePreset.ENGLISH_US_STUDIO_MULTI_SPEAKER

    @pytest.mark.asyncio
    async def test_requireVoicePreset_withKoreanKoreaStandardA(self):
        result = await self.mapper.requireVoicePreset('ko-KR-Standard-A')
        assert result is GoogleVoicePreset.KOREAN_KOREA_STANDARD_A

    def test_sanity(self):
        assert self.mapper is not None
        assert isinstance(self.mapper, GoogleJsonMapper)
        assert isinstance(self.mapper, GoogleJsonMapperInterface)

    @pytest.mark.asyncio
    async def test_serializeMultiSpeakerMarkupTurn(self):
        markupTurn = GoogleMultiSpeakerMarkupTurn(
            speaker = random.choice(list(GoogleMultiSpeakerVoicePreset.ENGLISH_US_STUDIO_MULTI_SPEAKER.speakerCharacters)),
            text = 'Hello, World!'
        )

        result = await self.mapper.serializeMultiSpeakerMarkupTurn(markupTurn)
        assert len(result) == 2

        assert result['speaker'] == markupTurn.speaker
        assert result['text'] == markupTurn.text

    @pytest.mark.asyncio
    async def test_serializeScope_withCloudTextToSpeech(self):
        result = await self.mapper.serializeScope(GoogleScope.CLOUD_TEXT_TO_SPEECH)
        assert result == 'https://www.googleapis.com/auth/cloud-platform'

    @pytest.mark.asyncio
    async def test_serializeScope_withCloudTranslation(self):
        result = await self.mapper.serializeScope(GoogleScope.CLOUD_TRANSLATION)
        assert result == 'https://www.googleapis.com/auth/cloud-translation'

    @pytest.mark.asyncio
    async def test_serializeScopes_withEmptyList(self):
        result: str | None = None

        with pytest.raises(ValueError):
            result = await self.mapper.serializeScopes(list())

        assert result is None

    @pytest.mark.asyncio
    async def test_serializeScopes_withCloudTextToSpeech(self):
        scope = GoogleScope.CLOUD_TEXT_TO_SPEECH
        result = await self.mapper.serializeScopes([scope])
        assert result == await self.mapper.serializeScope(scope)

    @pytest.mark.asyncio
    async def test_serializeScopes_withCloudTextToSpeechAndCloudTranslation(self):
        result = await self.mapper.serializeScopes([
            GoogleScope.CLOUD_TEXT_TO_SPEECH,
            GoogleScope.CLOUD_TRANSLATION,
        ])

        textToSpeech = await self.mapper.serializeScope(GoogleScope.CLOUD_TEXT_TO_SPEECH)
        translation = await self.mapper.serializeScope(GoogleScope.CLOUD_TRANSLATION)
        assert result == f'{textToSpeech} {translation}'

    @pytest.mark.asyncio
    async def test_serializeScopes_withCloudTranslation(self):
        scope = GoogleScope.CLOUD_TRANSLATION
        result = await self.mapper.serializeScopes([scope])
        assert result == await self.mapper.serializeScope(scope)

    @pytest.mark.asyncio
    async def test_serializeTextSynthesisInput(self):
        synthesisInput = GoogleTextSynthesisInput(
            text = 'Hello, World!'
        )

        result = await self.mapper.serializeTextSynthesisInput(synthesisInput)
        assert len(result) == 1

        assert result['text'] == synthesisInput.text

    @pytest.mark.asyncio
    async def test_serializeTextSynthesisInput_withMultiSpeaker(self):
        speakers: list[str] = list(GoogleMultiSpeakerVoicePreset.ENGLISH_US_STUDIO_MULTI_SPEAKER.speakerCharacters)

        firstTurn = GoogleMultiSpeakerMarkupTurn(
            speaker = speakers[0],
            text = 'Hello everyone from Eddie\'s stream!'
        )

        secondTurn = GoogleMultiSpeakerMarkupTurn(
            speaker = speakers[1],
            text = 'Thanks for the raid!'
        )

        turns: FrozenList[GoogleMultiSpeakerMarkupTurn] = FrozenList()
        turns.append(firstTurn)
        turns.append(secondTurn)
        turns.freeze()

        multiSpeakerMarkup = GoogleMultiSpeakerMarkup(
            turns = turns
        )

        synthesisInput = GoogleMultiSpeakerTextSynthesisInput(
            multiSpeakerMarkup = multiSpeakerMarkup
        )

        result = await self.mapper.serializeTextSynthesisInput(synthesisInput)
        assert len(result) == 1

        multiSpeakerMarkupResult = result['multi_speaker_markup']
        assert isinstance(multiSpeakerMarkupResult, dict)
        assert len(multiSpeakerMarkupResult) == 1

        turnsResult = multiSpeakerMarkupResult['turns']
        assert isinstance(turnsResult, list)
        assert len(turnsResult) == 2

        turnResult = turnsResult[0]
        assert isinstance(turnResult, dict)
        assert len(turnResult) == 2
        assert turnResult['speaker'] == firstTurn.speaker
        assert turnResult['text'] == firstTurn.text

        turnResult = turnsResult[1]
        assert isinstance(turnResult, dict)
        assert len(turnResult) == 2
        assert turnResult['speaker'] == secondTurn.speaker
        assert turnResult['text'] == secondTurn.text

    @pytest.mark.asyncio
    async def test_serializeTransliterationConfig_withFalse(self):
        config = GoogleTranslateTextTransliterationConfig(
            enableTransliteration = False
        )

        result = await self.mapper.serializeTransliterationConfig(config)
        assert result['enableTransliteration'] == config.enableTransliteration

    @pytest.mark.asyncio
    async def test_serializeTransliterationConfig_withTrue(self):
        config = GoogleTranslateTextTransliterationConfig(
            enableTransliteration = True
        )

        result = await self.mapper.serializeTransliterationConfig(config)
        assert result['enableTransliteration'] == config.enableTransliteration

    @pytest.mark.asyncio
    async def test_serializeVoiceGender_withFemale(self):
        voiceGender = GoogleVoiceGender.FEMALE
        result = await self.mapper.serializeVoiceGender(voiceGender)
        assert result == 'FEMALE'

    @pytest.mark.asyncio
    async def test_serializeVoiceGender_withMale(self):
        voiceGender = GoogleVoiceGender.MALE
        result = await self.mapper.serializeVoiceGender(voiceGender)
        assert result == 'MALE'

    @pytest.mark.asyncio
    async def test_serializeVoiceGender_withUnspecified(self):
        voiceGender = GoogleVoiceGender.UNSPECIFIED
        result = await self.mapper.serializeVoiceGender(voiceGender)
        assert result == 'SSML_VOICE_GENDER_UNSPECIFIED'

    @pytest.mark.asyncio
    async def test_serializeVoicePreset_withEnglishUsStudioMultiSpeaker(self):
        result = await self.mapper.serializeVoicePreset(GoogleMultiSpeakerVoicePreset.ENGLISH_US_STUDIO_MULTI_SPEAKER)
        assert result == 'en-US-Studio-MultiSpeaker'

    @pytest.mark.asyncio
    async def test_serializeVoicePreset_withEnglishUsStandardA(self):
        result = await self.mapper.serializeVoicePreset(GoogleVoicePreset.ENGLISH_US_STANDARD_A)
        assert result == 'en-US-Standard-A'
