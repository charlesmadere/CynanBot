from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.deepL.deepLJsonMapperInterface import DeepLJsonMapperInterface
from CynanBot.deepL.deepLTranslationRequest import DeepLTranslationRequest
from CynanBot.deepL.deepLTranslationResponse import DeepLTranslationResponse
from CynanBot.deepL.deepLTranslationResponses import DeepLTranslationResponses
from CynanBot.timber.timberInterface import TimberInterface


class DeepLJsonMapper(DeepLJsonMapperInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

    async def parseTranslationResponse(
        self,
        jsonContents: dict[str, Any] | None
    ) -> DeepLTranslationResponse | None:
        if jsonContents is None or len(jsonContents) == 0:
            return None

        if not utils.isValidStr(jsonContents.get('text')):
            return None

        text = utils.getStrFromDict(jsonContents, 'text')

        detectedSourceLanguage: str | None = None
        if 'detected_source_language' in jsonContents and utils.isValidStr(jsonContents.get('detected_source_language')):
            detectedSourceLanguage = utils.getStrFromDict(jsonContents, 'detected_source_language')

        return DeepLTranslationResponse(
            detectedSourceLanguage = detectedSourceLanguage,
            text = text
        )

    async def parseTranslationResponses(
        self,
        jsonContents: dict[str, Any] | None
    ) -> DeepLTranslationResponses | None:
        if jsonContents is None or len(jsonContents) == 0:
            return None

        translationsJson: list[dict[str, Any]] | None = jsonContents.get('translations')
        if not isinstance(translationsJson, list) or len(translationsJson) == 0:
            return None

        translations: list[DeepLTranslationResponse] = list()

        for translationJson in translationsJson:
            translationResponse = await self.parseTranslationResponse(translationJson)

            if translationResponse is not None:
                translations.append(translationResponse)

        if len(translations) == 0:
            return None

        return DeepLTranslationResponses(
            translations = translations
        )

    async def serializeTranslationRequest(
        self,
        request: DeepLTranslationRequest
    ) -> dict[str, Any]:
        if not isinstance(request, DeepLTranslationRequest):
            raise TypeError(f'request argument is malformed: \"{request}\"')

        return {
            'target_lang': request.getTargetLanguage().requireIso6391Code(),
            'text': [ request.getText() ]
        }
