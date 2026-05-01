"""Build orchestration: invoking ``BR.AS.Build.exe`` for AS projects."""
import logging
import os.path
import re
import subprocess
from typing import Union

from .returncodes import ASReturnCodes


def ASProjetGetConfigs(project: str):
    if os.path.isfile(project):
        project = os.path.split(project)[0]
    project = os.path.join(project, 'Physical')
    return [d for d in os.listdir(project) if os.path.isdir(os.path.join(project, d))]


def batchBuildAsProject(
    project,
    ASPath: str,
    configurations=None,
    buildMode: str = 'Build',
    buildRUCPackage: bool = True,
    tempPath: str = '',
    logPath: str = '',
    binaryPath: str = '',
    simulation: bool = False,
    additionalArg: Union[str, list, tuple, None] = None,
) -> subprocess.CompletedProcess:
    if configurations is None:
        configurations = []
    completedProcess = None
    for config in configurations:
        completedProcess = buildASProject(
            project, ASPath,
            configuration=config, buildMode=buildMode, buildRUCPackage=buildRUCPackage,
            tempPath=tempPath, logPath=logPath, binaryPath=binaryPath,
            simulation=simulation, additionalArg=additionalArg,
        )
        if completedProcess.returncode > ASReturnCodes["Warnings"]:
            logging.info(f'Build for configuration {config} has completed with errors, see DEBUG logging for details')
            return completedProcess
        logging.info(f'Build for configuration {config} has completed without errors, see DEBUG logging for details')
    return completedProcess


def buildASProject(
    project,
    ASPath: str,
    configuration: str = '',
    buildMode: str = 'Build',
    buildRUCPackage: bool = True,
    tempPath: str = '',
    binaryPath: str = '',
    logPath: str = '',
    simulation: bool = False,
    additionalArg: Union[str, list, tuple, None] = None,
) -> subprocess.CompletedProcess:
    commandLine = [ASPath, '"' + os.path.abspath(project) + '"']

    if configuration:
        commandLine.extend(['-c', configuration])

    if buildMode:
        commandLine.extend(['-buildMode', buildMode])
        if buildMode.capitalize() == 'Rebuild':
            commandLine.append('-all')

    if tempPath:
        commandLine.extend(['-t', tempPath])

    if binaryPath:
        commandLine.extend(['-o', binaryPath])

    if simulation:
        commandLine.append('-simulation')

    if buildRUCPackage:
        commandLine.append('-buildRUCPackage')

    if additionalArg:
        if isinstance(additionalArg, str):
            commandLine.append(additionalArg)
        elif isinstance(additionalArg, (list, tuple)):
            commandLine.extend(additionalArg)

    logging.info(f'Starting build for configuration {configuration}...')
    logging.debug(commandLine)
    process = subprocess.Popen(commandLine, stdout=subprocess.PIPE, encoding="utf-8", errors='replace')

    log_file = os.path.join(logPath, "build.log")
    logging.info("Recording build log here: " + log_file)

    with open(log_file, "w", encoding='utf-8') as f:
        while process.returncode is None:
            raw = process.stdout.readline()
            data = raw.rstrip()
            f.write(raw)
            if data != "":
                warningMatch = re.search('warning [0-9]*:', data)
                errorMatch = re.search('error [0-9]*:', data)
                if warningMatch is not None:
                    logging.warning("\033[32m" + data + "\033[0m")
                elif errorMatch is not None:
                    logging.error("\033[31m" + data + "\033[0m")
                else:
                    logging.debug(data)
            process.poll()

    return process
