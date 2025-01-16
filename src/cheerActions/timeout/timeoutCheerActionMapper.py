from ..cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from ...timeout.timeoutStreamStatusRequirement import TimeoutStreamStatusRequirement


class TimeoutCheerActionMapper:

    async def toTimeoutActionDataStreamStatusRequirement(
        self,
        streamStatusRequirement: CheerActionStreamStatusRequirement
    ) -> TimeoutStreamStatusRequirement:
        if not isinstance(streamStatusRequirement, CheerActionStreamStatusRequirement):
            raise TypeError(f'streamStatusRequirement argument is malformed: \"{streamStatusRequirement}\"')

        match streamStatusRequirement:
            case CheerActionStreamStatusRequirement.ANY:
                return TimeoutStreamStatusRequirement.ANY

            case CheerActionStreamStatusRequirement.OFFLINE:
                return TimeoutStreamStatusRequirement.OFFLINE

            case CheerActionStreamStatusRequirement.ONLINE:
                return TimeoutStreamStatusRequirement.ONLINE

            case _:
                raise ValueError(f'unknown CheerActionStreamStatusRequirement value: \"{streamStatusRequirement}\"')
