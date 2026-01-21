from dataclasses import dataclass

from ..absTtsProperties import AbsTtsProperties
from ....language.languageEntry import LanguageEntry
from ....tts.models.ttsProvider import TtsProvider


@dataclass(frozen = True, slots = True)
class GoogleTtsProperties(AbsTtsProperties):
    languageEntry: LanguageEntry | None

    @property
    def provider(self) -> TtsProvider:
        return TtsProvider.GOOGLE
