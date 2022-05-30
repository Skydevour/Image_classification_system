import asyncio
import traceback
from utils import log


async def run_command_shell(command):
    """Run command in subprocess (shell)

    Note:
        This can be used if you wish to execute e.g. "copy"
        on Windows, which can only be executed in the shell.
    """
    process = None
    result = ''
    try:
        # Create subprocess
        process = await asyncio.create_subprocess_shell(
            command, stdout=asyncio.subprocess.PIPE)

        # Status
        #  log.logger.info('Started:' + command, '(pid = ' + str(process.pid) + ')')

        # Wait for the subprocess to finish
        stdout, stderr = await process.communicate()

        # Progress
        if process.returncode == 0:
            log.logger.info('Done: {0} (pid = {1} )'.format(
                command, process.pid))
        else:
            log.logger.error('Failed: {0} (pid = {1} )'.format(
                command, process.pid))

        # Result
        result = stdout.decode().strip()
    except Exception:
        log.logger.error(traceback.print_exc())
    finally:
        if process is not None and process.returncode is None:
            process.terminate()
    # Return stdout
    return result