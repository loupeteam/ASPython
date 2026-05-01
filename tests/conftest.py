import sys
from pathlib import Path

# Make the repo-root packages importable when running ``pytest`` without an editable install.
_repo_root = Path(__file__).resolve().parent.parent
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))
