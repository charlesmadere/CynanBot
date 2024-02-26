import traceback
from typing import Any, Dict, List, Optional

import CynanBot.misc.utils as utils
from CynanBot.google.googleJsonMapperInterface import GoogleJsonMapperInterface
from CynanBot.google.googleTranslateTextGlossaryConfig import \
    GoogleTranslateTextGlossaryConfig
from CynanBot.google.googleTranslateTextResponse import \
    GoogleTranslateTextResponse
from CynanBot.google.googleTranslation import GoogleTranslation
from CynanBot.timber.timberInterface import TimberInterface


class GoogleJsonMapper(GoogleJsonMapperInterface):

    def __init__(
        self,
        timber: TimberInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

    async def parseTranslateTextGlossaryConfig(
        self,
        jsonContents: Optional[Dict[str, Any]]
    ) -> Optional[GoogleTranslateTextGlossaryConfig]:
        if jsonContents is None or len(jsonContents) == 0:
            return None

        ignoreCase = utils.getBoolFromDict(jsonContents, 'ignoreCase')
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
            exception = ValueError(f'Failed to parse jsonContents into a glossary config! ({jsonContents=}) ({glossaryConfig=})')
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
