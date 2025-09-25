from dataclasses import dataclass


@dataclass(frozen = True)
class DiceBluetoothInfo:
    diceAddress: str
    diceName: str
