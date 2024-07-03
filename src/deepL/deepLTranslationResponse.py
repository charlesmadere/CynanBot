from dataclasses import dataclass

from ..language.languageEntry import LanguageEntry


@dataclass(frozen = True)
class DeepLTranslationResponse():
    detectedSourceLanguage: LanguageEntry | None
    text: str
