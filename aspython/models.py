"""Domain value objects (build configurations, library export results, dependencies)."""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class LibExportInfo:
    name: str
    path: str
    exception: Optional[BaseException] = None
    lib: Optional[object] = None


@dataclass
class ProjectExportInfo:
    _success: List[LibExportInfo] = field(default_factory=list)
    _failed: List[LibExportInfo] = field(default_factory=list)

    def addLibInfo(self, libInfo: LibExportInfo) -> None:
        if libInfo.exception is None:
            self._success.append(libInfo)
        else:
            self._failed.append(libInfo)

    def extend(self, *exportInfo: "ProjectExportInfo") -> None:
        for info in exportInfo:
            self._success.extend(info._success)
            self._failed.extend(info._failed)

    @property
    def success(self) -> List[LibExportInfo]:
        return self._success

    @property
    def failed(self) -> List[LibExportInfo]:
        return self._failed


@dataclass
class Dependency:
    name: str
    minVersion: str = ''
    maxVersion: str = ''


@dataclass
class BuildConfig:
    name: str
    path: str = ''
    type: str = 'sg4'
    hardware: str = ''

    # Backwards compat: original constructor signature used kwarg `typ`.
    def __init__(self, name: str, path: str = '', typ: str = 'sg4', hardware: str = '') -> None:
        self.name = name
        self.path = path
        self.type = typ
        self.hardware = hardware
