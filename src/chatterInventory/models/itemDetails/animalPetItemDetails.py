from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class AnimalPetItemDetails:
    soundDirectory: str
