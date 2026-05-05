"""B&R AS Library (.lby) representation."""
import logging
import os
import os.path
import pathlib
import shutil
import xml.etree.ElementTree as ET
from typing import List, Union

from .models import BuildConfig, Dependency, LibExportInfo
from .paths import getLibraryType, getProgramType, getPkgType
from .xml_base import xmlAsFile


class Library(xmlAsFile):
    '''Represents a single ``.lby`` library file.'''

    def __init__(self, path):
        if os.path.isdir(path):
            path = os.path.join(path, getLibraryType(path) + '.lby')

        self.name = os.path.basename(os.path.dirname(path))
        self._dependencies: List[Dependency] = []
        super().__init__(path)
        self._xmlTag = self._getXmlTag(self.package)
        self._xmlTagChild = self._xmlTag[:-1]

    @property
    def files(self) -> ET.Element:
        return self.find(self._xmlTag)

    @property
    def fileList(self):
        return self.findall(self._xmlTag, self._xmlTagChild)

    @property
    def dependencyList(self):
        return self.findall('Dependencies', 'Dependency')

    @property
    def dependencies(self) -> List[Dependency]:
        self._dependencies.clear()
        for element in self.dependencyList:
            self._dependencies.append(
                Dependency(
                    name=element.get('ObjectName', 'Unknown'),
                    minVersion=element.get('FromVersion', ''),
                    maxVersion=element.get('ToVersion', ''),
                )
            )
        return self._dependencies

    @property
    def dependencyNames(self) -> List[str]:
        return [dep.name for dep in self.dependencies]

    @property
    def version(self) -> str:
        return self.root.get("Version", '0')

    @property
    def description(self) -> str:
        return self.root.get("Description", '')

    @property
    def type(self):
        return getLibraryType(self.dirPath)

    def addObject(self, *paths):
        for path in paths:
            if not os.path.isfile(path) and not os.path.isdir(path):
                raise FileNotFoundError(path)
            name = os.path.split(path)[1]
            newPath = os.path.join(self.dirPath, name)
            shutil.copyfile(path, newPath)
            self._addObjectElement(newPath)
        self.write()

    def _addObjectElement(self, path):
        element = self._createPkgElement(path, self._xmlTagChild)
        self.files.append(element)
        if element.get('Type') == 'Package' and self._xmlTag != 'Objects':
            self._convertXmlTag(self._xmlTag, 'Objects')

    def addDependency(self, *dependency):
        deps_container = self.find('Dependencies')
        if deps_container is None:
            deps_container = ET.SubElement(self.root, 'Dependencies')
        for dependent in dependency:
            if not isinstance(dependent, Dependency):
                raise TypeError('Expected Dependency class got', type(dependent))
            deps_container.append(self._createDependencyElement(dependent))

    def export(self, dest, buildFolder, buildConfigs, overwrite=False, binary=True, includeVersion=False) -> LibExportInfo:
        path = os.path.join(dest, self.name)
        if includeVersion:
            path = os.path.join(path, 'V%s' % self.version)
        info = LibExportInfo(self.name, path, None, self)
        try:
            if overwrite and os.path.exists(path):
                logging.debug('Export already exists, removing %s', path)
                shutil.rmtree(path, onerror=self._rmtreeOnError)
            if binary:
                self._collectBinaryLibrary(buildFolder, path, buildConfigs)
            else:
                self._collectSourceLibrary(self.dirPath, path)
        except (FileNotFoundError, FileExistsError) as error:
            logging.debug(error)
            info.exception = error
        return info

    def synchronize(self):
        objects = self.files
        items = list(os.listdir(self.dirPath))
        usedItems = []
        toRemove = []

        for obj in objects:
            if obj.text not in items:
                toRemove.append(obj)
            else:
                usedItems.append(obj.text)

        for obj in toRemove:
            objects.remove(obj)

        for item in items:
            if item not in usedItems:
                if os.path.splitext(item)[1] != '.lby':
                    if item not in ('SG4', 'SG3', 'SGC'):
                        self._addObjectElement(os.path.join(self.dirPath, item))

        self.write()

    def _convertXmlTag(self, fromTag: str, toTag: str):
        childTag = toTag[:-1]
        for elem in self.findall(fromTag):
            elem.tag = self.nameSpaceFormatted + toTag
            for child in elem:
                child.tag = self.nameSpaceFormatted + childTag
                if toTag == 'Objects':
                    child.set('Type', 'File')
        self._xmlTag = toTag
        self._xmlTagChild = childTag

    def _collectBinaryLibrary(self, buildFolder, dest, buildConfigs: List[BuildConfig]) -> None:
        '''Copies all files for a binary library into dest.'''
        packageFileName = self.type + '.lby'
        builds = {}
        for build in buildConfigs:
            if builds.get(build.type) is None:
                builds[build.type] = build

        self._collectSourceLibrary(
            self.dirPath, dest,
            ['.c', '.st', '.cpp', '.git', '.vscode', '.gitignore', 'jenkinsfile', 'CMakeLists.txt'],
            True,
        )

        if builds.get("sg4") is not None:
            self._collectConfigBinary(buildFolder, builds["sg4"], self.name, os.path.join(dest, 'SG4'))
        if builds.get("sg4_arm") is not None:
            self._collectConfigBinary(buildFolder, builds["sg4_arm"], self.name, os.path.join(dest, 'SG4', 'Arm'))

        os.rename(os.path.join(dest, packageFileName), os.path.join(dest, 'Binary.lby'))
        newLib = Library(os.path.join(dest, 'Binary.lby'))
        newLib.root.set('SubType', 'Binary')
        newLib.synchronize()

    @staticmethod
    def _formatVersionString(version: str) -> str:
        return '.'.join(str(int(x)) for x in version.split(sep='.'))

    @staticmethod
    def _createPkgElement(path: str, tag: str) -> ET.Element:
        attributes = {}
        attributes['Type'] = getPkgType(path)
        if attributes['Type'] == 'Library':
            attributes['Language'] = getLibraryType(path)
        if attributes['Type'] == 'Program':
            attributes['Language'] = getProgramType(path)
        element = ET.Element(tag, attrib=attributes)
        element.text = os.path.split(path)[1]
        element.tail = "\n"
        return element

    @staticmethod
    def _createDependencyElement(dependency: Dependency):
        attributes = {'ObjectName': dependency.name}
        if dependency.minVersion:
            attributes['FromVersion'] = dependency.minVersion
        if dependency.maxVersion:
            attributes['ToVersion'] = dependency.maxVersion
        return ET.Element('Dependency', attributes)

    @staticmethod
    def _getXmlTag(package: ET.ElementTree) -> str:
        namespace = Library._getASNamespaceFormatted(package)
        for child in package.getroot():
            if child.tag.replace(namespace, '') in ('Files', 'Objects'):
                return child.tag.replace(namespace, '')
        return 'Files'

    @staticmethod
    def _rmtreeOnError(func, path, exc_info):
        '''Error handler for ``shutil.rmtree`` that retries on access errors.'''
        import stat
        if not os.access(path, os.W_OK):
            os.chmod(path, stat.S_IWUSR)
            func(path)
        else:
            raise Exception(*exc_info)

    @staticmethod
    def _collectSourceLibrary(sourceFolder: Union[str], dest: Union[str], excludes=None, ignoreFolders=False) -> None:
        '''Copies all files for a source library into dest.'''
        if excludes is None:
            excludes = []

        def _ignorePatterns(path, names):
            ignores = []
            for name in names:
                for item in excludes:
                    if name.lower().endswith(item.lower()):
                        ignores.append(name)
                if ignoreFolders and os.path.isdir(os.path.join(path, name)):
                    ignores.append(name)
            return ignores

        shutil.copytree(sourceFolder, dest, ignore=_ignorePatterns)

    @staticmethod
    def _collectConfigBinary(tempPath: str, config: BuildConfig, libraryName: str, dest) -> None:
        '''Collects all binary files associated with a HW Config.'''
        pathlib.Path(dest).mkdir(parents=True, exist_ok=True)
        shutil.copy2(os.path.join(tempPath, 'Objects', config.name, config.hardware, libraryName + '.br'), dest)
        shutil.copy2(os.path.join(tempPath, 'Includes', libraryName + '.h'), dest)
        shutil.copy2(os.path.join(tempPath, 'Archives', config.name, config.hardware, 'lib' + libraryName + '.a'), dest)

    @staticmethod
    def _collectLogicalBinary(sourceFolder: Union[str], dest) -> None:
        '''Collects all Logical View files required for a binary library.'''
        pathlib.Path(dest).mkdir(parents=True, exist_ok=True)
        validExtensions = ['fun', 'lby', 'var', 'typ', 'md']
        for item in os.listdir(sourceFolder):
            extension = item.split('.')[-1]
            if extension in validExtensions:
                shutil.copy(os.path.join(sourceFolder, item), dest)
