from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class AnimalPetItemDetails:
    inventoryMax: int | None
    soundDirectory: str
