from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class EccoConstants:
    baseUrl: str = 'https://www.eccothedolphin.com'
    websiteUrl: str = f'{baseUrl}/en'
