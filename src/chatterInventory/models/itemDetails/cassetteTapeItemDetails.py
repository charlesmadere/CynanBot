from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class CassetteTapeItemDetails:
    inventoryMax: int | None
