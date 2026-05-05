# Change log

- 0.3.0   - Major maintainability refactor
            - Split `ASTools.py` into a proper `aspython` package (`project`, `library`, `package`, `task`, `deployment`, `config`, `build`, `simulation`, `paths`, `models`, `xml_base`, `returncodes`, `utils`, `installer`, `hmi`, `unittests`, `upgrades`, `cnc`, `logging_setup`)
            - Unified the nine `CmdLine*.py` scripts behind a single `aspython` CLI with subcommands (`build`, `arsim`, `export-libs`, `deploy-libs`, `safety-crc`, `version`, `installer`, `package-hmi`, `run-tests`); legacy `CmdLine*.py` scripts kept as deprecation shims
            - Added `pyproject.toml` with console_scripts entry point, dev extras, and a PyInstaller spec under `packaging/`
            - Added `tests/` (pytest) covering imports, dataclass models, path helpers, and CLI dispatch
            - Added GitHub Actions CI for Windows
            - Backwards-compatible: `import ASTools` and `python CmdLineXxx.py …` still work and emit `DeprecationWarning`

- 0.2.2   - Adapt SW task element's path to be relative to Logical

- 0.2.1   - Fix logical path to actual path functions

- 0.2.0   - Add support for referenced libraries 
          - Improve install upgrades script
            - Fix install upgrades
            - Add recursive option
            - Add default base path for Automation Studio
            - Allow AS Version path to just be version folder name. In this case it will use Automation Studio base path as a prefix
          - Fix User and HMI files in ARSim cmd line interface 
          - Update webHMI references to Loupe UX

- 0.1.1   - Add support for including user partition and HMI files in Simulator.tar.gz

- 0.1.0   - Release (Synchronize and consolidate all script versions)

- 0.0.2   - Release

- 0.0.1.9 - Fix binary library exports including cpp files 

- 0.0.1.8 - Fix relative project paths failing during builds
          - Refactor code and deprecate some functions

- 0.0.1.7 - Renamed package to ASTools
          - Fix logging would sometimes produce invalid characters

- 0.0.1.6 - Add colors to output
          - Add build.log for AS results
          - Fix some bugs related to AS builds

- 0.0.1.5 - Fix binary library exports .lby file still containing some .c and .st files 

- 0.0.1.4 - Add support for AS4.X instead of just 4.5

- 0.0.1.3 - Add build option 'None'

- 0.0.1 - Initial version