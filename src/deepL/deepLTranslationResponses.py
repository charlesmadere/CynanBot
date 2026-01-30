from dataclasses import dataclass

from frozenlist import FrozenList

from .deepLTranslationResponse import DeepLTranslationResponse


@dataclass(frozen = True, slots = True)
class DeepLTranslationResponses:
    translations: FrozenList[DeepLTranslationResponse]
