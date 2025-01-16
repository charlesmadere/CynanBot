from dataclasses import dataclass

from .chatBandInstrument import ChatBandInstrument


@dataclass(frozen = True)
class ChatBandMember:
    isEnabled: bool
    instrument: ChatBandInstrument
    author: str
    keyPhrase: str
