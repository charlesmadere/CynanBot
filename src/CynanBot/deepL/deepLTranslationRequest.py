from dataclasses import dataclass

from CynanBot.language.languageEntry import LanguageEntry


@dataclass(frozen = True)
class DeepLTranslationRequest():
    targetLanguage: LanguageEntry
    text: str
