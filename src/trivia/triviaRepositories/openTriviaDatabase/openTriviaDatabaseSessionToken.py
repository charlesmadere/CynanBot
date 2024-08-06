from dataclasses import dataclass


@dataclass(frozen = True)
class OpenTriviaDatabaseSessionToken:
    responseCode: int
    responseMessage: str
    token: str
