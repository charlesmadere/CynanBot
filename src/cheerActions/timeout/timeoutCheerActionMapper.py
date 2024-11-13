from ..cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from ...timeout.timeoutActionData import TimeoutActionData


class TimeoutCheerActionMapper:

    async def toTimeoutActionDataStreamStatusRequirement(
        self,
        streamStatusRequirement: CheerActionStreamStatusRequirement
    ) -> TimeoutActionData.StreamStatusRequirement:
        if not isinstance(streamStatusRequirement, CheerActionStreamStatusRequirement):
            raise TypeError(f'streamStatusRequirement argument is malformed: \"{streamStatusRequirement}\"')

        match streamStatusRequirement:
            case CheerActionStreamStatusRequirement.ANY:
                return TimeoutActionData.StreamStatusRequirement.ANY

            case CheerActionStreamStatusRequirement.OFFLINE:
                return TimeoutActionData.StreamStatusRequirement.OFFLINE

            case CheerActionStreamStatusRequirement.ONLINE:
                return TimeoutActionData.StreamStatusRequirement.ONLINE

            case _:
                raise ValueError(f'unknown CheerActionStreamStatusRequirement value: \"{streamStatusRequirement}\"')
