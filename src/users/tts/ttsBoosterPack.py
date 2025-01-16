import locale
from dataclasses import dataclass

from ...tts.ttsProvider import TtsProvider


@dataclass(frozen = True)
class TtsBoosterPack:
    cheerAmount: int
    ttsProvider: TtsProvider

    @property
    def cheerAmountStr(self) -> str:
        return locale.format_string("%d", self.cheerAmount, grouping = True)
