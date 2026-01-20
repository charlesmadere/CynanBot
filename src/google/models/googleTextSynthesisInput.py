from dataclasses import dataclass

from .absGoogleTextSynthesisInput import AbsGoogleTextSynthesisInput


@dataclass(frozen = True, slots = True)
class GoogleTextSynthesisInput(AbsGoogleTextSynthesisInput):
    text: str
