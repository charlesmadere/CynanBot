from dataclasses import dataclass

from .absGoogleTextSynthesisInput import AbsGoogleTextSynthesisInput
from .googleMultiSpeakerMarkup import GoogleMultiSpeakerMarkup


@dataclass(frozen = True)
class GoogleMultiSpeakerTextSynthesisInput(AbsGoogleTextSynthesisInput):
    multiSpeakerMarkup: GoogleMultiSpeakerMarkup
