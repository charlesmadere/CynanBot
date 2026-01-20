from dataclasses import dataclass

from ..language.languageEntry import LanguageEntry


@dataclass(frozen = True, slots = True)
class DeepLTranslationRequest:
    targetLanguage: LanguageEntry
    text: str
