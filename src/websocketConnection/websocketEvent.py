from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .websocketEventType import WebsocketEventType


@dataclass(frozen = True, slots = True)
class WebsocketEvent:
    eventTime: datetime
    eventData: dict[str, Any]
    eventType: WebsocketEventType
