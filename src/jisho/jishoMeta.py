from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class JishoMeta:
    status: int
