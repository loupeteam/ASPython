"""B&R AS CPU configuration (Cpu.pkg / Configuration)."""
import os.path

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
