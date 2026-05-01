"""``aspython arsim`` subcommand."""
import logging
import os
import shutil
import sys
import tarfile

from .. import Project
from ..returncodes import ASReturnCodes


SUBCOMMAND = 'arsim'
HELP = 'Build (optional) and create an ARsim package for an AS project.'


def add_subparser(subparsers):
    p = subparsers.add_parser(SUBCOMMAND, help=HELP, description=HELP)
    p.add_argument('project', type=str, help='AS project you want to build')
    p.add_argument('-c', '--configuration', nargs='+', type=str, required=True,
                   help='AS configuration(s) you want to build')
    p.add_argument('-bm', '--buildMode', type=str, default='None',
                   choices=['Rebuild', 'Build', 'BuildAndTransfer', 'BuildAndCreateCompactFlash', 'None'])
    p.add_argument('-ss', '--startSim', action='store_true',
                   help='Start ARsim after creation')
    p.add_argument('-uf', '--userFiles', type=str, default='',
                   help='Path to folder with user partition files to include in the simulator')
    p.add_argument('-hf', '--hmiFiles', type=str, default='',
                   help='Path to folder with HMI files to include in the simulator')
    p.set_defaults(func=run)
    return p


def run(args) -> int:
    logging.debug('args: %s', args)
    project = Project(args.project)

    if args.buildMode != 'None':
        for config in args.configuration:
            buildStatus = project.build(config, buildMode=args.buildMode, simulation=True)
            if buildStatus.returncode > ASReturnCodes['Warnings']:
                sys.exit(f'Build failed for config {config}')
            logging.debug('Building of %s Complete!', config)

    for config in args.configuration:
        destination = os.path.join(project.tempPath, 'SIM', config)
        sim_root = os.path.join(project.tempPath, 'SIM')
        if not os.path.isdir(sim_root):
            os.mkdir(sim_root)
        if os.path.isdir(destination):
            shutil.rmtree(destination)
        os.mkdir(destination)

        project.createSim(config, destination=destination, startSim=args.startSim)

        if args.userFiles != '':
            shutil.copytree(args.userFiles, os.path.join(destination, 'ARSimUser'))
        if args.hmiFiles != '':
            shutil.copytree(args.hmiFiles, os.path.join(destination, 'HMI'),
                            ignore=shutil.ignore_patterns('node_modules'))

        os.chdir(destination)
        tf = tarfile.open('Simulator.tar.gz', mode='w:gz', format=tarfile.PAX_FORMAT)
        for item in os.listdir():
            tf.add(item)
        tf.close()

    return 0
