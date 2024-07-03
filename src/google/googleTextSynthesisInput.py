from dataclasses import dataclass


@dataclass(frozen = True)
class GoogleTextSynthesisInput():
    text: str
