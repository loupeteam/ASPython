# ASPython

Python toolkit for programmatic interaction with B&R Automation Studio projects.

Provided by [Loupe](https://loupe.team) · info@loupe.team · 1-800-240-7042

---

## Overview

ASPython (`aspython`) is a Python package that provides both a **command-line interface** and a **Python API** for automating common Automation Studio workflows: building configurations, managing libraries, creating simulators, packaging HMIs, running unit tests, and more.

---

## Requirements

- Python 3.8+
- B&R Automation Studio installed (required for build/sim operations)
- Windows (Automation Studio is Windows-only)

---

## Installation

Install from source in editable mode (recommended for development):

```bash
pip install -e .
```

Install with optional CNC support (requires `lxml`):

```bash
pip install -e .[cnc]
```

Install with all development dependencies (testing, linting, packaging):

```bash
pip install -e .[dev]
```

After installation the `aspython` command is available on your PATH.

---

## CLI Reference

```
aspython <command> [options]
aspython --help
aspython <command> --help
```

Global flags available on every subcommand:

| Flag | Description |
|------|-------------|
| `-l`, `--logLevel` | Log verbosity: `DEBUG`, `INFO`, `WARNING`, `ERROR` (default: `WARNING`) |
| `-v`, `--version` | Print the installed version and exit |

### `aspython build`

Build one or more configurations of an AS project.

```
aspython build <project> -c <config> [<config> ...] [options]
```

| Argument | Description |
|----------|-------------|
| `project` | Path to the AS project |
| `-c`, `--configuration` | One or more AS configuration names to build (required) |
| `-bm`, `--buildMode` | Build mode: `Build` (default), `Rebuild`, `BuildAndTransfer`, `BuildAndCreateCompactFlash`, `None` |
| `-rp`, `--buildRUCPackage` | Disable building the RUC package |
| `-sim`, `--simulation` | Build for simulation |
| `-pip` | Generate a PIP (`.tar.gz`) after build completes |

### `aspython arsim`

Build (optionally) and create an ARsim package for an AS project.

```
aspython arsim <project> -c <config> [<config> ...] [options]
```

| Argument | Description |
|----------|-------------|
| `project` | Path to the AS project |
| `-c`, `--configuration` | One or more AS configuration names (required) |
| `-bm`, `--buildMode` | Build before packaging: `None` (default, skip build), `Build`, `Rebuild`, etc. |
| `-ss`, `--startSim` | Start ARsim after creating the package |
| `-uf`, `--userFiles` | Path to a folder of user partition files to include |
| `-hf`, `--hmiFiles` | Path to a folder of HMI files to include |

Output is written to `<project>/Temp/SIM/<config>/Simulator.tar.gz`.

### `aspython export-libs`

Export libraries from an AS project in binary or source format.

```
aspython export-libs <project> -c <config> [<config> ...] [options]
```

| Argument | Description |
|----------|-------------|
| `project` | Path to the AS project |
| `-c`, `--configuration` | One or more AS configuration names (required) |
| `-dest`, `--destination` | Export destination path (default: `../Exports` relative to project) |
| `-wl`, `--whitelist` | Export only these libraries (overrides blacklist) |
| `-bl`, `--blacklist` | Skip libraries matching these glob patterns |
| `-o`, `--overwrite` | Overwrite previously-exported libraries |
| `-source`, `--sourceFile` | Export as source instead of binary |
| `-bm`, `--buildMode` | Build before exporting (default: `None`) |
| `-iv`, `--includeVersion` | Include version number in the folder structure |

### `aspython deploy-libs`

Deploy libraries into a cpu.sw deployment table.

```
aspython deploy-libs -d <cpu.sw> -lf <library-folder> [options]
```

| Argument | Description |
|----------|-------------|
| `-d`, `--deploymentFile` | Path to the `cpu.sw` file (required) |
| `-lf`, `--libraryFolder` | Folder containing the libraries to deploy (required) |
| `-lib`, `--libraries` | Specific library names to deploy (default: all libraries in the folder) |

### `aspython safety-crc`

Retrieve the CRC of a B&R Safe Application from a built project.

```
aspython safety-crc <project> -c <config> -sa <safe-app>
```

| Argument | Description |
|----------|-------------|
| `project` | Path to the AS project |
| `-c`, `--configuration` | AS configuration name (required) |
| `-sa`, `--safeApp` | Safe application name (e.g. `MySafeApp.SafAPP`) (required) |

Prints the CRC value to stdout.

### `aspython version`

Read a project's build version from a `.var` file.

```
aspython version <project> -bi <buildInfo.var> [options]
```

| Argument | Description |
|----------|-------------|
| `project` | Path to the AS project |
| `-bi`, `--buildInfo` | Path to the buildInfo `.var` file (required) |
| `--semver` | Return the version in Semantic Version format |

Prints the version string to stdout.

### `aspython installer`

Generate a Windows installer (`.exe`) from an Inno Setup `.iss` script.

```
aspython installer <script.iss> -o <output> -an <appName> [options]
```

| Argument | Description |
|----------|-------------|
| `script` | Path to the `.iss` script (required) |
| `-o`, `--output` | Destination folder for the compiled installer (required) |
| `-an`, `--appName` | Application name (required) |
| `-av`, `--appVersion` | Application version (default: `1.0.0`) |
| `-ap`, `--appPublisher` | Publisher name (default: `Loupe`) |
| `-au`, `--appUrl` | Publisher URL (default: `https://loupe.team`) |
| `-sd`, `--simDir` | Directory containing simulation assets |
| `-ud`, `--userDir` | Directory containing user partition assets |
| `-jb`, `--junctionBatch` | Junction batch filename (default: `ConnectFileDevice.bat`) |
| `-hd`, `--hmiDir` | Directory containing HMI assets |
| `-he`, `--hmiExe` | HMI executable filename |

### `aspython package-hmi`

Package a Loupe UX-based HMI using electron-packager.

```
aspython package-hmi -s <source> -o <output> -an <appName> [options]
```

| Argument | Description |
|----------|-------------|
| `-s`, `--source` | Source folder containing the HMI `package.json` (required) |
| `-o`, `--output` | Destination folder for packaged files (required) |
| `-an`, `--appName` | Application name (required) |
| `-av`, `--appVersion` | Application version (default: `1.0.0`) |
| `-ap`, `--appPublisher` | Publisher name (default: `Loupe`) |
| `--installElectronPackager` | Install electron-packager before packaging |

### `aspython run-tests`

Run unit tests against a PLC test server and write JUnit-style XML results.

```
aspython run-tests <host> -d <destination> [options]
```

| Argument | Description |
|----------|-------------|
| `host` | IP address of the PLC running the test server (required) |
| `-d`, `--destination` | Directory to write test result XML files (required) |
| `-a`, `--all` | Run all available tests |

---

## Python API

The package exposes a public API that can be imported directly:

```python
from aspython import Project, Library, Package, BuildConfig
```

### `Project`

The main entry point for working with an AS project.

```python
project = Project('/path/to/MyProject')

# Build a configuration
result = project.build('MyConfig', buildMode='Build')

# Export libraries
results = project.exportLibraries('/path/to/exports', buildConfigs=[...])

# Create an ARsim package
project.createSim('MyConfig', destination='/path/to/sim')

# Create a PIP
project.createPIP('MyConfig', '/path/to/pip')

# Read a constant from a .var file
version = project.getConstantValue('path/to/buildInfo.var', 'versionId')

# Read a value from an .ini file
crc = project.getIniValue('relative/path/to/CPU.ini', 'CRC', 'PROJECT')
```

Key properties:

| Property | Description |
|----------|-------------|
| `project.dirPath` | Absolute path to the project directory |
| `project.tempPath` | Absolute path to the project's `Temp` directory |
| `project.buildConfigs` | List of `BuildConfig` objects for each AS configuration |

### `Library`

Represents an Automation Studio library.

```python
from aspython import Library
lib = Library('/path/to/MyLibrary')
```

### `Package`

Represents an AS logical package (`.pkg` file).

### `BuildConfig`

Represents a build configuration within a project.

```python
for config in project.buildConfigs:
    print(config.name)
```

### `SwDeploymentTable`

Read and modify a `cpu.sw` software deployment table.

```python
from aspython import SwDeploymentTable
table = SwDeploymentTable('/path/to/cpu.sw')
table.deployLibrary('/path/to/libs', 'MyLibrary')
```

### Path utilities

```python
from aspython import (
    getASPath,
    getASBuildPath,
    convertAsPathToWinPath,
    convertWinPathToAsPath,
)
```

---

## Legacy compatibility

The legacy `CmdLine*.py` scripts and the `import ASTools` pattern continue to work as deprecation shims. Prefer the `aspython` CLI and package API for new code.

| Legacy | Current |
|--------|---------|
| `python CmdLineBuild.py` | `aspython build` |
| `python CmdLineARSim.py` | `aspython arsim` |
| `python CmdLineExportLib.py` | `aspython export-libs` |
| `python CmdLineDeployLibraries.py` | `aspython deploy-libs` |
| `python CmdLineGetSafetyCrc.py` | `aspython safety-crc` |
| `python CmdLineGetVersion.py` | `aspython version` |
| `python CmdLineCreateInstaller.py` | `aspython installer` |
| `python CmdLinePackageHmi.py` | `aspython package-hmi` |
| `python CmdLineRunUnitTests.py` | `aspython run-tests` |

---

## Development

Run the test suite:

```bash
pytest
```

Lint:

```bash
ruff check .
```

---

## Licensing

This project is licensed under the [MIT License](LICENSE).
