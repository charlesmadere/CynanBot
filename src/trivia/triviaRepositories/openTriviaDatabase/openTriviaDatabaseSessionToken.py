from dataclasses import dataclass

from .openTriviaDatabaseResponseCode import OpenTriviaDatabaseResponseCode


@dataclass(frozen = True, slots = True)
class OpenTriviaDatabaseSessionToken:
    responseCode: OpenTriviaDatabaseResponseCode
    responseMessage: str | None
    token: str
