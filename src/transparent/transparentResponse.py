from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True, slots = True)
class TransparentResponse:
    date: datetime
    enPhrase: str
    fnPhrase: str
    langName: str | None
    notes: str | None
    phraseSoundUrl: str | None
    translation: str
    transliteratedSentence: str | None
    transliteratedWord: str | None
    word: str
    wordSoundUrl: str | None
    wordType: str
