from dataclasses import dataclass

from .openTriviaDatabaseResponseCode import OpenTriviaDatabaseResponseCode


@dataclass(frozen = True)
class OpenTriviaDatabaseSessionToken:
    responseCode: OpenTriviaDatabaseResponseCode
    responseMessage: str | None
    token: str
