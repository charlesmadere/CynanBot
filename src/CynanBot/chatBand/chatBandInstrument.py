from enum import Enum, auto

import CynanBot.misc.utils as utils


class ChatBandInstrument(Enum):

    BASS = auto()
    DRUMS = auto()
    GUITAR = auto()
    MAGIC = auto()
    PIANO = auto()
    SYNTH = auto()
    TRUMPET = auto()
    VIOLIN = auto()
    WHISTLE = auto()

    @classmethod
    def fromStr(cls, text: str):
        if not utils.isValidStr(text):
            raise ValueError(f'text argument is malformed: \"{text}\"')

        text = text.lower()

        if text == 'bass':
            return ChatBandInstrument.BASS
        elif text == 'drums':
            return ChatBandInstrument.DRUMS
        elif text == 'guitar':
            return ChatBandInstrument.GUITAR
        elif text == 'magic':
            return ChatBandInstrument.MAGIC
        elif text == 'piano':
            return ChatBandInstrument.PIANO
        elif text == 'synth':
            return ChatBandInstrument.SYNTH
        elif text == 'trumpet':
            return ChatBandInstrument.TRUMPET
        elif text == 'violin':
            return ChatBandInstrument.VIOLIN
        elif text == 'whistle':
            return ChatBandInstrument.WHISTLE
        else:
            raise ValueError(f'unknown ChatBandInstrument: \"{text}\"')

    def toStr(self) -> str:
        if self is ChatBandInstrument.BASS:
            return 'bass'
        elif self is ChatBandInstrument.DRUMS:
            return 'drums'
        elif self is ChatBandInstrument.GUITAR:
            return 'guitar'
        elif self is ChatBandInstrument.MAGIC:
            return 'magic'
        elif self is ChatBandInstrument.PIANO:
            return 'piano'
        elif self is ChatBandInstrument.SYNTH:
            return 'synth'
        elif self is ChatBandInstrument.TRUMPET:
            return 'trumpet'
        elif self is ChatBandInstrument.VIOLIN:
            return 'violin'
        elif self is ChatBandInstrument.WHISTLE:
            return 'whistle'
        else:
            raise RuntimeError(f'unknown ChatBandInstrument: \"{self}\"')
