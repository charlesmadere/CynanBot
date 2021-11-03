import asyncio
from typing import List

from twitchio.abcs import Messageable

import CynanBotCommon.utils as utils


async def safeSend(
    messageable: Messageable,
    message: str,
    twitchMaxSize: int = 500,
    perMessageMaxSize: int = 450,
    maxMessages: int = 3
):
    if messageable is None:
        raise ValueError(f'messageable argument is malformed: \"{messageable}\"')
    elif not utils.isValidNum(twitchMaxSize):
        raise ValueError(f'twitchMaxSize argument is malformed: \"{twitchMaxSize}\"')
    elif twitchMaxSize < 400 or twitchMaxSize > 500:
        raise ValueError(f'twitchMaxSize argument is out of bounds: {twitchMaxSize}')
    elif not utils.isValidNum(perMessageMaxSize):
        raise ValueError(f'perMessageMaxSize argument is malformed: \"{perMessageMaxSize}\"')
    elif perMessageMaxSize >= twitchMaxSize:
        raise ValueError(f'perMessageMaxSize ({perMessageMaxSize}) is >= twitchMaxSize ({twitchMaxSize})')
    elif perMessageMaxSize < 300:
        raise ValueError(f'perMessageMaxSize is out of bounds: {perMessageMaxSize}')
    elif not utils.isValidNum(maxMessages):
        raise ValueError(f'maxMessages argument is malformed: \"{maxMessages}\"')
    elif maxMessages < 3 or maxMessages > 5:
        raise ValueError(f'maxMessages is out of bounds: {maxMessages}')

    if not utils.isValidStr(message):
        return

    if len(message) < twitchMaxSize:
        await messageable.send(message)
        return

    messages: List[str] = list()
    messages.append(message)

    index = 0

    while index < len(messages):
        m = messages[index]

        if len(m) >= twitchMaxSize:
            spaceIndex = m.rfind(' ')

            while spaceIndex >= perMessageMaxSize:
                spaceIndex = m[0:spaceIndex].rfind(' ')

            if spaceIndex == -1:
                raise RuntimeError(f'This message is insane and can\'t be sent (len is {len(message)}):\n{message}')

            messages[index] = m[0:spaceIndex].strip()
            messages.append(m[spaceIndex:len(m)].strip())

        index = index + 1

    if len(messages) > maxMessages:
        raise RuntimeError(f'This message is just too long and won\'t be sent (len is {len(message)}):\n{message}')

    for m in messages:
        await messageable.send(m)

async def waitThenSend(
    messageable: Messageable,
    delaySeconds: int,
    message: str,
    heartbeat = lambda: True,
    beforeSend = lambda: None,
    afterSend = lambda: None
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
        beforeSend()
        await safeSend(messageable, message)
        afterSend()
