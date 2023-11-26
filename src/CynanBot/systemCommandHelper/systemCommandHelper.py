import asyncio
from asyncio import CancelledError as AsyncioCancelledError
from asyncio import TimeoutError as AsyncioTimeoutError
from asyncio.subprocess import Process
from typing import ByteString, Optional, Tuple

import misc.utils as utils
import psutil
from systemCommandHelper.systemCommandHelperInterface import \
    SystemCommandHelperInterface
from timber.timberInterface import TimberInterface


class SystemCommandHelper(SystemCommandHelperInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

    async def executeCommand(self, command: str, timeoutSeconds: float = 10):
        if not utils.isValidStr(command):
            self.__timber.log('SystemCommandHelper', f'Received malformed command argument: \"{command}\"')
            return
        elif not utils.isValidNum(timeoutSeconds):
            raise ValueError(f'timeoutSeconds argument is malformed: \"{timeoutSeconds}\"')
        elif timeoutSeconds < 3 or timeoutSeconds > utils.getIntMaxSafeSize():
            raise ValueError(f'timeoutSeconds argument is out of bounds: {timeoutSeconds}')

        process: Optional[Process] = None
        outputTuple: Optional[Tuple[ByteString]] = None
        exception: Optional[Exception] = None

        try:
            process = await asyncio.create_subprocess_shell(
                cmd = command,
                stdout = asyncio.subprocess.PIPE,
                stderr = asyncio.subprocess.PIPE
            )

            outputTuple = await asyncio.wait_for(
                fut = process.communicate(),
                timeout = timeoutSeconds
            )
        except (AsyncioCancelledError, Exception) as e:
            exception = e

        if isinstance(exception, AsyncioTimeoutError) or isinstance(exception, AsyncioCancelledError) or isinstance(exception, TimeoutError):
            await self.__killProcess(process)

        outputString: Optional[str] = None

        if outputTuple is not None and len(outputTuple) >= 2:
            outputString = outputTuple[1].decode('utf-8').strip()

        self.__timber.log('SystemCommandHelper', f'Ran system command ({command}) ({outputString=}) ({exception=})')

    async def __killProcess(self, process: Optional[Process]):
        if process is None:
            return
        elif not isinstance(process, Process):
            raise ValueError(f'process argument is malformed: \"{process}\"')
        elif process.returncode is not None:
            return

        parent = psutil.Process(process.pid)

        for child in parent.children(recursive = True): 
            child.terminate()

        parent.terminate()
