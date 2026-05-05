"""``aspython installer`` subcommand — generate an Inno Setup installer."""
from ..installer import compileInstaller, generateGUID


SUBCOMMAND = 'installer'
HELP = 'Generate an Inno Setup installer (.exe) from an .iss script.'


def add_subparser(subparsers):
    p = subparsers.add_parser(SUBCOMMAND, help=HELP, description=HELP)
    p.add_argument('script', type=str, help='Name of the iss script to compile')
    p.add_argument('-o', '--output', type=str, required=True,
                   help='Destination folder for the installer')
    p.add_argument('-an', '--appName', type=str, required=True,
                   help='Name of the app to create')
    p.add_argument('-av', '--appVersion', type=str, default='1.0.0',
                   help='Version of the app to create')
    p.add_argument('-ap', '--appPublisher', type=str, default='Loupe',
                   help='Name of the app publisher')
    p.add_argument('-au', '--appUrl', type=str, default='https://loupe.team',
                   help='URL of the app publisher')
    p.add_argument('-sd', '--simDir', type=str,
                   help='Directory where Simulation assets are located')
    p.add_argument('-ud', '--userDir', type=str,
                   help='Directory where User Partition assets are located')
    p.add_argument('-jb', '--junctionBatch', type=str, default='ConnectFileDevice.bat',
                   help='Name of the Junction Batch file')
    p.add_argument('-hd', '--hmiDir', type=str,
                   help='Directory where HMI assets are located')
    p.add_argument('-he', '--hmiExe', type=str, help='Name of the HMI EXE file')
    p.set_defaults(func=run)
    return p


def run(args) -> int:
    GUID = generateGUID()
    compileInstaller(args, GUID)
    return 0
