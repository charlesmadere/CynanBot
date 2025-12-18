from dataclasses import dataclass
from typing import Awaitable, Callable

from .diceRollResult import DiceRollResult


@dataclass(frozen = True)
class DiceRollRequest:
    callback: Callable[[DiceRollResult], Awaitable[None]]
    twitchChannelId: str
