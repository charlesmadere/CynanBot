from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class JishoAttribution:
    dbpedia: bool | None = None
    jmdict: bool | None = None
    jmnedict: bool | None = None
    dbpediaUrl: str | None = None
    jmdictUrl: str | None = None
    jmnedictUrl: str | None = None
