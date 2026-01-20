from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class DiceBluetoothInfo:
    diceAddress: str
    diceName: str
