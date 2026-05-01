"""HMI packaging via electron-packager."""
import json
import logging
import os
import subprocess


def installDependencies(source: str) -> None:
    os.chdir(source)
    if 'package.json' not in os.listdir('.'):
        logging.info('The source directory does not contain a package.json, skipping install')
    else:
        subprocess.run('npm install', encoding='utf-8', errors='replace', shell=True)


def installElectronPackager() -> None:
    subprocess.run('npm install electron-packager -g', encoding='utf-8', errors='replace', shell=True)


def updateAppVersion(source: str, version: str) -> str:
    with open(source + '/package.json', 'r+') as f:
        data = json.load(f)
        data['version'] = version
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
    return version


def packageHMI(source: str, appName: str, output: str, appPublisher: str, appVersion: str) -> None:
    command = [
        'electron-packager',
        source,
        appName,
        '--platform=win32',
        '--arch=x64',
        f'--out={output}',
        '--overwrite',
        f'--win32metadata.CompanyName="{appPublisher}"',
        f'--win32metadata.FileDescription="Build #{appVersion}"',
    ]
    logging.info(command)
    subprocess.run(command, encoding='utf-8', shell=True)
