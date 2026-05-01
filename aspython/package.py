"""B&R AS Package (Package.pkg) representation."""
import os
import os.path
import shutil
import xml.etree.ElementTree as ET

from .paths import getLibraryType, getProgramType, getPkgType
from .xml_base import xmlAsFile


class Package(xmlAsFile):
    def __init__(self, path: str, new_pkg: bool = False):
        if os.path.isdir(path):
            path = os.path.join(path, 'Package.pkg')
            if new_pkg:
                package_element = ET.Element('Package')
                package_element.set('xmlns', 'http://br-automation.co.at/AS/Package')
                ET.SubElement(package_element, 'Objects')
                tree = ET.ElementTree(package_element)
        if new_pkg:
            super().__init__(path, tree)
        else:
            super().__init__(path)

    def synchPackageFile(self):
        items = list(os.listdir(self.dirPath))
        objsText = {}

        for element in self.objects:
            if element.text not in items:
                self._removePkgObject(element.text)
            else:
                objsText[element.text] = element

        for item in items:
            if item == os.path.split(self.path)[1]:
                continue
            if item not in objsText:
                self._addPkgObject(path=os.path.join(self.dirPath, item))

        self.write()
        return self

    def addObject(self, path, reference=False):
        '''Copy file or folder to package and directory.'''
        name = os.path.basename(path)
        newPath = os.path.join(self.dirPath, name)
        if os.path.dirname(path) != self.dirPath and not reference:
            if os.path.isfile(path):
                shutil.copyfile(path, newPath)
            else:
                shutil.copytree(path, newPath)
        return self._addPkgObject(newPath)

    def addEmptyPackage(self, name):
        full_path = self.dirPath + '/' + name
        os.mkdir(full_path)
        self._addPkgObject(full_path)
        newPackage = Package(full_path, True)
        newPackage.write()
        return newPackage

    def removeObject(self, name):
        '''Remove file or folder from package and directory.'''
        path_to_remove = os.path.join(self.dirPath, name)
        if os.path.isdir(path_to_remove):
            shutil.rmtree(path_to_remove)
        elif os.path.isfile(path_to_remove):
            os.remove(path_to_remove)
        self._removePkgObject(name)

    def _removePkgObject(self, name):
        for child in self.objects:
            if child.text == name:
                self.objects.remove(child)
        self.write()

    def _addPkgObject(self, path: str, reference: bool = False, element: ET.Element = None) -> ET.Element:
        if element is None:
            element = self._createElement(path, reference=reference)
        obj = self.find('Objects')
        obj.append(element)
        self.write()
        return element

    @staticmethod
    def _createElement(path: str, reference: bool = False) -> ET.Element:
        if path is None:
            raise FileNotFoundError(path)
        attributes = {}
        attributes['Type'] = getPkgType(path)
        if attributes['Type'] == 'Library':
            attributes['Language'] = getLibraryType(path)
        if attributes['Type'] == 'Program':
            attributes['Language'] = getProgramType(path)
        if reference:
            attributes['Reference'] = "true"

        element = ET.Element('Object', attrib=attributes)
        if reference:
            if os.path.isabs(path):
                element.text = os.path.abspath(path)
            else:
                element.text = os.path.normpath(os.path.join('\\', path))
        else:
            element.text = os.path.basename(path)
        element.tail = "\n"
        return element

    @property
    def objects(self):
        return self.find('Objects')

    @property
    def objectList(self):
        return self.findall('Objects', 'Object')
