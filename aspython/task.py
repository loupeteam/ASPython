"""B&R AS Task (.prg) representation."""
import os
import os.path

from .xml_base import xmlAsFile


class Task(xmlAsFile):
    def __init__(self, path: str):
        if os.path.isdir(path):
            self.path = path
            if 'ANSIC.prg' in os.listdir(path):
                self.type = 'ANSIC'
                super().__init__(os.path.join(path, 'ANSIC.prg'))
            elif 'IEC.prg' in os.listdir(path):
                self.type = 'IEC'
                super().__init__(os.path.join(path, 'IEC.prg'))
            else:
                self.type = None
