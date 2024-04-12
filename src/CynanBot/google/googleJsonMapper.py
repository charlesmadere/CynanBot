import traceback
from datetime import datetime, timedelta, timezone, tzinfo
from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.google.googleAccessToken import GoogleAccessToken
from CynanBot.google.googleJsonMapperInterface import GoogleJsonMapperInterface
from CynanBot.google.googleScope import GoogleScope
from CynanBot.google.googleTextSynthesisInput import GoogleTextSynthesisInput
from CynanBot.google.googleTextSynthesisResponse import \
    GoogleTextSynthesisResponse
from CynanBot.google.googleTextSynthesizeRequest import \
    GoogleTextSynthesizeRequest
from CynanBot.google.googleTranslateTextGlossaryConfig import \
    GoogleTranslateTextGlossaryConfig
from CynanBot.google.googleTranslateTextResponse import \
    GoogleTranslateTextResponse
from CynanBot.google.googleTranslateTextTransliterationConfig import \
    GoogleTranslateTextTransliterationConfig
from CynanBot.google.googleTranslation import GoogleTranslation
from CynanBot.google.googleTranslationRequest import GoogleTranslationRequest
from CynanBot.google.googleVoiceAudioConfig import GoogleVoiceAudioConfig
from CynanBot.google.googleVoiceAudioEncoding import GoogleVoiceAudioEncoding
from CynanBot.google.googleVoiceGender import GoogleVoiceGender
from CynanBot.google.googleVoiceSelectionParams import \
    GoogleVoiceSelectionParams
from CynanBot.timber.timberInterface import TimberInterface


class GoogleJsonMapper(GoogleJsonMapperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        timeZone: tzinfo = timezone.utc
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZone, tzinfo):
            raise TypeError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__timber: TimberInterface = timber
        self.__timeZone: tzinfo = timeZone

    async def parseAccessToken(
        self,
        jsonContents: dict[str, Any] | None
    ) -> GoogleAccessToken | None:
        if jsonContents is None or len(jsonContents) == 0:
            return None

        now = datetime.now(self.__timeZone)
        expiresIn = utils.getIntFromDict(jsonContents, 'expires_in')
        expireTime = now + timedelta(seconds = expiresIn)

        accessToken = utils.getStrFromDict(jsonContents, 'access_token')

        return GoogleAccessToken(
            expireTime = expireTime,
            accessToken = accessToken
        )

    async def parseTextSynthesisResponse(
        self,
        jsonContents: dict[str, Any] | None
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
        jsonContents: dict[str, Any] | None
    ) -> GoogleTranslateTextResponse | None:
        if jsonContents is None or len(jsonContents) == 0:
            return None

        glossaryTranslations: list[GoogleTranslation] | None = None
        glossaryTranslationsJson: list[dict[str, Any]] | None = jsonContents.get('glossaryTranslations')

        if isinstance(glossaryTranslationsJson, list):
            glossaryTranslations = list()

            for glossaryTranslationJson in glossaryTranslationsJson:
                glossaryTranslation = await self.parseTranslation(glossaryTranslationJson)

                if glossaryTranslation is not None:
                    glossaryTranslations.append(glossaryTranslation)

        translations: list[GoogleTranslation] | None = None
        translationsJson: list[dict[str, Any]] | None = jsonContents.get('translations')

        if isinstance(translationsJson, list):
            translations = list()

            for translationJson in translationsJson:
                translation = await self.parseTranslation(translationJson)

                if translation is not None:
                    translations.append(translation)

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

        if jsonString == 'ALAW':
            return GoogleVoiceAudioEncoding.ALAW
        elif jsonString == 'AUDIO_ENCODING_UNSPECIFIED':
            return GoogleVoiceAudioEncoding.UNSPECIFIED
        elif jsonString == 'LINEAR16':
            return GoogleVoiceAudioEncoding.LINEAR_16
        elif jsonString == 'MP3':
            return GoogleVoiceAudioEncoding.MP3
        elif jsonString == 'MULAW':
            return GoogleVoiceAudioEncoding.MULAW
        elif jsonString == 'OGG_OPUS':
            return GoogleVoiceAudioEncoding.OGG_OPUS
        else:
            self.__timber.log('GoogleJsonMapper', f'Encountered unknown GoogleVoiceAudioEncoding value: \"{jsonString}\"')
            return None

    async def parseVoiceGender(
        self,
        jsonString: str | None
    ) -> GoogleVoiceGender | None:
        if not utils.isValidStr(jsonString):
            return None

        if jsonString == 'FEMALE':
            return GoogleVoiceGender.FEMALE
        elif jsonString == 'MALE':
            return GoogleVoiceGender.MALE
        elif jsonString == 'SSML_VOICE_GENDER_UNSPECIFIED':
            return GoogleVoiceGender.UNSPECIFIED
        else:
            self.__timber.log('GoogleJsonMapper', f'Encountered unknown GoogleVoiceGender value: \"{jsonString}\"')
            return None

    async def serializeGlossaryConfig(
        self,
        glossaryConfig: GoogleTranslateTextGlossaryConfig
    ) -> dict[str, Any]:
        if not isinstance(glossaryConfig, GoogleTranslateTextGlossaryConfig):
            raise TypeError(f'glossaryConfig argument is malformed: \"{glossaryConfig}\"')

        dictionary: dict[str, Any] = {
            'ignoreCase': glossaryConfig.getIgnoreCase()
        }

        if utils.isValidStr(glossaryConfig.getGlossary()):
            dictionary['glossary'] = glossaryConfig.getGlossary()

        return dictionary

    async def serializeScope(
        self,
        scope: GoogleScope
    ) -> str:
        if not isinstance(scope, GoogleScope):
            raise TypeError(f'scope argument is malformed: \"{scope}\"')

        if scope is GoogleScope.CLOUD_TEXT_TO_SPEECH:
            return 'https://www.googleapis.com/auth/cloud-platform'
        elif scope is GoogleScope.CLOUD_TRANSLATION:
            return 'https://www.googleapis.com/auth/cloud-translation'
        else:
            raise ValueError(f'The given GoogleScope value is unknown: \"{scope}\"')

    async def serializeScopes(
        self,
        scopes: list[GoogleScope]
    ) -> str:
        if not isinstance(scopes, list):
            raise TypeError(f'scopes argument is malformed: \"{scopes}\"')
        elif len(scopes) == 0:
            raise ValueError(f'scopes argument is empty: \"{scopes}\"')

        scopeStrings: list[str] = list()

        for scope in scopes:
            scopeStrings.append(await self.serializeScope(scope))

        return ' '.join(scopeStrings)

    async def serializeSynthesizeRequest(
        self,
        synthesizeRequest: GoogleTextSynthesizeRequest
    ) -> dict[str, Any]:
        if not isinstance(synthesizeRequest, GoogleTextSynthesizeRequest):
            raise TypeError(f'synthesizeRequest argument is malformed: \"{synthesizeRequest}\"')

        return {
            'audioConfig': await self.serializeVoiceAudioConfig(synthesizeRequest.getAudioConfig()),
            'input': await self.serializeTextSynthesisInput(synthesizeRequest.getInput()),
            'voice': await self.serializeVoiceSelectionParams(synthesizeRequest.getVoice())
        }

    async def serializeTextSynthesisInput(
        self,
        textSynthesisInput: GoogleTextSynthesisInput
    ) -> dict[str, Any]:
        if not isinstance(textSynthesisInput, GoogleTextSynthesisInput):
            raise TypeError(f'textSynthesisInput argument is malformed: \"{textSynthesisInput}\"')

        return {
            'text': textSynthesisInput.getText()
        }

    async def serializeTranslationRequest(
        self,
        translationRequest: GoogleTranslationRequest
    ) -> dict[str, Any]:
        if not isinstance(translationRequest, GoogleTranslationRequest):
            raise TypeError(f'translationRequest argument is malformed: \"{translationRequest}\"')

        dictionary: dict[str, Any] = {
            'contents': translationRequest.getContents(),
            'mimeType': translationRequest.getMimeType(),
            'targetLanguageCode': translationRequest.getTargetLanguageCode()
        }

        glossaryConfig = translationRequest.getGlossaryConfig()
        if glossaryConfig is not None:
            dictionary['glossaryConfig'] = await self.serializeGlossaryConfig(glossaryConfig)

        if utils.isValidStr(translationRequest.getModel()):
            dictionary['model'] = translationRequest.getModel()

        if utils.isValidStr(translationRequest.getSourceLanguageCode()):
            dictionary['sourceLanguageCode'] = translationRequest.getSourceLanguageCode()

        transliterationConfig = translationRequest.getTransliterationConfig()
        if transliterationConfig is not None:
            dictionary['transliterationConfig'] = await self.serializeTransliterationConfig(transliterationConfig)

        return dictionary

    async def serializeTransliterationConfig(
        self,
        transliterationConfig: GoogleTranslateTextTransliterationConfig
    ) -> dict[str, Any]:
        if not isinstance(transliterationConfig, GoogleTranslationRequest):
            raise TypeError(f'transliterationConfig argument is malformed: \"{transliterationConfig}\"')

        return {
            'enableTransliteration': transliterationConfig.getEnableTransliteration()
        }

    async def serializeVoiceAudioConfig(
        self,
        voiceAudioConfig: GoogleVoiceAudioConfig
    ) -> dict[str, Any]:
        if not isinstance(voiceAudioConfig, GoogleVoiceAudioConfig):
            raise TypeError(f'voiceAudioConfig argument is malformed: \"{voiceAudioConfig}\"')

        dictionary: dict[str, Any] = {
            'audioEncoding': await self.serializeVoiceAudioEncoding(voiceAudioConfig.getAudioEncoding())
        }

        if utils.isValidNum(voiceAudioConfig.getPitch()):
            dictionary['pitch'] = voiceAudioConfig.getPitch()

        if utils.isValidInt(voiceAudioConfig.getSampleRateHertz()):
            dictionary['sampleRateHertz'] = voiceAudioConfig.getSampleRateHertz()

        if utils.isValidNum(voiceAudioConfig.getSpeakingRate()):
            dictionary['speakingRate'] = voiceAudioConfig.getSpeakingRate()

        if utils.isValidNum(voiceAudioConfig.getVolumeGainDb()):
            dictionary['volumeGainDb'] = voiceAudioConfig.getVolumeGainDb()

        return dictionary

    async def serializeVoiceAudioEncoding(
        self,
        voiceAudioEncoding: GoogleVoiceAudioEncoding
    ) -> str:
        if not isinstance(voiceAudioEncoding, GoogleVoiceAudioEncoding):
            raise TypeError(f'voiceAudioEncoding argument is malformed: \"{voiceAudioEncoding}\"')

        if voiceAudioEncoding is GoogleVoiceAudioEncoding.ALAW:
            return 'ALAW'
        elif voiceAudioEncoding is GoogleVoiceAudioEncoding.LINEAR_16:
            return 'LINEAR16'
        elif voiceAudioEncoding is GoogleVoiceAudioEncoding.MP3:
            return 'MP3'
        elif voiceAudioEncoding is GoogleVoiceAudioEncoding.MULAW:
            return 'MULAW'
        elif voiceAudioEncoding is GoogleVoiceAudioEncoding.OGG_OPUS:
            return 'OGG_OPUS'
        elif voiceAudioEncoding is GoogleVoiceAudioEncoding.UNSPECIFIED:
            raise ValueError(f'The given GoogleVoiceAudioEncoding value is unsupported: \"{voiceAudioEncoding}\"')
        else:
            raise ValueError(f'The given GoogleVoiceAudioEncoding value is unknown: \"{voiceAudioEncoding}\"')

    async def serializeVoiceGender(
        self,
        voiceGender: GoogleVoiceGender
    ) -> str:
        if not isinstance(voiceGender, GoogleVoiceGender):
            raise TypeError(f'voiceGender argument is malformed: \"{voiceGender}\"')

        if voiceGender is GoogleVoiceGender.FEMALE:
            return 'FEMALE'
        elif voiceGender is GoogleVoiceGender.MALE:
            return 'MALE'
        elif voiceGender is GoogleVoiceGender.UNSPECIFIED:
            return 'SSML_VOICE_GENDER_UNSPECIFIED'
        else:
            raise ValueError(f'The given GoogleVoiceGender value is unknown: \"{voiceGender}\"')

    async def serializeVoiceSelectionParams(
        self,
        voiceSelectionParams: GoogleVoiceSelectionParams
    ) -> dict[str, Any]:
        if not isinstance(voiceSelectionParams, GoogleVoiceSelectionParams):
            raise TypeError(f'voiceSelectionParams argument is malformed: \"{voiceSelectionParams}\"')

        result: dict[str, Any] = {
            'languageCode': voiceSelectionParams.getLanguageCode()
        }

        name = voiceSelectionParams.getName()
        if utils.isValidStr(name):
            result['name'] = name

        gender = voiceSelectionParams.getGender()
        if gender is not None:
            result['ssmlGender'] = await self.serializeVoiceGender(gender)

        return result
