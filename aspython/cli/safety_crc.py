"""``aspython safety-crc`` subcommand."""
import os.path
import sys

from .. import Project


SUBCOMMAND = 'safety-crc'
HELP = 'Retrieve the CRC value of a B&R Safe Application.'


def add_subparser(subparsers):
    p = subparsers.add_parser(SUBCOMMAND, help=HELP, description=HELP)
    p.add_argument('project', type=str, help='Path to AS project')
    p.add_argument('-c', '--configuration', nargs='+', type=str, required=True,
                   help='AS configuration(s)')
    p.add_argument('-sa', '--safeApp', type=str, required=True,
                   help='Location of the safe application binaries')
    p.set_defaults(func=run)
    return p


def run(args) -> int:
    project = Project(args.project)

    configurationDirectory = os.path.join(project.dirPath, 'Physical', args.configuration[0])
    plcDirectory = [name for name in os.listdir(configurationDirectory)
                    if os.path.isdir(os.path.join(configurationDirectory, name))]

    splitSafetyApp = args.safeApp.split('.')
    relativePath = os.path.join('Physical', args.configuration[0], plcDirectory[0],
                                'MappSafety', splitSafetyApp[0], 'C', 'PLC', 'R', 'CPU', 'CPU.ini')
    sys.stdout.write(project.getIniValue(relativePath, 'CRC', 'PROJECT'))
    return 0
