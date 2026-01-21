from dataclasses import dataclass
from datetime import datetime

from .triviaQuestionType import TriviaQuestionType
from .triviaSource import TriviaSource


@dataclass(frozen = True, slots = True)
class TriviaQuestionReference:
    dateTime: datetime
    emote: str
    triviaId: str
    twitchChannel: str
    twitchChannelId: str
    triviaSource: TriviaSource
    triviaType: TriviaQuestionType
