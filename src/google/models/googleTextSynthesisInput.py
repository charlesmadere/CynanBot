from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class GoogleTextSynthesisInput:
    text: str
