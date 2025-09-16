from dataclasses import dataclass


@dataclass(frozen = True)
class AnimalPetItemDetails:
    soundDirectory: str
