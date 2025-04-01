from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True)
class GrenadeAttack:
    attackedDateTime: datetime
    attackedUserId: str
