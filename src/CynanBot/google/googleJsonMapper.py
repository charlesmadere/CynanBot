import traceback
from typing import Any, Dict, List, Optional

import CynanBot.misc.utils as utils
from CynanBot.google.googleJsonMapperInterface import GoogleJsonMapperInterface
from CynanBot.google.googleTextSynthesisResponse import \
    GoogleTextSynthesisResponse
from CynanBot.google.googleTranslateTextGlossaryConfig import \
    GoogleTranslateTextGlossaryConfig
from CynanBot.google.googleTranslateTextResponse import \
    GoogleTranslateTextResponse
from CynanBot.google.googleTranslation import GoogleTranslation
from CynanBot.google.googleVoiceAudioConfig import GoogleVoiceAudioConfig
from CynanBot.google.googleVoiceAudioEncoding import GoogleVoiceAudioEncoding
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
            return None
