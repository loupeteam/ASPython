"""AS CNC configuration helpers (requires the optional ``lxml`` dependency)."""

try:  # pragma: no cover - import guard
    import lxml.etree as ET
except ModuleNotFoundError:  # pragma: no cover - import guard
    ET = None


def listOfProcs(tree, include_comments: bool = False):
    if ET is None:
        raise ModuleNotFoundError(
            "aspython.cnc requires the optional 'lxml' dependency. Install it with "
            "'pip install lxml'."
        )
    procs = []
    for node in tree.xpath('//BuiltInProcs'):
        for child in node:
            if child.tag is not ET.Comment:
                if include_comments and child.getprevious() is not None and child.getprevious().tag is ET.Comment:
                    procs.append(child.getprevious())
                procs.append(child)
    return procs
