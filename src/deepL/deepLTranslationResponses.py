from dataclasses import dataclass

from .deepLTranslationResponse import DeepLTranslationResponse


@dataclass(frozen = True)
class DeepLTranslationResponses:
    translations: list[DeepLTranslationResponse] | None = None
