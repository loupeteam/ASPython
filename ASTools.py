'''
 * File: ASTools.py
 * Copyright (c) 2023 Loupe
 * https://loupe.team
 *
 * This file is part of ASPython, licensed under the MIT License.
'''
"""Backwards-compatibility shim.

Historically all of ASPython lived in this single file. The implementation now lives in the
``aspython`` package; this module re-exports every previously public name and emits a
``DeprecationWarning`` on import. New code should ``import aspython`` (or
``from aspython import Project``) instead.
"""
import warnings as _warnings

from aspython import (  # noqa: F401
    ASReturnCodes,
    PVIReturnCodeText,
    LibExportInfo,
    ProjectExportInfo,
    Dependency,
    BuildConfig,
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
    xmlAsFile,
    Library,
    Package,
    Task,
    SwDeploymentTable,
    CpuConfig,
    ASProjetGetConfigs,
    batchBuildAsProject,
    buildASProject,
    CreateARSimStructure,
    Project,
    toDict,
)

_warnings.warn(
    "Importing from 'ASTools' is deprecated; use 'aspython' instead "
    "(e.g. 'from aspython import Project').",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = [
    "ASReturnCodes", "PVIReturnCodeText",
    "LibExportInfo", "ProjectExportInfo", "Dependency", "BuildConfig",
    "getASPath", "getASBuildPath", "getPVITransferPath",
    "getActualPathFromLogicalPath", "getAsPathType",
    "convertAsPathToWinPath", "convertWinPathToAsPath",
    "getLibraryPathInPackage", "getLibraryType", "getProgramType", "getPkgType",
    "xmlAsFile", "Library", "Package", "Task", "SwDeploymentTable", "CpuConfig",
    "ASProjetGetConfigs", "batchBuildAsProject", "buildASProject",
    "CreateARSimStructure", "Project", "toDict",
]
