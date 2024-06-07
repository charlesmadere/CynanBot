from dataclasses import dataclass


@dataclass(frozen = True)
class JishoAttribution():
    dbpedia: bool
    jmdict: bool
    jmnedict: bool
