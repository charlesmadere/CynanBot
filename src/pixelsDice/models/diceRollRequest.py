from dataclasses import dataclass

from ..listeners.pixelsDiceRollRequestCallback import PixelsDiceRollRequestCallback


@dataclass(frozen = True)
class DiceRollRequest:
    callback: PixelsDiceRollRequestCallback
    twitchChannelId: str
