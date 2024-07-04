from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen = True)
class WebsocketEvent:
    eventTime: datetime
    eventData: dict[str, Any]
