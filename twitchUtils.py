import asyncio
from typing import List

import CynanBotCommon.utils as utils
from TwitchIO.twitchio.abcs import Messageable


async def safeSend(messageable: Messageable, message: str):
    if messageable is None:
        raise ValueError(f'messageable argument is malformed: \"{messageable}\"')
    elif not utils.isValidStr(message):
        return

    if len(message) < 500:
        await messageable.send(message)
        return

    messages: List[str] = list()
    messages.append(message)

    index = 0

    while index < len(messages):
        m = messages[index]

        if len(m) >= 500:
            spaceIndex = m.rfind(' ')

            while spaceIndex >= 450:
                spaceIndex = m[0:spaceIndex].rfind(' ')

            if spaceIndex == -1:
                raise RuntimeError(f'This message is insane and can\'t be sent (len is {len(message)}):\n{message}')

            messages[index] = m[0:spaceIndex].strip()
            messages.append(m[spaceIndex:len(m)].strip())

        index = index + 1

    if len(messages) > 3:
        raise RuntimeError(f'This message is just too long and won\'t be sent (len is {len(message)}):\n{message}')

    for m in messages:
        await messageable.send(m)

async def waitThenSend(
    messageable: Messageable,
    delaySeconds: int,
    message: str,
    heartbeat = lambda: True
):
    if messageable is None:
        raise ValueError(f'messageable argument is malformed: \"{messageable}\"')
    elif not utils.isValidNum(delaySeconds):
        raise ValueError(f'delaySeconds argument is malformed: \"{delaySeconds}\"')
    elif delaySeconds < 1:
        raise ValueError(f'delaySeconds argument is out of bounds: \"{delaySeconds}\"')
    elif not utils.isValidStr(message):
        return
    elif heartbeat is None:
        raise ValueError(f'heartbeat argument is malformed: \"{heartbeat}\"')

    await asyncio.sleep(delaySeconds)

    if heartbeat():
        await safeSend(messageable, message)
