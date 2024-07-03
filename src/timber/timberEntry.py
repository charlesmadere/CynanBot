from dataclasses import dataclass

from ..misc.simpleDateTime import SimpleDateTime


@dataclass(frozen = True)
class TimberEntry():
    exception: Exception | None
    logTime: SimpleDateTime
    msg: str
    tag: str
    traceback: str | None
