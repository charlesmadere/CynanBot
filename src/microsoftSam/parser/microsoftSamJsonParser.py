import re
from typing import Any, Collection, Final, Pattern

from frozendict import frozendict
from frozenlist import FrozenList

from .microsoftSamJsonParserInterface import MicrosoftSamJsonParserInterface
from ..models.microsoftSamVoice import MicrosoftSamVoice
from ...misc import utils as utils


class MicrosoftSamJsonParser(MicrosoftSamJsonParserInterface):

    def __init__(self):
        self.__voiceRegExes: Final[frozendict[MicrosoftSamVoice, Collection[Pattern]]] = self.__buildVoiceRegExes()

    def __buildVoiceRegExes(self) -> frozendict[MicrosoftSamVoice, Collection[Pattern]]:
        adultFemale1: FrozenList[Pattern] = FrozenList()
        adultFemale1.append(re.compile(r'^\s*adult(?:\s+|_|-)?female(?:\s+|_|-)?1?\s*$', re.IGNORECASE))
        adultFemale1.freeze()

        adultFemale2: FrozenList[Pattern] = FrozenList()
        adultFemale2.append(re.compile(r'^\s*adult(?:\s+|_|-)?female(?:\s+|_|-)?2\s*$', re.IGNORECASE))
        adultFemale2.freeze()

        adultFemaleWhisper: FrozenList[Pattern] = FrozenList()
        adultFemaleWhisper.append(re.compile(r'^\s*adult(?:\s+|_|-)?female(?:\s+|_|-)?whisper\s*$', re.IGNORECASE))
        adultFemaleWhisper.freeze()

        adultMale1: FrozenList[Pattern] = FrozenList()
        adultMale1.append(re.compile(r'^\s*adult(?:\s+|_|-)?male(?:\s+|_|-)?1?\s*$', re.IGNORECASE))
        adultMale1.freeze()

        adultMale2: FrozenList[Pattern] = FrozenList()
        adultMale2.append(re.compile(r'^\s*adult(?:\s+|_|-)?male(?:\s+|_|-)?2\s*$', re.IGNORECASE))
        adultMale2.freeze()

        adultMale3: FrozenList[Pattern] = FrozenList()
        adultMale3.append(re.compile(r'^\s*adult(?:\s+|_|-)?male(?:\s+|_|-)?3\s*$', re.IGNORECASE))
        adultMale3.freeze()

        adultMale4: FrozenList[Pattern] = FrozenList()
        adultMale4.append(re.compile(r'^\s*adult(?:\s+|_|-)?male(?:\s+|_|-)?4\s*$', re.IGNORECASE))
        adultMale4.freeze()

        adultMale5: FrozenList[Pattern] = FrozenList()
        adultMale5.append(re.compile(r'^\s*adult(?:\s+|_|-)?male(?:\s+|_|-)?5\s*$', re.IGNORECASE))
        adultMale5.freeze()

        adultMale6: FrozenList[Pattern] = FrozenList()
        adultMale6.append(re.compile(r'^\s*adult(?:\s+|_|-)?male(?:\s+|_|-)?6\s*$', re.IGNORECASE))
        adultMale6.freeze()

        adultMale7: FrozenList[Pattern] = FrozenList()
        adultMale7.append(re.compile(r'^\s*adult(?:\s+|_|-)?male(?:\s+|_|-)?7\s*$', re.IGNORECASE))
        adultMale7.freeze()

        adultMale8: FrozenList[Pattern] = FrozenList()
        adultMale8.append(re.compile(r'^\s*adult(?:\s+|_|-)?male(?:\s+|_|-)?8\s*$', re.IGNORECASE))
        adultMale8.freeze()

        adultMaleWhisper: FrozenList[Pattern] = FrozenList()
        adultMaleWhisper.append(re.compile(r'^\s*adult(?:\s+|_|-)?male(?:\s+|_|-)?whisper\s*$', re.IGNORECASE))
        adultMaleWhisper.freeze()

        bonziBuddy: FrozenList[Pattern] = FrozenList()
        bonziBuddy.append(re.compile(r'^\s*bonzi(?:\s+|_|-)?buddy\s*$', re.IGNORECASE))
        bonziBuddy.freeze()

        mary: FrozenList[Pattern] = FrozenList()
        mary.append(re.compile(r'^\s*mary\s*$', re.IGNORECASE))
        mary.freeze()

        maryHall: FrozenList[Pattern] = FrozenList()
        maryHall.append(re.compile(r'^\s*mary(?:\s+|_|-)?hall\s*$', re.IGNORECASE))
        maryHall.freeze()

        marySpace: FrozenList[Pattern] = FrozenList()
        marySpace.append(re.compile(r'^\s*mary(?:\s+|_|-)?space\s*$', re.IGNORECASE))
        marySpace.append(re.compile(r'^\s*mary(?:\s+|_|-)?in(?:\s+|_|-)?space\s*$', re.IGNORECASE))
        marySpace.freeze()

        maryStadium: FrozenList[Pattern] = FrozenList()
        maryStadium.append(re.compile(r'^\s*mary(?:\s+|_|-)?stadium\s*$', re.IGNORECASE))
        maryStadium.append(re.compile(r'^\s*mary(?:\s+|_|-)?in(?:\s+|_|-)?stadium\s*$', re.IGNORECASE))
        maryStadium.freeze()

        maryTelephone: FrozenList[Pattern] = FrozenList()
        maryTelephone.append(re.compile(r'^\s*mary(?:\s+|_|-)?(tele)?phone\s*$', re.IGNORECASE))
        maryTelephone.freeze()

        mike: FrozenList[Pattern] = FrozenList()
        mike.append(re.compile(r'^\s*mike\s*$', re.IGNORECASE))
        mike.freeze()

        mikeHall: FrozenList[Pattern] = FrozenList()
        mikeHall.append(re.compile(r'^\s*mike(?:\s+|_|-)?hall\s*$', re.IGNORECASE))
        mikeHall.freeze()

        mikeSpace: FrozenList[Pattern] = FrozenList()
        mikeSpace.append(re.compile(r'^\s*mike(?:\s+|_|-)?space\s*$', re.IGNORECASE))
        mikeSpace.append(re.compile(r'^\s*mike(?:\s+|_|-)?in(?:\s+|_|-)?space\s*$', re.IGNORECASE))
        mikeSpace.freeze()

        mikeStadium: FrozenList[Pattern] = FrozenList()
        mikeStadium.append(re.compile(r'^\s*mike(?:\s+|_|-)?stadium\s*$', re.IGNORECASE))
        mikeStadium.append(re.compile(r'^\s*mike(?:\s+|_|-)?in(?:\s+|_|-)?stadium\s*$', re.IGNORECASE))
        mikeStadium.freeze()

        mikeTelephone: FrozenList[Pattern] = FrozenList()
        mikeTelephone.append(re.compile(r'^\s*mike(?:\s+|_|-)?(tele)?phone\s*$', re.IGNORECASE))
        mikeTelephone.freeze()

        robo1: FrozenList[Pattern] = FrozenList()
        robo1.append(re.compile(r'^\s*robo(?:\s+|_|-)?1?\s*$', re.IGNORECASE))
        robo1.freeze()

        robo2: FrozenList[Pattern] = FrozenList()
        robo2.append(re.compile(r'^\s*robo(?:\s+|_|-)?2\s*$', re.IGNORECASE))
        robo2.freeze()

        robo3: FrozenList[Pattern] = FrozenList()
        robo3.append(re.compile(r'^\s*robo(?:\s+|_|-)?3\s*$', re.IGNORECASE))
        robo3.freeze()

        robo4: FrozenList[Pattern] = FrozenList()
        robo4.append(re.compile(r'^\s*robo(?:\s+|_|-)?4\s*$', re.IGNORECASE))
        robo4.freeze()

        robo5: FrozenList[Pattern] = FrozenList()
        robo5.append(re.compile(r'^\s*robo(?:\s+|_|-)?5\s*$', re.IGNORECASE))
        robo5.freeze()

        robo6: FrozenList[Pattern] = FrozenList()
        robo6.append(re.compile(r'^\s*robo(?:\s+|_|-)?6\s*$', re.IGNORECASE))
        robo6.freeze()

        sam: FrozenList[Pattern] = FrozenList()
        sam.append(re.compile(r'^\s*sam\s*$', re.IGNORECASE))
        sam.freeze()

        return frozendict({
            MicrosoftSamVoice.ADULT_FEMALE_1: adultFemale1,
            MicrosoftSamVoice.ADULT_FEMALE_2: adultFemale2,
            MicrosoftSamVoice.ADULT_FEMALE_WHISPER: adultFemaleWhisper,
            MicrosoftSamVoice.ADULT_MALE_1: adultMale1,
            MicrosoftSamVoice.ADULT_MALE_2: adultMale2,
            MicrosoftSamVoice.ADULT_MALE_3: adultMale3,
            MicrosoftSamVoice.ADULT_MALE_4: adultMale4,
            MicrosoftSamVoice.ADULT_MALE_5: adultMale5,
            MicrosoftSamVoice.ADULT_MALE_6: adultMale6,
            MicrosoftSamVoice.ADULT_MALE_7: adultMale7,
            MicrosoftSamVoice.ADULT_MALE_8: adultMale8,
            MicrosoftSamVoice.ADULT_MALE_WHISPER: adultMaleWhisper,
            MicrosoftSamVoice.BONZI_BUDDY: bonziBuddy,
            MicrosoftSamVoice.MARY: mary,
            MicrosoftSamVoice.MARY_HALL: maryHall,
            MicrosoftSamVoice.MARY_SPACE: marySpace,
            MicrosoftSamVoice.MARY_STADIUM: maryStadium,
            MicrosoftSamVoice.MARY_TELEPHONE: maryTelephone,
            MicrosoftSamVoice.MIKE: mike,
            MicrosoftSamVoice.MIKE_HALL: mikeHall,
            MicrosoftSamVoice.MIKE_SPACE: mikeSpace,
            MicrosoftSamVoice.MIKE_STADIUM: mikeStadium,
            MicrosoftSamVoice.MIKE_TELEPHONE: mikeTelephone,
            MicrosoftSamVoice.ROBO_1: robo1,
            MicrosoftSamVoice.ROBO_2: robo2,
            MicrosoftSamVoice.ROBO_3: robo3,
            MicrosoftSamVoice.ROBO_4: robo4,
            MicrosoftSamVoice.ROBO_5: robo5,
            MicrosoftSamVoice.ROBO_6: robo6,
            MicrosoftSamVoice.SAM: sam
        })

    async def parseVoice(
        self,
        string: str | Any | None
    ) -> MicrosoftSamVoice | None:
        if not utils.isValidStr(string):
            return None

        for microsoftSamVoice, voiceRegExes in self.__voiceRegExes.items():
            for voiceRegEx in voiceRegExes:
                if voiceRegEx.fullmatch(string) is not None:
                    return microsoftSamVoice

        return None

    async def requireVoice(
        self,
        string: str | Any | None
    ) -> MicrosoftSamVoice:
        result = await self.parseVoice(string)

        if result is None:
            raise ValueError(f'Unable to parse \"{string}\" into MicrosoftSamVoice value!')

        return result

    async def serializeVoice(
        self,
        voice: MicrosoftSamVoice
    ) -> str:
        if not isinstance(voice, MicrosoftSamVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        match voice:
            case MicrosoftSamVoice.ADULT_FEMALE_1: return 'adult_female_1'
            case MicrosoftSamVoice.ADULT_FEMALE_2: return 'adult_female_2'
            case MicrosoftSamVoice.ADULT_FEMALE_WHISPER: return 'adult_female_whisper'
            case MicrosoftSamVoice.ADULT_MALE_1: return 'adult_male_1'
            case MicrosoftSamVoice.ADULT_MALE_2: return 'adult_male_2'
            case MicrosoftSamVoice.ADULT_MALE_3: return 'adult_male_3'
            case MicrosoftSamVoice.ADULT_MALE_4: return 'adult_male_4'
            case MicrosoftSamVoice.ADULT_MALE_5: return 'adult_male_5'
            case MicrosoftSamVoice.ADULT_MALE_6: return 'adult_male_6'
            case MicrosoftSamVoice.ADULT_MALE_7: return 'adult_male_7'
            case MicrosoftSamVoice.ADULT_MALE_8: return 'adult_male_8'
            case MicrosoftSamVoice.ADULT_MALE_WHISPER: return 'adult_male_whisper'
            case MicrosoftSamVoice.BONZI_BUDDY: return 'bonzi_buddy'
            case MicrosoftSamVoice.MARY: return 'mary'
            case MicrosoftSamVoice.MARY_HALL: return 'mary_hall'
            case MicrosoftSamVoice.MARY_SPACE: return 'mary_space'
            case MicrosoftSamVoice.MARY_STADIUM: return 'mary_stadium'
            case MicrosoftSamVoice.MARY_TELEPHONE: return 'mary_telephone'
            case MicrosoftSamVoice.MIKE: return 'mike'
            case MicrosoftSamVoice.MIKE_HALL: return 'mike_hall'
            case MicrosoftSamVoice.MIKE_SPACE: return 'mike_space'
            case MicrosoftSamVoice.MIKE_STADIUM: return 'mike_stadium'
            case MicrosoftSamVoice.MIKE_TELEPHONE: return 'mike_telephone'
            case MicrosoftSamVoice.ROBO_1: return 'robo_1'
            case MicrosoftSamVoice.ROBO_2: return 'robo_2'
            case MicrosoftSamVoice.ROBO_3: return 'robo_3'
            case MicrosoftSamVoice.ROBO_4: return 'robo_4'
            case MicrosoftSamVoice.ROBO_5: return 'robo_5'
            case MicrosoftSamVoice.ROBO_6: return 'robo_6'
            case MicrosoftSamVoice.SAM: return 'sam'
            case _: raise RuntimeError(f'Encountered unknown MicrosoftSamVoice value: \"{voice}\"')
