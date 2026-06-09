"""B&R AS CPU configuration (Cpu.pkg / Configuration)."""
import os.path
from typing import List, Optional

from .deployment import SwDeploymentTable
from .paths import findProjectRoot, resolveReferencePath
from .xml_base import xmlAsFile


class CpuConfig(xmlAsFile):
    def __init__(self, path: str):
        if os.path.isfile(path):
            self.path = path
            super().__init__(path)
            self.buildElement = self.find('Configuration', 'Build')
            self.arElement = self.find('Configuration', 'AutomationRuntime')

    def getGccVersion(self):
        return self.buildElement.attrib.get('GccVersion')

    def setGccVersion(self, value):
        self.buildElement.attrib['GccVersion'] = value
        self.write()

    def getPreBuildStep(self):
        return self.buildElement.attrib.get('PreBuildStep')

    def setPreBuildStep(self, value):
        self.buildElement.attrib['PreBuildStep'] = value
        self.write()

    def getArVersion(self):
        return self.arElement.attrib.get('Version')

    def setArVersion(self, value):
        self.arElement.attrib['Version'] = value
        self.write()

    gccVersion = property(getGccVersion, setGccVersion)
    preBuildStep = property(getPreBuildStep, setPreBuildStep)
    arVersion = property(getArVersion, setArVersion)

    @property
    def objectList(self) -> List:
        """The ``<Object>`` entries listed under this Cpu.pkg's ``<Objects>``."""
        return self.findall('Objects', 'Object')

    def getSoftwareConfigPath(self, projectRoot: Optional[str] = None) -> Optional[str]:
        """Resolve this CPU's software-configuration (``.sw``) file on disk.

        The ``.sw`` may be a file owned by this CPU folder, or a reference to
        another configuration's ``.sw`` (common when several configurations
        share one software deployment). References are resolved relative to the
        project root, which is auto-detected from the package location when
        *projectRoot* is not given.
        """
        if projectRoot is None:
            projectRoot = findProjectRoot(self.path) or self.dirPath
        for obj in self.objectList:
            text = (obj.text or '').strip()
            if not text.lower().endswith('.sw'):
                continue
            if obj.attrib.get('Reference', 'false').lower() == 'true':
                return resolveReferencePath(text, self.dirPath, projectRoot)
            return os.path.normpath(os.path.join(self.dirPath, text))
        # Fall back to the conventional local file name.
        local = os.path.join(self.dirPath, 'Cpu.sw')
        return os.path.normpath(local) if os.path.isfile(local) else None

    def getSwDeploymentTable(self, projectRoot: Optional[str] = None) -> Optional[SwDeploymentTable]:
        """Return the resolved :class:`SwDeploymentTable`, or ``None`` if absent."""
        swPath = self.getSoftwareConfigPath(projectRoot)
        if swPath and os.path.isfile(swPath):
            return SwDeploymentTable(swPath)
        return None
