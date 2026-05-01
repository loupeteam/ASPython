"""ASPython - Python toolkit for B&R Automation Studio projects.

Public API is re-exported here for convenience::

    from aspython import Project, Library, Package, BuildConfig
"""
from ._version import __version__
from .returncodes import ASReturnCodes, PVIReturnCodeText
from .models import LibExportInfo, ProjectExportInfo, Dependency, BuildConfig
from .paths import (
    getASPath,
    getASBuildPath,
    getPVITransferPath,
    getActualPathFromLogicalPath,
    getAsPathType,
    convertAsPathToWinPath,
    convertWinPathToAsPath,
    getLibraryPathInPackage,
    getLibraryType,
    getProgramType,
    getPkgType,
)
from .xml_base import xmlAsFile
from .library import Library
from .package import Package
from .task import Task
from .deployment import SwDeploymentTable
from .config import CpuConfig
from .build import (
    ASProjetGetConfigs,
    batchBuildAsProject,
    buildASProject,
)
from .simulation import CreateARSimStructure
from .project import Project
from .utils import toDict

__all__ = [
    "__version__",
    "ASReturnCodes",
    "PVIReturnCodeText",
    "LibExportInfo",
    "ProjectExportInfo",
    "Dependency",
    "BuildConfig",
    "getASPath",
    "getASBuildPath",
    "getPVITransferPath",
    "getActualPathFromLogicalPath",
    "getAsPathType",
    "convertAsPathToWinPath",
    "convertWinPathToAsPath",
    "getLibraryPathInPackage",
    "getLibraryType",
    "getProgramType",
    "getPkgType",
    "xmlAsFile",
    "Library",
    "Package",
    "Task",
    "SwDeploymentTable",
    "CpuConfig",
    "ASProjetGetConfigs",
    "batchBuildAsProject",
    "buildASProject",
    "CreateARSimStructure",
    "Project",
    "toDict",
]
