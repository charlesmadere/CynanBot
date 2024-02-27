from enum import Enum, auto


class GoogleScope(Enum):

    CLOUD_TEXT_TO_SPEECH = auto()
    CLOUD_TRANSLATION = auto()

    def toScopeStr(self) -> str:
        if self is GoogleScope.CLOUD_TEXT_TO_SPEECH:
            return 'https://www.googleapis.com/auth/cloud-platform'
        elif self is GoogleScope.CLOUD_TRANSLATION:
            return 'https://www.googleapis.com/auth/cloud-translation'
        else:
            raise RuntimeError(f'unknown GoogleScope: \"{self}\"')
