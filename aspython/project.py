"""B&R AS Project (.apj) representation."""
import configparser
import fnmatch
import logging
import os
import os.path
import re
import subprocess
import xml.etree.ElementTree as ET
from typing import List, Union

from .build import batchBuildAsProject
from .library import Library
from .models import BuildConfig, ProjectExportInfo
from .package import Package
from .paths import (
    convertAsPathToWinPath,
    getASBuildPath,
    getConfigType,
    getHardwareFolderFromConfig,
    getPVITransferPath,
)
from .returncodes import PVIReturnCodeText
from .simulation import CreateARSimStructure
from .xml_base import xmlAsFile


class Project(xmlAsFile):
    def __init__(self, path: str):
        if os.path.isdir(path):
            projectFile = [f for f in os.listdir(path) if f.endswith('.apj')][0]
            path = os.path.join(path, projectFile)

        super().__init__(path)

        self.name = os.path.basename(os.path.splitext(path)[0])
        self.sourcePath = os.path.join(self.dirPath, 'Logical')
        self.physicalPath = os.path.join(self.dirPath, 'Physical')
        self.tempPath = os.path.join(self.dirPath, 'Temp')
        self.binaryPath = os.path.join(self.dirPath, 'Binaries')
        self.cacheIgnore = ['_AS', 'Acp10*', 'Arnc0*', 'Mapp*', 'Motion', 'TRF_LIB', 'Mp*', 'As*']
        self.libraries: List[Library] = []
        self.cacheProject()

    def _checkIgnore(self, iterable, ignores) -> List[str]:
        if ignores is not None:
            for ignore in ignores:
                iterable[:] = [name for name in iterable if not fnmatch.fnmatch(name, ignore)]
        return iterable

    def _checkLibIgnore(self, libs: List[Library], ignores) -> List[Library]:
        for ignore in ignores:
            libs[:] = [lib for lib in libs if not fnmatch.fnmatch(lib.path, ignore)]
        return libs

    def _resetCache(self):
        self.libraries.clear()

    def cacheProject(self):
        self._resetCache()
        for root, dirs, files in os.walk(self.sourcePath, topdown=True):
            dirs[:] = self._checkIgnore(dirs, self.cacheIgnore)
            files[:] = self._checkIgnore(files, self.cacheIgnore)

            for name in files:
                if name.endswith('.lby'):
                    try:
                        lib = Library(os.path.join(root, name))
                        self.libraries.append(lib)
                    except Exception:
                        pass
                if name.endswith('.pkg'):
                    package = Package(os.path.join(root, name))
                    objects = package.findall('Objects', 'Object')
                    for item in objects:
                        if (item.get('Type', '').lower() == 'library') & (item.get('Reference', '').lower() == 'true'):
                            path = convertAsPathToWinPath(item.text)
                            if path.startswith('.'):
                                path = os.path.abspath(os.path.join(os.path.dirname(self.path), path))
                            lib = Library(path)
                            self.libraries.append(lib)
        return self

    def exportLibraries(self, dest, overwrite=False, buildConfigs: List[BuildConfig] = None,
                        blacklist: list = None, whitelist: list = None,
                        binary: bool = True, includeVersion: bool = False) -> ProjectExportInfo:
        if buildConfigs is None:
            buildConfigs = self.buildConfigs
        if whitelist is None:
            whitelist = []
        if blacklist is None:
            blacklist = []

        exportLibs = []
        if len(whitelist) > 0:
            whitelist = [el.lower() for el in whitelist]
            for lib in self.libraries:
                if lib.name.lower() in whitelist:
                    exportLibs.append(lib)
        elif len(blacklist) > 0:
            blacklist = [el.lower() for el in blacklist]
            for lib in self.libraries:
                if lib.name.lower() not in blacklist:
                    exportLibs.append(lib)
        else:
            exportLibs = self.libraries.copy()

        exportInfo = ProjectExportInfo()
        for lib in exportLibs:
            logging.info('Exporting ' + lib.name + '...')
            result = lib.export(dest, self.tempPath, buildConfigs,
                                overwrite=overwrite, binary=binary, includeVersion=includeVersion)
            exportInfo.addLibInfo(result)
        return exportInfo

    def exportLibrary(self, library: Library, dest: str, overwrite=False,
                      ignores: Union[tuple, list] = None, binary: bool = True,
                      includeVersion: bool = False, withDependencies: bool = True) -> ProjectExportInfo:
        exportInfo = ProjectExportInfo()
        if withDependencies:
            depNames = library.dependencyNames
            depNames = self._checkIgnore(depNames, ignores)
            depNames = self._checkIgnore(depNames, self.cacheIgnore)
            dependencies = self.getLibrariesByName(depNames)
            for dep in dependencies:
                result = self.exportLibrary(dep, dest, ignores=ignores, overwrite=overwrite,
                                            binary=binary, includeVersion=includeVersion)
                exportInfo.extend(result)

        result = library.export(dest, self.tempPath, self.buildConfigs,
                                overwrite=overwrite, binary=binary, includeVersion=includeVersion)
        exportInfo.addLibInfo(result)
        return exportInfo

    def build(self, *configNames, buildMode: str = 'Build', buildRUCPackage: bool = True,
              tempPath: str = '', binaryPath: str = '', simulation: bool = False,
              additionalArgs: Union[str, list, tuple, None] = None):
        for configName in configNames:
            simulation_status = self.getHardwareParameter(configName, 'Simulation')
            if simulation_status == '':
                self.setHardwareParameter(configName, 'Simulation', str(int(simulation)))
            elif bool(int(simulation_status)) != simulation:
                self.setHardwareParameter(configName, 'Simulation', str(int(simulation)))

        return batchBuildAsProject(
            self.path, getASBuildPath(self.ASVersion), configNames, buildMode, buildRUCPackage,
            tempPath=tempPath, logPath=self.dirPath, binaryPath=binaryPath, simulation=simulation,
            additionalArg=additionalArgs,
        )

    def createPIP(self, configName, destination):
        logging.info(f'Creating PIP at {destination}')
        pviVersion = self.ASVersion.replace('AS', '', 1)
        pviVersion = 'V' + pviVersion[:1] + '.' + pviVersion[1:]

        config = self.getConfigByName(configName)
        RUCPackagePath = os.path.join(self.binaryPath, config.name, config.hardware, 'RUCPackage', 'RUCPackage.zip')

        RUCFolderPath = os.path.dirname(RUCPackagePath)
        RUCPilPath = os.path.join(RUCFolderPath, 'CreatePIP.pil')
        with open(RUCPilPath, 'w+') as f:
            f.write(
                f'CreatePIP "{RUCPackagePath}", '
                f'"InstallMode=ForceReboot InstallRestriction=AllowPartitioning KeepPVValues=0 '
                f'ExecuteInitExit=1 IgnoreVersion=1", "Default", "SupportLegacyAR=0", '
                f'"DestinationDirectory={destination}"'
            )

        arguments = [
            os.path.join(getPVITransferPath(pviVersion), 'PVITransfer.exe'),
            '-automatic', '-silent', RUCPilPath, '-consoleOutput',
        ]
        logging.debug(arguments)
        process = subprocess.run(arguments)
        logging.debug(process)
        if process.returncode == 0:
            logging.debug('PIP created')
        else:
            logging.debug(
                f'Error in creating PIP, code {process.returncode}: '
                f'{PVIReturnCodeText.get(process.returncode, "Unknown")}'
            )
        return process

    def createArsim(self, *configNames, destination=None, startSim: bool = False):
        '''*Deprecated* - see ``createSim``.'''
        if destination is None:
            destination = self.path
        return self.createSim(*configNames, destination=destination, startSim=startSim)

    def createSim(self, *configNames, destination, startSim: bool = False):
        pviVersion = self.ASVersion.replace('AS', '', 1)
        pviVersion = 'V' + pviVersion[:1] + '.' + pviVersion[1:]
        for configName in configNames:
            config = self.getConfigByName(configName)
            CreateARSimStructure(
                os.path.join(self.binaryPath, config.name, config.hardware, 'RUCPackage', 'RUCPackage.zip'),
                destination, pviVersion, startSim=startSim,
            )

    def startSim(self, configName: str, build: bool = False):
        pass

    def getLibraryByName(self, libName: str):
        for lib in self.libraries:
            if lib.name == libName:
                return lib
        return None

    def getLibrariesByName(self, libNames: List[str]) -> List[Library]:
        return [lib for lib in self.libraries if lib.name in libNames]

    def getConfigByName(self, configName: str) -> BuildConfig:
        return next(i for i in self.buildConfigs if i.name == configName)

    def getConstantValue(self, filePath: str, varName: str):
        fullFilePath = os.path.join(self.dirPath, filePath)
        with open(fullFilePath, "r") as f:
            fileContents = f.read()
        return re.search(varName + ".*'(.*)'", fileContents).group(1)

    def getIniValue(self, filePath: str, sectionName: str, keyName: str):
        fullFilePath = os.path.join(self.dirPath, filePath)
        config = configparser.ConfigParser()
        config.read(fullFilePath)
        return config[sectionName][keyName]

    @property
    def buildConfigs(self) -> List[BuildConfig]:
        return self._getConfigs(self.physicalPath)

    @property
    def buildConfigNames(self) -> List[str]:
        return [config.name for config in self.buildConfigs]

    @property
    def ASVersion(self) -> str:
        with open(self.path, 'r') as f:
            return self._parseASVersion(f.read())

    @staticmethod
    def _parseASVersion(apj: str) -> str:
        result = re.search('<?AutomationStudio Version="(.*)" ', apj).group(1).split('.')
        # AS <= 4.x installs to versioned folders like AS41, AS45, AS46
        # (major + minor). AS 6.x installs into a single AS6 folder, with
        # minor revisions (6.0, 6.1, 6.5, ...) sharing one install path.
        try:
            major = int(result[0])
        except (ValueError, IndexError):
            major = 0
        if major >= 6:
            version = result[0]
        else:
            version = ''.join(result[0:2])
        return 'AS' + version

    def getHardwareParameter(self, config, paramName) -> str:
        hardwareFile = xmlAsFile(os.path.join(self.physicalPath, config, 'Hardware.hw'))
        element = hardwareFile.find("Module", "Parameter[@ID='" + paramName + "']")
        if element is not None:
            return element.attrib['Value']
        return ''

    def setHardwareParameter(self, config, paramName, paramValue):
        hardwareFile = xmlAsFile(os.path.join(self.physicalPath, config, 'Hardware.hw'))
        try:
            attributes = hardwareFile.find("Module", "Parameter[@ID='" + paramName + "']").attrib
            attributes['Value'] = paramValue
            hardwareFile.write()
        except Exception:
            attributes = {'ID': paramName, 'Value': paramValue}
            element = ET.Element('Parameter', attrib=attributes)
            parent_map = {c: p for p in hardwareFile.package.iter() for c in p}
            config_element = hardwareFile.find("Module", "Parameter[@ID='ConfigurationID']")
            for key, value in parent_map.items():
                if config_element == key:
                    parent = value
                    parent_element = hardwareFile.find("Module[@Name='" + parent.attrib["Name"] + "']")
                    parent_element.append(element)
                    hardwareFile.write()
                    return

    def _getConfigs(self, physicalPath: str) -> List[BuildConfig]:
        physical = Package(os.path.join(self.physicalPath, 'Physical.pkg'))
        objects = physical.findall('Objects', 'Object')
        configurations: List[BuildConfig] = []
        for config in objects:
            if config.get('Type', '').lower() == 'configuration':
                path = os.path.join(physicalPath, config.text)
                configurations.append(BuildConfig(name=config.text, path=path,
                                                   hardware=getHardwareFolderFromConfig(path)))
                configurations[-1].type = getConfigType(configurations[-1])
        return configurations
