import locale
from dataclasses import dataclass

from ...tts.models.ttsProvider import TtsProvider


@dataclass(frozen = True, slots = True)
class TtsBoosterPack:
    isEnabled: bool
    cheerAmount: int
    ttsProvider: TtsProvider

    @property
    def cheerAmountStr(self) -> str:
        return locale.format_string("%d", self.cheerAmount, grouping = True)
