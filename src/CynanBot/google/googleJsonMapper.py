import traceback
from typing import Any, Dict, List, Optional

import CynanBot.misc.utils as utils
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
        timber: TimberInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

    async def parseTextSynthesisResponse(
        self,
        jsonContents: Optional[Dict[str, Any]]
    ) -> Optional[GoogleTextSynthesisResponse]:
        if jsonContents is None or len(jsonContents) == 0:
            return None

        audioConfig = await self.parseVoiceAudioConfig(jsonContents.get('audioConfig'))
        if audioConfig is None:
            exception = ValueError(f'Failed to parse \"audioConfig\" element into a GoogleVoiceAudioConfig! ({jsonContents=}) ({audioConfig=})')
            self.__timber.log('GoogleJsonMapper', f'Unable to construct a GoogleTextSynthesisResponse instance as there is no audio config ({jsonContents=}) ({audioConfig=})', exception, traceback.format_exc())
            raise exception

        audioContent = utils.getStrFromDict(jsonContents, 'audioContent')

        return GoogleTextSynthesisResponse(
            audioConfig = audioConfig,
            audioContent = audioContent
        )

    async def parseTranslateTextGlossaryConfig(
        self,
        jsonContents: Optional[Dict[str, Any]]
    ) -> Optional[GoogleTranslateTextGlossaryConfig]:
        if jsonContents is None or len(jsonContents) == 0:
            return None

        ignoreCase = utils.getBoolFromDict(jsonContents, 'ignoreCase')

        glossary: Optional[str] = None
        if 'glossary' in jsonContents and utils.isValidStr(jsonContents.get('glossary')):
            glossary = utils.getStrFromDict(jsonContents, 'glossary')

        return GoogleTranslateTextGlossaryConfig(
            ignoreCase = ignoreCase,
            glossary = glossary
        )

    async def parseTranslateTextResponse(
        self,
        jsonContents: Optional[Dict[str, Any]]
    ) -> Optional[GoogleTranslateTextResponse]:
        if jsonContents is None or len(jsonContents) == 0:
            return None

        glossaryTranslations: Optional[List[GoogleTranslation]] = None
        glossaryTranslationsJson: Optional[List[Dict[str, Any]]] = jsonContents.get('glossaryTranslations')

        if isinstance(glossaryTranslationsJson, List):
            glossaryTranslations = list()

            for glossaryTranslationJson in glossaryTranslationsJson:
                glossaryTranslation = await self.parseTranslation(glossaryTranslationJson)

                if glossaryTranslation is not None:
                    glossaryTranslations.append(glossaryTranslation)

        translations: Optional[List[GoogleTranslation]] = None
        translationsJson: Optional[List[Dict[str, Any]]] = jsonContents.get('translations')

        if isinstance(translationsJson, List):
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
        jsonContents: Optional[Dict[str, Any]]
    ) -> Optional[GoogleTranslation]:
        if jsonContents is None or len(jsonContents) == 0:
            return None

        glossaryConfig = await self.parseTranslateTextGlossaryConfig(jsonContents.get('glossaryConfig'))
        if glossaryConfig is None:
            exception = ValueError(f'Failed to parse \"glossaryConfig\" element into a GoogleTranslateTextGlossaryConfig! ({jsonContents=}) ({glossaryConfig=})')
            self.__timber.log('GoogleJsonMapper', f'Unable to construct a GoogleTranslation instance as there is no glossary config ({jsonContents=}) ({glossaryConfig=})', exception, traceback.format_exc())
            raise exception

        detectedLanguageCode = utils.getStrFromDict(jsonContents, 'detectedLangaugeCode')

        model: Optional[str] = None
        if 'model' in jsonContents and utils.isValidStr(jsonContents.get('model')):
            model = utils.getStrFromDict(jsonContents, 'model')

        translatedText: Optional[str] = None
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
        jsonContents: Optional[Dict[str, Any]]
    ) -> Optional[GoogleVoiceAudioConfig]:
        if jsonContents is None or len(jsonContents) == 0:
            return None

        pitch: Optional[float] = None
        if 'pitch' in jsonContents and utils.isValidNum(jsonContents.get('pitch')):
            pitch = utils.getFloatFromDict(jsonContents, 'pitch')

        speakingRate: Optional[float] = None
        if 'speakingRate' in jsonContents and utils.isValidNum(jsonContents.get('speakingRate')):
            speakingRate = utils.getFloatFromDict(jsonContents, 'speakingRate')

        volumeGainDb: Optional[float] = None
        if 'volumeGainDb' in jsonContents and utils.isValidNum(jsonContents.get('volumeGainDb')):
            volumeGainDb = utils.getFloatFromDict(jsonContents, 'volumeGainDb')

        sampleRateHertz: Optional[int] = None
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
        jsonString: Optional[str]
    ) -> Optional[GoogleVoiceAudioEncoding]:
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
        elif jsonString == 'MP3_64_KBPS':
            return GoogleVoiceAudioEncoding.MP3_64_KBPS
        elif jsonString == 'MULAW':
            return GoogleVoiceAudioEncoding.MULAW
        elif jsonString == 'OGG_OPUS':
            return GoogleVoiceAudioEncoding.OGG_OPUS
        else:
            self.__timber.log('GoogleJsonMapper', f'Encountered unknown GoogleVoiceAudioEncoding value: \"{jsonString}\"')
            return None

    async def parseVoiceGender(
        self,
        jsonString: Optional[str]
    ) -> Optional[GoogleVoiceGender]:
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
    ) -> Dict[str, Any]:
        if not isinstance(glossaryConfig, GoogleTranslateTextGlossaryConfig):
            raise TypeError(f'glossaryConfig argument is malformed: \"{glossaryConfig}\"')

        dictionary: Dict[str, Any] = {
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

    async def serializeSynthesizeRequest(
        self,
        synthesizeRequest: GoogleTextSynthesizeRequest
    ) -> Dict[str, Any]:
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
    ) -> Dict[str, Any]:
        if not isinstance(textSynthesisInput, GoogleTextSynthesisInput):
            raise TypeError(f'textSynthesisInput argument is malformed: \"{textSynthesisInput}\"')

        return {
            'text': textSynthesisInput.getText()
        }

    async def serializeTranslationRequest(
        self,
        translationRequest: GoogleTranslationRequest
    ) -> Dict[str, Any]:
        if not isinstance(translationRequest, GoogleTranslationRequest):
            raise TypeError(f'translationRequest argument is malformed: \"{translationRequest}\"')

        dictionary: Dict[str, Any] = {
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
    ) -> Dict[str, Any]:
        if not isinstance(transliterationConfig, GoogleTranslationRequest):
            raise TypeError(f'transliterationConfig argument is malformed: \"{transliterationConfig}\"')

        return {
            'enableTransliteration': transliterationConfig.getEnableTransliteration()
        }

    async def serializeVoiceAudioConfig(
        self,
        voiceAudioConfig: GoogleVoiceAudioConfig
    ) -> Dict[str, Any]:
        if not isinstance(voiceAudioConfig, GoogleVoiceAudioConfig):
            raise TypeError(f'voiceAudioConfig argument is malformed: \"{voiceAudioConfig}\"')

        dictionary: Dict[str, Any] = {
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
        elif voiceAudioEncoding is GoogleVoiceAudioEncoding.MP3_64_KBPS:
            return 'MP3_64_KBPS'
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
    ) -> Dict[str, Any]:
        if not isinstance(voiceSelectionParams, GoogleVoiceSelectionParams):
            raise TypeError(f'voiceSelectionParams argument is malformed: \"{voiceSelectionParams}\"')

        return {
            'languageCode': voiceSelectionParams.getLanguageCode(),
            'name': voiceSelectionParams.getName(),
            'ssmlGender': await self.serializeVoiceGender(voiceSelectionParams.getGender())
        }
