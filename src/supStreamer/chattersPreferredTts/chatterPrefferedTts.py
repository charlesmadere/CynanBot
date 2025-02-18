from dataclasses import dataclass

from ...language.languageEntry import LanguageEntry
from ...tts.ttsProvider import TtsProvider


@dataclass(frozen = True)
class ChatterPreferredTts:
    languageEntry: LanguageEntry | None
    chatterUserId: str
    twitchChannelId: str
    ttsProvider: TtsProvider
