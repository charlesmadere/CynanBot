from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class SupStreamerBoosterPack:
    message: str
    reply: str
