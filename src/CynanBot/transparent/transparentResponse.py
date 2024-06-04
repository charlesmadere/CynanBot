from dataclasses import dataclass
from datetime import datetime

from CynanBot.language.languageEntry import LanguageEntry


@dataclass(frozen = True)
class TransparentResponse():
    date: datetime
    enPhrase: str
    fnPhrase: str
    notes: str | None
    phraseSoundUrl: str | None
    translation: str
    transliteratedSentence: str | None
    transliteratedWord: str | None
    word: str
    wordSoundUrl: str | None
    wordType: str
