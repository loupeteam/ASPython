"""B&R Automation Studio path helpers and AS-style path conversions."""
import os.path
from typing import Optional


# Candidate base directories where B&R Automation Studio may be installed.
# AS <= 4.x defaults to C:\BrAutomation. AS 6 changed the default to
# C:\Program Files (x86)\BRAutomation (note: no space in "BRAutomation").
_AS_BASE_CANDIDATES = [
    "C:\\BrAutomation",
    "C:\\Program Files (x86)\\BRAutomation",
    "C:\\Program Files\\BRAutomation",
]


def _findASBase(version: str = '') -> str:
    """Return the base BrAutomation directory.

    If a specific version is provided, prefer a base that actually contains
    a folder for that version. Otherwise return the first base that exists.
    Falls back to the legacy default 'C:\\BrAutomation' if none are found.
    """
    if version and version.lower() != 'base':
        for base in _AS_BASE_CANDIDATES:
            if os.path.isdir(os.path.join(base, version.upper())):
                return base
    for base in _AS_BASE_CANDIDATES:
        if os.path.isdir(base):
            return base
    return _AS_BASE_CANDIDATES[0]


def getASPath(version: str) -> str:
    base = _findASBase(version)
    if version.lower() == 'base':
        return base
    return os.path.join(base, version.upper(), 'Bin-en')


def getASBuildPath(version: str) -> str:
    if version.lower() == 'base':
        return getASPath('base')
    return os.path.join(getASPath(version), "BR.AS.Build.exe")


def getPVITransferPath(version: str) -> str:
    base = getASPath('base')
    return os.path.join(base, 'PVI', version, 'PVI', 'Tools', 'PVITransfer')


def getLibraryType(path: str) -> str:
    if os.path.exists(os.path.join(path, 'ANSIC.lby')):
        return 'ANSIC'
    if os.path.exists(os.path.join(path, 'IEC.lby')):
        return 'IEC'
    if os.path.exists(os.path.join(path, 'Binary.lby')):
        return 'Binary'
    return 'None'


def getProgramType(path: str) -> str:
    if os.path.exists(os.path.join(path, 'ANSIC.prg')):
        return 'ANSIC'
    if os.path.exists(os.path.join(path, 'IEC.prg')):
        return 'IEC'
    if os.path.exists(os.path.join(path, 'Binary.prg')):
        return 'Binary'
    return 'None'


def getPkgType(path: str) -> Optional[str]:
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    if os.path.isdir(path):
        if getLibraryType(path) != 'None':
            return 'Library'
        if getProgramType(path) != 'None':
            return 'Program'
        return 'Package'
    if os.path.isfile(path):
        return 'File'
    return None


def getAsPathType(path: str) -> Optional[str]:
    """Returns 'relative', 'absolute', or None for an AS-style path string."""
    if path[0] == '\\' or path[0:2] == "..":
        return "relative"
    if path[0] == '/' or path[0:2] == "C:":
        return "absolute"
    return None


def convertAsPathToWinPath(asPath: str) -> str:
    if getAsPathType(asPath) == 'relative':
        return '.' + os.path.join(os.sep, os.path.normpath(asPath))
    return os.path.normpath(asPath)


def convertWinPathToAsPath(winPath: str) -> str:
    if os.path.isabs(winPath):
        return os.path.normpath(winPath)
    return os.path.join('\\', os.path.normpath(winPath))


def getLibraryPathInPackage(libraryPackagePath: str, libraryName: str) -> Optional[str]:
    """Return the path to ``<libraryName>.lby`` within a Libraries package, resolving references."""
    # Local import to avoid a circular package <-> paths dependency at import time.
    from .package import Package

    asPackage = Package(libraryPackagePath)
    for obj in asPackage.objectList:
        if obj.attrib.get('Reference', 'false') == 'true' and libraryName.lower() in obj.text.lower():
            return convertAsPathToWinPath(obj.text)
        if obj.text.lower() == libraryName.lower():
            return os.path.join(libraryPackagePath, libraryName)
    return None


def getActualPathFromLogicalPath(logicalPath: str) -> Optional[str]:
    """Resolve an AS 'Logical' path on disk, walking through reference packages."""
    from .package import Package

    splitPath = os.path.normpath(logicalPath).split(os.sep)
    if splitPath[0] == "":
        splitPath = splitPath[1:]
    currentPath = "."
    for step in splitPath:
        if step.lower() in [s.lower() for s in os.listdir(currentPath)]:
            currentPath = os.path.join(currentPath, step)
        elif 'package.pkg' in [s.lower() for s in os.listdir(currentPath)]:
            currentAsPackage = Package(currentPath)
            found = False
            for obj in currentAsPackage.objectList:
                if obj.attrib.get('Reference', '') == 'true' and step in obj.text:
                    currentPath = convertAsPathToWinPath(obj.text)
                    found = True
            if not found:
                return None
        else:
            return None
    return currentPath


def getHardwareFolderFromConfig(configPath: str) -> str:
    """Get the hardware folder name from a path to a configuration folder.

    Assumes there is a single hardware sub-folder under the configuration.
    """
    return [d for d in os.listdir(configPath) if os.path.isdir(os.path.join(configPath, d))][0]


# Type-detection cpu prefix table (was buried inside getConfigType in the legacy module).
_SG4_ARM = 'sg4_arm'
_SG4 = 'sg4'
_CPU_TYPE_MAP = {
    'x20cp04': _SG4_ARM,
    'x20cp13': _SG4,
    'x20cp14': _SG4,
    'x20cp3': _SG4,
    'apc': _SG4,
    '5pc': _SG4,
}


def getConfigType(config) -> str:
    """Returns 'sg4' or 'sg4_arm' based on the hardware folder name."""
    for key, value in _CPU_TYPE_MAP.items():
        if config.hardware.lower().startswith(key):
            return value
    return _SG4
