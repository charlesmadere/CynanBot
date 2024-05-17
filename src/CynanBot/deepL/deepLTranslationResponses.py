from dataclasses import dataclass

from CynanBot.deepL.deepLTranslationResponse import DeepLTranslationResponse


@dataclass(frozen = True)
class DeepLTranslationResponses():
    translations: list[DeepLTranslationResponse] | None = None
