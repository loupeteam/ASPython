"""B&R AS software deployment table (cpu.sw)."""
import os
import os.path
import xml.etree.ElementTree as ET
from typing import List

from .paths import getActualPathFromLogicalPath, getLibraryPathInPackage, getLibraryType
from .task import Task
from .xml_base import xmlAsFile


class SwDeploymentTable(xmlAsFile):
    def __init__(self, path: str):
        if os.path.isfile(path):
            self.path = path
            super().__init__(path)
            for i in range(8):
                tc = self.find(f"TaskClass[@Name='Cyclic#{i+1}']")
                if tc is None:
                    tc = self._addRootLevelElement('TaskClass', i, {"Name": f"Cyclic#{i+1}"})
            lib = self.find('Libraries')
            if lib is None:
                lib = self._addRootLevelElement('Libraries')
            self.read()

    def deployLibrary(self, libraryFolder, library, attributes=None):
        if attributes is None:
            attributes = {}
        obj = self.find('Libraries')
        for lib in self.libraries:
            if lib.lower() == library.lower():
                return
        element = self._createLibraryElement(libraryFolder, library, attributeOverrides=attributes)
        obj.append(element)
        self.write()

    def deployTask(self, taskFolder, taskName, taskClass):
        cyclicName = "Cyclic#" + [s for s in str(taskClass) if s.isdigit()][0]
        tc = self.find(f"TaskClass[@Name='{cyclicName}']")
        preexistingTask = self.find(f"TaskClass[@Name='{cyclicName}']", "Task[@Name='" + taskName[:10] + "']")
        if preexistingTask is not None:
            return
        element = self._createTaskElement(taskFolder, taskName)
        tc.append(element)
        self.write()

    def _createLibraryElement(self, libraryFolder, name, memory: str = 'UserROM', attributeOverrides=None) -> ET.Element:
        if attributeOverrides is None:
            attributeOverrides = {}
        lbyPath = getLibraryPathInPackage(libraryFolder, name)
        language = getLibraryType(lbyPath)
        splitPath = os.path.split(libraryFolder)
        parentFolder = splitPath[-1]
        attributes = {
            'Name': name,
            'Source': '.'.join(('Libraries', parentFolder, name, 'lby')),
            'Memory': memory,
            'Language': language,
            'Debugging': 'true',
        }
        for attributeName in attributeOverrides:
            attributes[attributeName] = attributeOverrides[attributeName]
        element = ET.Element('LibraryObject', attrib=attributes)
        element.tail = "\n"
        return element

    def _createTaskElement(self, taskFolder, taskName, memory: str = 'UserROM') -> ET.Element:
        actualTaskFolderPath = getActualPathFromLogicalPath(taskFolder)
        prgPath = os.path.join(actualTaskFolderPath, taskName)
        task = Task(prgPath)
        language = task.type
        splitPath = os.path.normpath(taskFolder).split(os.sep)
        for i, part in enumerate(splitPath):
            if part.lower() == "logical":
                splitPath = splitPath[i + 1:]
                break
        splitPath.append(taskName)
        splitPath.append('prg')
        attributes = {
            'Name': taskName[:10],
            'Source': '.'.join(splitPath),
            'Memory': memory,
            'Language': language,
            'Debugging': 'true',
        }
        element = ET.Element('Task', attrib=attributes)
        element.tail = "\n"
        return element

    def _addLibrariesElement(self):
        self._addRootLevelElement('Libraries')
        self.read()
        return self.find('Libraries')

    def _addRootLevelElement(self, name, index=None, attributes=None):
        if attributes is None:
            attributes = {}
        element = ET.Element(name, attrib=attributes)
        element.tail = "\n"
        if index is None:
            self.root.append(element)
        else:
            self.root.insert(index, element)
        self.write()

    @property
    def libraries(self) -> List:
        return [element.get('Name', 'Unknown') for element in self.findall('Libraries', 'LibraryObject')]
