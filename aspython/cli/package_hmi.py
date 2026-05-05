"""``aspython package-hmi`` subcommand — package a Loupe UX HMI."""
import logging

from ..hmi import installDependencies, installElectronPackager, packageHMI, updateAppVersion


SUBCOMMAND = 'package-hmi'
HELP = 'Package a Loupe UX-based HMI via electron-packager.'


def add_subparser(subparsers):
    p = subparsers.add_parser(SUBCOMMAND, help=HELP, description=HELP)
    p.add_argument('-s', '--source', type=str, required=True,
                   help='Source folder where the HMI files (main package.json) are located')
    p.add_argument('-o', '--output', type=str, required=True,
                   help='Destination folder for the packaged files')
    p.add_argument('-an', '--appName', type=str, required=True,
                   help='Name of the app to package')
    p.add_argument('-av', '--appVersion', type=str, default='1.0.0',
                   help='Version of the app to create')
    p.add_argument('-ap', '--appPublisher', type=str, default='Loupe',
                   help='Name of the app publisher')
    p.add_argument('--installElectronPackager', dest='installElectronPackager', action='store_true',
                   help='Install electron-packager before packaging')
    p.set_defaults(func=run)
    return p


def run(args) -> int:
    installDependencies(args.source)
    try:
        installDependencies(args.source + '/public')
    except Exception:
        logging.info('No public sub-folder found, skipping its dependency installation')

    if args.installElectronPackager:
        installElectronPackager()

    appSemanticVersion = updateAppVersion(args.source, args.appVersion)
    packageHMI(args.source, args.appName, args.output, args.appPublisher, appSemanticVersion)
    return 0
