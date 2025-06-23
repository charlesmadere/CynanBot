import traceback
from datetime import datetime, timedelta
from typing import Any, Collection, Final

from frozenlist import FrozenList

from .googleJsonMapperInterface import GoogleJsonMapperInterface
from ..accessToken.googleAccessToken import GoogleAccessToken
from ..models.absGoogleTextSynthesisInput import AbsGoogleTextSynthesisInput
from ..models.googleMultiSpeakerMarkup import GoogleMultiSpeakerMarkup
from ..models.googleMultiSpeakerMarkupTurn import GoogleMultiSpeakerMarkupTurn
from ..models.googleMultiSpeakerTextSynthesisInput import GoogleMultiSpeakerTextSynthesisInput
from ..models.googleMultiSpeakerVoicePreset import GoogleMultiSpeakerVoicePreset
from ..models.googleScope import GoogleScope
from ..models.googleTextSynthesisInput import GoogleTextSynthesisInput
from ..models.googleTextSynthesisResponse import GoogleTextSynthesisResponse
from ..models.googleTextSynthesizeRequest import GoogleTextSynthesizeRequest
from ..models.googleTranslateTextGlossaryConfig import GoogleTranslateTextGlossaryConfig
from ..models.googleTranslateTextResponse import GoogleTranslateTextResponse
from ..models.googleTranslateTextTransliterationConfig import GoogleTranslateTextTransliterationConfig
from ..models.googleTranslation import GoogleTranslation
from ..models.googleTranslationRequest import GoogleTranslationRequest
from ..models.googleVoiceAudioConfig import GoogleVoiceAudioConfig
from ..models.googleVoiceAudioEncoding import GoogleVoiceAudioEncoding
from ..models.googleVoiceGender import GoogleVoiceGender
from ..models.googleVoicePreset import GoogleVoicePreset
from ..models.googleVoiceSelectionParams import GoogleVoiceSelectionParams
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class GoogleJsonMapper(GoogleJsonMapperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository

    async def parseAccessToken(
        self,
        jsonContents: dict[str, Any] | None | Any
    ) -> GoogleAccessToken | None:
        if jsonContents is None or len(jsonContents) == 0:
            return None

        now = datetime.now(self.__timeZoneRepository.getDefault())
        expiresIn = utils.getIntFromDict(jsonContents, 'expires_in')
        expireTime = now + timedelta(seconds = expiresIn)

        accessToken = utils.getStrFromDict(jsonContents, 'access_token')

        return GoogleAccessToken(
            expireTime = expireTime,
            accessToken = accessToken
        )

    async def parseTextSynthesisResponse(
        self,
        jsonContents: dict[str, Any] | None | Any
    ) -> GoogleTextSynthesisResponse | None:
        if jsonContents is None or len(jsonContents) == 0:
            return None

        audioConfig = await self.parseVoiceAudioConfig(jsonContents.get('audioConfig'))
        audioContent = utils.getStrFromDict(jsonContents, 'audioContent')

        return GoogleTextSynthesisResponse(
            audioConfig = audioConfig,
            audioContent = audioContent
        )

    async def parseTranslateTextGlossaryConfig(
        self,
        jsonContents: dict[str, Any] | None
    ) -> GoogleTranslateTextGlossaryConfig | None:
        if jsonContents is None or len(jsonContents) == 0:
            return None

        ignoreCase = utils.getBoolFromDict(jsonContents, 'ignoreCase')

        glossary: str | None = None
        if 'glossary' in jsonContents and utils.isValidStr(jsonContents.get('glossary')):
            glossary = utils.getStrFromDict(jsonContents, 'glossary')

        return GoogleTranslateTextGlossaryConfig(
            ignoreCase = ignoreCase,
            glossary = glossary
        )

    async def parseTranslateTextResponse(
        self,
        jsonContents: dict[str, Any] | None | Any
    ) -> GoogleTranslateTextResponse | None:
        if jsonContents is None or len(jsonContents) == 0:
            return None

        glossaryTranslations: FrozenList[GoogleTranslation] | None = None
        glossaryTranslationsJson: list[dict[str, Any]] | None = jsonContents.get('glossaryTranslations')

        if isinstance(glossaryTranslationsJson, list):
            glossaryTranslations = FrozenList()

            for glossaryTranslationJson in glossaryTranslationsJson:
                glossaryTranslation = await self.parseTranslation(glossaryTranslationJson)

                if glossaryTranslation is not None:
                    glossaryTranslations.append(glossaryTranslation)

            glossaryTranslations.freeze()

        translations: FrozenList[GoogleTranslation] | None = None
        translationsJson: list[dict[str, Any]] | None = jsonContents.get('translations')

        if isinstance(translationsJson, list):
            translations = FrozenList()

            for translationJson in translationsJson:
                translation = await self.parseTranslation(translationJson)

                if translation is not None:
                    translations.append(translation)

            translations.freeze()

        return GoogleTranslateTextResponse(
            glossaryTranslations = glossaryTranslations,
            translations = translations
        )

    async def parseTranslation(
        self,
        jsonContents: dict[str, Any] | None
    ) -> GoogleTranslation | None:
        if jsonContents is None or len(jsonContents) == 0:
            return None

        glossaryConfig = await self.parseTranslateTextGlossaryConfig(jsonContents.get('glossaryConfig'))

        detectedLanguageCode: str | None = None
        if 'detectedLanguageCode' in jsonContents and utils.isValidStr(jsonContents.get('detectedLanguageCode')):
            detectedLanguageCode = utils.getStrFromDict(jsonContents, 'detectedLanguageCode')

        model: str | None = None
        if 'model' in jsonContents and utils.isValidStr(jsonContents.get('model')):
            model = utils.getStrFromDict(jsonContents, 'model')

        translatedText: str | None = None
        if 'translatedText' in jsonContents and utils.isValidStr(jsonContents.get('translatedText')):
            translatedText = utils.getStrFromDict(jsonContents, 'translatedText')

        return GoogleTranslation(
            glossaryConfig = glossaryConfig,
            detectedLanguageCode = detectedLanguageCode,
            model = model,
            translatedText = translatedText
        )

    async def parseVoiceAudioConfig(
        self,
        jsonContents: dict[str, Any] | None
    ) -> GoogleVoiceAudioConfig | None:
        if jsonContents is None or len(jsonContents) == 0:
            return None

        pitch: float | None = None
        if 'pitch' in jsonContents and utils.isValidNum(jsonContents.get('pitch')):
            pitch = utils.getFloatFromDict(jsonContents, 'pitch')

        speakingRate: float | None = None
        if 'speakingRate' in jsonContents and utils.isValidNum(jsonContents.get('speakingRate')):
            speakingRate = utils.getFloatFromDict(jsonContents, 'speakingRate')

        volumeGainDb: float | None = None
        if 'volumeGainDb' in jsonContents and utils.isValidNum(jsonContents.get('volumeGainDb')):
            volumeGainDb = utils.getFloatFromDict(jsonContents, 'volumeGainDb')

        sampleRateHertz: int | None = None
        if 'sampleRateHertz' in jsonContents and utils.isValidNum(jsonContents.get('sampleRateHertz')):
            sampleRateHertz = utils.getIntFromDict(jsonContents, 'sampleRateHertz')

        audioEncoding = await self.parseVoiceAudioEncoding(jsonContents.get('audioEncoding'))
        if audioEncoding is None:
            exception = ValueError(f'Failed to parse \"audioEncoding\" field into a GoogleVoiceAudioEncoding! ({jsonContents=}) ({audioEncoding=})')
            self.__timber.log('GoogleJsonMapper', f'Unable to construct a GoogleVoiceAudioConfig instance as there is no audio encoding ({jsonContents=}) ({audioEncoding=})', exception, traceback.format_exc())
            raise exception

        return GoogleVoiceAudioConfig(
            pitch = pitch,
            speakingRate = speakingRate,
            volumeGainDb = volumeGainDb,
            sampleRateHertz = sampleRateHertz,
            audioEncoding = audioEncoding
        )

    async def parseVoiceAudioEncoding(
        self,
        jsonString: str | None
    ) -> GoogleVoiceAudioEncoding | None:
        if not utils.isValidStr(jsonString):
            return None

        match jsonString:
            case 'ALAW': return GoogleVoiceAudioEncoding.ALAW
            case 'AUDIO_ENCODING_UNSPECIFIED': return GoogleVoiceAudioEncoding.UNSPECIFIED
            case 'LINEAR16': return GoogleVoiceAudioEncoding.LINEAR_16
            case 'MP3': return GoogleVoiceAudioEncoding.MP3
            case 'MULAW': return GoogleVoiceAudioEncoding.MULAW
            case 'OGG_OPUS': return GoogleVoiceAudioEncoding.OGG_OPUS
            case _:
                self.__timber.log('GoogleJsonMapper', f'Encountered unknown GoogleVoiceAudioEncoding value: \"{jsonString}\"')
                return None

    async def parseVoiceGender(
        self,
        jsonString: str | None
    ) -> GoogleVoiceGender | None:
        if not utils.isValidStr(jsonString):
            return None

        match jsonString:
            case 'FEMALE': return GoogleVoiceGender.FEMALE
            case 'MALE': return GoogleVoiceGender.MALE
            case 'SSML_VOICE_GENDER_UNSPECIFIED': return GoogleVoiceGender.UNSPECIFIED
            case _:
                self.__timber.log('GoogleJsonMapper', f'Encountered unknown GoogleVoiceGender value: \"{jsonString}\"')
                return None

    async def parseVoicePreset(
        self,
        jsonString: str | Any | None
    ) -> GoogleVoicePreset | None:
        if not utils.isValidStr(jsonString):
            return None

        for voicePreset in GoogleVoicePreset:
            if jsonString == voicePreset.fullName:
                return voicePreset

        return None

    async def requireVoiceAudioEncoding(
        self,
        jsonString: str | None
    ) -> GoogleVoiceAudioEncoding:
        result = await self.parseVoiceAudioEncoding(jsonString)

        if result is None:
            raise ValueError(f'Unable to parse \"{jsonString}\" into GoogleVoiceAudioEncoding value!')

        return result

    async def requireVoicePreset(
        self,
        jsonString: str | Any | None
    ) -> GoogleVoicePreset:
        result = await self.parseVoicePreset(jsonString)

        if result is None:
            raise ValueError(f'Unable to parse \"{jsonString}\" into GoogleVoicePreset value!')

        return result

    async def serializeGlossaryConfig(
        self,
        glossaryConfig: GoogleTranslateTextGlossaryConfig
    ) -> dict[str, Any]:
        if not isinstance(glossaryConfig, GoogleTranslateTextGlossaryConfig):
            raise TypeError(f'glossaryConfig argument is malformed: \"{glossaryConfig}\"')

        dictionary: dict[str, Any] = {
            'ignoreCase': glossaryConfig.ignoreCase
        }

        if utils.isValidStr(glossaryConfig.glossary):
            dictionary['glossary'] = glossaryConfig.glossary

        return dictionary

    async def serializeMultiSpeakerMarkup(
        self,
        markup: GoogleMultiSpeakerMarkup
    ) -> dict[str, Any]:
        if not isinstance(markup, GoogleMultiSpeakerMarkup):
            raise TypeError(f'markup argument is malformed: \"{markup}\"')

        turns: list[dict[str, str]] = list()

        for markupTurn in markup.turns:
            turns.append(await self.serializeMultiSpeakerMarkupTurn(markupTurn))

        return {
            'turns': turns
        }

    async def serializeMultiSpeakerMarkupTurn(
        self,
        markupTurn: GoogleMultiSpeakerMarkupTurn
    ) -> dict[str, Any]:
        if not isinstance(markupTurn, GoogleMultiSpeakerMarkupTurn):
            raise TypeError(f'markupTurn argument is malformed: \"{markupTurn}\"')

        return {
            'speaker': await self.serializeMultiSpeakerVoicePreset(markupTurn.speaker),
            'text': markupTurn.text,
        }

    async def serializeMultiSpeakerVoicePreset(
        self,
        voicePreset: GoogleMultiSpeakerVoicePreset
    ) -> str:
        if not isinstance(voicePreset, GoogleMultiSpeakerVoicePreset):
            raise TypeError(f'voicePreset argument is malformed: \"{voicePreset}\"')

        return voicePreset.speakerCharacter

    async def serializeScope(
        self,
        scope: GoogleScope
    ) -> str:
        if not isinstance(scope, GoogleScope):
            raise TypeError(f'scope argument is malformed: \"{scope}\"')

        match scope:
            case GoogleScope.CLOUD_TEXT_TO_SPEECH: return 'https://www.googleapis.com/auth/cloud-platform'
            case GoogleScope.CLOUD_TRANSLATION: return 'https://www.googleapis.com/auth/cloud-translation'
            case _: raise ValueError(f'The given GoogleScope value is unknown: \"{scope}\"')

    async def serializeScopes(
        self,
        scopes: Collection[GoogleScope]
    ) -> str:
        if not isinstance(scopes, Collection):
            raise TypeError(f'scopes argument is malformed: \"{scopes}\"')

        frozenScopes: FrozenList[GoogleScope] = FrozenList(scopes)
        frozenScopes.freeze()

        if len(frozenScopes) == 0:
            raise ValueError(f'scopes argument is empty: \"{scopes}\"')

        scopeStrings: list[str] = list()

        for scope in frozenScopes:
            scopeStrings.append(await self.serializeScope(scope))

        scopeStrings.sort(key = lambda scopeString: scopeString.casefold())
        return ' '.join(scopeStrings)

    async def serializeSynthesizeRequest(
        self,
        synthesizeRequest: GoogleTextSynthesizeRequest
    ) -> dict[str, Any]:
        if not isinstance(synthesizeRequest, GoogleTextSynthesizeRequest):
            raise TypeError(f'synthesizeRequest argument is malformed: \"{synthesizeRequest}\"')

        audioConfig = await self.serializeVoiceAudioConfig(synthesizeRequest.audioConfig)
        synthesisInput = await self.serializeTextSynthesisInput(synthesizeRequest.synthesisInput)
        voice = await self.serializeVoiceSelectionParams(synthesizeRequest.voice)

        return {
            'audioConfig': audioConfig,
            'input': synthesisInput,
            'voice': voice,
        }

    async def serializeTextSynthesisInput(
        self,
        synthesisInput: AbsGoogleTextSynthesisInput
    ) -> dict[str, Any]:
        if not isinstance(synthesisInput, AbsGoogleTextSynthesisInput):
            raise TypeError(f'synthesisInput argument is malformed: \"{synthesisInput}\"')

        if isinstance(synthesisInput, GoogleMultiSpeakerTextSynthesisInput):
            return await self.__serializeMultiSpeakerTextSynthesisInput(synthesisInput)
        elif isinstance(synthesisInput, GoogleTextSynthesisInput):
            return await self.__serializeTextSynthesisInput(synthesisInput)
        else:
            raise ValueError(f'The given AbsGoogleTextSynthesisInput type is unknown: \"{synthesisInput}\"')

    async def __serializeMultiSpeakerTextSynthesisInput(
        self,
        synthesisInput: GoogleMultiSpeakerTextSynthesisInput
    ) -> dict[str, Any]:
        if not isinstance(synthesisInput, GoogleMultiSpeakerTextSynthesisInput):
            raise TypeError(f'synthesisInput argument is malformed: \"{synthesisInput}\"')

        multiSpeakerMarkup = await self.serializeMultiSpeakerMarkup(synthesisInput.multiSpeakerMarkup)

        return {
            'multi_speaker_markup': multiSpeakerMarkup
        }

    async def __serializeTextSynthesisInput(
        self,
        synthesisInput: GoogleTextSynthesisInput
    ) -> dict[str, Any]:
        if not isinstance(synthesisInput, GoogleTextSynthesisInput):
            raise TypeError(f'synthesisInput argument is malformed: \"{synthesisInput}\"')

        return {
            'text': synthesisInput.text
        }

    async def serializeTranslationRequest(
        self,
        translationRequest: GoogleTranslationRequest
    ) -> dict[str, Any]:
        if not isinstance(translationRequest, GoogleTranslationRequest):
            raise TypeError(f'translationRequest argument is malformed: \"{translationRequest}\"')

        dictionary: dict[str, Any] = {
            'contents': list(translationRequest.contents),
            'mimeType': translationRequest.mimeType,
            'targetLanguageCode': translationRequest.targetLanguageCode
        }

        if translationRequest.glossaryConfig is not None:
            dictionary['glossaryConfig'] = await self.serializeGlossaryConfig(translationRequest.glossaryConfig)

        if utils.isValidStr(translationRequest.model):
            dictionary['model'] = translationRequest.model

        if utils.isValidStr(translationRequest.sourceLanguageCode):
            dictionary['sourceLanguageCode'] = translationRequest.sourceLanguageCode

        if translationRequest.transliterationConfig is not None:
            dictionary['transliterationConfig'] = await self.serializeTransliterationConfig(
                transliterationConfig = translationRequest.transliterationConfig
            )

        return dictionary

    async def serializeTransliterationConfig(
        self,
        transliterationConfig: GoogleTranslateTextTransliterationConfig
    ) -> dict[str, Any]:
        if not isinstance(transliterationConfig, GoogleTranslateTextTransliterationConfig):
            raise TypeError(f'transliterationConfig argument is malformed: \"{transliterationConfig}\"')

        return {
            'enableTransliteration': transliterationConfig.enableTransliteration
        }

    async def serializeVoiceAudioConfig(
        self,
        voiceAudioConfig: GoogleVoiceAudioConfig
    ) -> dict[str, Any]:
        if not isinstance(voiceAudioConfig, GoogleVoiceAudioConfig):
            raise TypeError(f'voiceAudioConfig argument is malformed: \"{voiceAudioConfig}\"')

        dictionary: dict[str, Any] = {
            'audioEncoding': await self.serializeVoiceAudioEncoding(voiceAudioConfig.audioEncoding)
        }

        if utils.isValidNum(voiceAudioConfig.pitch):
            dictionary['pitch'] = voiceAudioConfig.pitch

        if utils.isValidInt(voiceAudioConfig.sampleRateHertz):
            dictionary['sampleRateHertz'] = voiceAudioConfig.sampleRateHertz

        if utils.isValidNum(voiceAudioConfig.speakingRate):
            dictionary['speakingRate'] = voiceAudioConfig.speakingRate

        if utils.isValidNum(voiceAudioConfig.volumeGainDb):
            dictionary['volumeGainDb'] = voiceAudioConfig.volumeGainDb

        return dictionary

    async def serializeVoiceAudioEncoding(
        self,
        voiceAudioEncoding: GoogleVoiceAudioEncoding
    ) -> str:
        if not isinstance(voiceAudioEncoding, GoogleVoiceAudioEncoding):
            raise TypeError(f'voiceAudioEncoding argument is malformed: \"{voiceAudioEncoding}\"')

        match voiceAudioEncoding:
            case GoogleVoiceAudioEncoding.ALAW: return 'ALAW'
            case GoogleVoiceAudioEncoding.LINEAR_16: return 'LINEAR16'
            case GoogleVoiceAudioEncoding.MP3: return 'MP3'
            case GoogleVoiceAudioEncoding.MULAW: return 'MULAW'
            case GoogleVoiceAudioEncoding.OGG_OPUS: return 'OGG_OPUS'
            case GoogleVoiceAudioEncoding.UNSPECIFIED:
                raise ValueError(f'The given GoogleVoiceAudioEncoding value is unsupported: \"{voiceAudioEncoding}\"')
            case _:
                raise ValueError(f'The given GoogleVoiceAudioEncoding value is unknown: \"{voiceAudioEncoding}\"')

    async def serializeVoiceGender(
        self,
        voiceGender: GoogleVoiceGender
    ) -> str:
        if not isinstance(voiceGender, GoogleVoiceGender):
            raise TypeError(f'voiceGender argument is malformed: \"{voiceGender}\"')

        match voiceGender:
            case GoogleVoiceGender.FEMALE: return 'FEMALE'
            case GoogleVoiceGender.MALE: return 'MALE'
            case GoogleVoiceGender.UNSPECIFIED: return 'SSML_VOICE_GENDER_UNSPECIFIED'
            case _: raise ValueError(f'The given GoogleVoiceGender value is unknown: \"{voiceGender}\"')

    async def serializeVoicePreset(
        self,
        voicePreset: GoogleVoicePreset
    ) -> str:
        if not isinstance(voicePreset, GoogleVoicePreset):
            raise TypeError(f'voicePreset argument is malformed: \"{voicePreset}\"')

        return voicePreset.fullName

    async def serializeVoiceSelectionParams(
        self,
        voiceSelectionParams: GoogleVoiceSelectionParams
    ) -> dict[str, Any]:
        if not isinstance(voiceSelectionParams, GoogleVoiceSelectionParams):
            raise TypeError(f'voiceSelectionParams argument is malformed: \"{voiceSelectionParams}\"')

        result: dict[str, Any] = {
            'languageCode': voiceSelectionParams.languageCode
        }

        if utils.isValidStr(voiceSelectionParams.name):
            result['name'] = voiceSelectionParams.name

        if voiceSelectionParams.gender is not None:
            result['ssmlGender'] = await self.serializeVoiceGender(voiceSelectionParams.gender)

        return result
