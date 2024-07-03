from dataclasses import dataclass
from datetime import datetime

from .configuration.twitchMessageable import TwitchMessageable


@dataclass(frozen = True)
class OutboundMessage():
    delayUntilTime: datetime
    message: str
    messageable: TwitchMessageable
