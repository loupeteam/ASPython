"""Base ``xmlAsFile`` class for reading/writing AS XML files (.lby/.pkg/.apj/...)."""
import os.path
import xml.etree.ElementTree as ET
from typing import List, Optional


class xmlAsFile:
    def __init__(self, path: str, new_data: Optional[ET.ElementTree] = None):
        self.path = path
        if new_data is None:
            self.read()
        else:
            self._package = new_data
            self.package.write(self.path, xml_declaration=True, encoding='utf-8', method='xml')

    def read(self):
        '''Reads AS xml file into xml tree'''
        if not os.path.exists(self.path):
            raise FileNotFoundError(self.path)
        self._package = ET.parse(self.path)
        return self

    def write(self):
        '''Writes xml tree to file with AS Namespace'''
        # TODO: This loses the <?AutomationStudio Version=...> processing instruction.
        ns = self._getASNamespace(self.package)
        ET.register_namespace('', ns)  # TODO: This is an ET global effect.
        self._indentXml(self.package.getroot())
        self.package.write(self.path, xml_declaration=True, encoding='utf-8', method='xml')
        return self

    def find(self, *levels) -> ET.Element:
        path = '.'
        for level in levels:
            path += '/' + self.nameSpaceFormatted + level
        return self.root.find(path)

    def findall(self, *levels) -> List[ET.Element]:
        path = '.'
        for level in levels:
            path += '/' + self.nameSpaceFormatted + level
        return self.root.findall(path)

    @property
    def nameSpaceFormatted(self) -> str:
        ns = self.nameSpace
        if ns != '':
            ns = '{' + ns + '}'
        return ns

    @property
    def nameSpace(self) -> str:
        return self._getASNamespace(self.package)

    @property
    def root(self) -> ET.Element:
        return self.package.getroot()

    @property
    def package(self) -> ET.ElementTree:
        return self._package

    @property
    def dirPath(self) -> str:
        return os.path.dirname(self.path)

    @property
    def getXmlType(self) -> str:
        '''Returns a string representation of xml type (debug-only).'''
        ns = self._getASNamespace(self.package)
        return ns.split('/')[-1]

    @staticmethod
    def _indentXml(elem: ET.Element, level: int = 0) -> None:
        '''Indent Element and sub elements'''
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:  # noqa: B020 - mirror legacy semantics; tail-fix uses last child below.
                xmlAsFile._indentXml(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    @staticmethod
    def _getASNamespace(package: ET.ElementTree) -> str:
        '''Get Automation Studio's namespace for xml files.'''
        ns = package.getroot().tag.split('}')
        if ns[0][0] == '{':
            ns = ns[0][1:]
        else:
            ns = ''
        return ns

    @staticmethod
    def _getASNamespaceFormatted(package: ET.ElementTree) -> str:
        '''Get Automation Studio's namespace formatted as ElementTree expects.'''
        ns = xmlAsFile._getASNamespace(package)
        if ns != '':
            ns = '{' + ns + '}'
        return ns
