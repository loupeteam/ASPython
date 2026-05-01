"""Inno Setup (.iss) installer compilation."""
import logging
import subprocess
import uuid


ISCC_PATH = r"C:\Program Files (x86)\Inno Setup 6\iscc"


def generateGUID() -> str:
    return '{{' + str(uuid.uuid4()) + '}'


def compileInstaller(args, GUID: str) -> subprocess.CompletedProcess:
    """Compile an Inno Setup script using ``iscc``.

    ``args`` is the parsed argparse Namespace from ``aspython installer`` (or the legacy
    ``CmdLineCreateInstaller.py``). All assembly of /d-defines from app/sim/user/HMI options
    happens here.
    """
    command = [
        ISCC_PATH,
        args.script,
        f"/O{args.output}",
        f"/dAppName={args.appName}",
        f"/dAppVersion={args.appVersion}",
        f"/dAppPublisher={args.appPublisher}",
        f"/dAppUrl={args.appUrl}",
        f"/dAppGUID={GUID}",
    ]

    if args.simDir:
        command.append("/dIncludeSimulator=yes")
        command.append(f"/dSimulationDirectory={args.simDir}")
    else:
        command.append("/dIncludeSimulator=no")

    if args.userDir:
        command.append("/dIncludeUserPartition=yes")
        command.append(f"/dUserPartitionDirectory={args.userDir}")
        command.append(f"/dJunctionBatchFilename={args.junctionBatch}")
    else:
        command.append("/dIncludeUserPartition=no")

    if args.hmiDir:
        command.append("/dIncludeHmi=yes")
        command.append(f"/dHmiDirectory={args.hmiDir}")
        command.append(f"/dHmiExeName={args.hmiExe}")
    else:
        command.append("/dIncludeHmi=no")

    if getattr(args, 'logLevel', '') != 'DEBUG':
        command.append("/Qp")

    logging.debug(command)
    return subprocess.run(command, encoding="utf-8", errors='replace', shell=True)
