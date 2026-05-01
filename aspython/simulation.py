"""ARsim structure creation via ``PVITransfer.exe``."""
import logging
import os.path
import subprocess

from .paths import getPVITransferPath
from .returncodes import PVIReturnCodeText


def CreateARSimStructure(RUCPackage: str, destination: str, version: str, startSim: bool = False):
    logging.info(f'Creating ARSim structure at {destination}')
    RUCPath = os.path.dirname(RUCPackage)
    RUCPil = os.path.join(RUCPath, 'CreateARSim.pil')
    with open(RUCPil, 'w+') as f:
        f.write(f'CreateARsimStructure "{RUCPackage}", "{destination}", "Start={int(startSim)}"\n')
        if startSim:
            f.write('Connection "/IF=TCPIP /SA=1", "/DA=2 /DAIP=127.0.0.1 /REPO=11160", "WT=120"')

    arguments = [
        os.path.join(getPVITransferPath(version), 'PVITransfer.exe'),
        '-silent',
        RUCPil,
    ]
    logging.info('PVI version: ' + version)
    logging.debug(arguments)
    process = subprocess.run(arguments)

    logging.debug(process)
    if process.returncode == 0:
        logging.debug('ARSim created')
        if startSim:
            # silent / autoclose mode does not support starting arsim, so launch it ourselves.
            subprocess.Popen(
                os.path.join(destination, 'ar000loader.exe'),
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                creationflags=0x00000008,
            )
    else:
        logging.debug(
            f'Error in creating ARSimStructure code {process.returncode}: '
            f'{PVIReturnCodeText.get(process.returncode, "Unknown")}'
        )
    return process
