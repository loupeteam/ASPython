"""``aspython build`` subcommand."""
import logging
import os
import shutil
import sys
import tarfile

from .. import Project
from ..returncodes import ASReturnCodes


SUBCOMMAND = 'build'
HELP = 'Build one or more configurations of an AS project.'


def add_subparser(subparsers):
    p = subparsers.add_parser(SUBCOMMAND, help=HELP, description=HELP)
    p.add_argument('project', type=str, help='Path to AS project you want to build')
    p.add_argument('-c', '--configuration', nargs='+', type=str, required=True,
                   help='AS configuration(s) you want to build')
    p.add_argument('-bm', '--buildMode', type=str, default='Build',
                   choices=['Rebuild', 'Build', 'BuildAndTransfer', 'BuildAndCreateCompactFlash', 'None'],
                   help='Type of build in AS')
    p.add_argument('-rp', '--buildRUCPackage', action='store_false',
                   help='Disable building the RUCPackage')
    p.add_argument('-sim', '--simulation', action='store_true',
                   help='Build for simulation')
    p.add_argument('-pip', action='store_true',
                   help='Generate a PIP after the build completes')
    p.set_defaults(func=run)
    return p


def run(args) -> int:
    logging.debug('The project to be built is: %s', args.project)
    logging.debug('Config(s): %s, mode: %s, RUC: %s, sim: %s',
                  args.configuration, args.buildMode, args.buildRUCPackage, args.simulation)

    project = Project(os.path.abspath(args.project))

    for config in args.configuration:
        buildStatus = project.build(
            config, buildMode=args.buildMode,
            buildRUCPackage=args.buildRUCPackage, simulation=args.simulation,
        )

        if buildStatus.returncode > ASReturnCodes['Warnings']:
            sys.exit(f'Build failed for config {config}')

        if args.pip:
            destination = os.path.join(project.tempPath, 'PIP', config)
            pip_root = os.path.join(project.tempPath, 'PIP')
            if not os.path.isdir(pip_root):
                os.mkdir(pip_root)
            if os.path.isdir(destination):
                shutil.rmtree(destination)
            os.mkdir(destination)
            project.createPIP(config, destination)

            os.chdir(destination)
            tf = tarfile.open('Installer.tar.gz', mode='w:gz', format=tarfile.USTAR_FORMAT)
            for item in os.listdir():
                tf.add(item)
            tf.close()
        else:
            logging.debug('Building of %s Complete!', config)

    return 0
