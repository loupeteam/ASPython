"""B&R AS upgrade installer helpers."""
import logging
import subprocess


def installBRUpgrade(upgrade: str, brPath: str, asPath: str) -> int:
    commandLine = [upgrade, '-G=', '"' + brPath + '"']
    if brPath in asPath:
        commandLine.extend(['-V=', '"' + asPath + '"'])
    else:
        commandLine.extend(['-V=', '"' + brPath + '\\' + asPath + '"'])
    commandLine.append('-R')

    logging.info('Started installing upgrade ' + upgrade)
    logging.info(commandLine)

    process = subprocess.run(' '.join(commandLine), shell=False, capture_output=True)
    if process.returncode == 0:
        logging.info('Finished install upgrade ' + upgrade)
    else:
        logging.error('Error while installing upgrade ' + upgrade
                      + ' (return code = ' + str(process.returncode) + ')')
        logging.debug('stderr: ' + str(process.stderr))
        logging.debug('stdout: ' + str(process.stdout))

    return process.returncode
