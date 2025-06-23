from dataclasses import dataclass

from .absGoogleTextSynthesisInput import AbsGoogleTextSynthesisInput


@dataclass(frozen = True)
class GoogleTextSynthesisInput(AbsGoogleTextSynthesisInput):
    text: str
