"""
Source file parsing filters

The input to these filters is the source file path (absolute or relative),
and the result is some value from the source.
"""

import yaml
from claw.renderer import render

def header(path):
    """Reads and returns a file's header"""
    yamldata = ""
    with open(path, "r") as toread:
        for line in toread:
            if line.rstrip() == "---":
                break
            else:
                yamldata += line
    return yaml.load(yamldata)

def markdown(path):
    """Reads and returns file's markdown source"""
    mddata = ""
    with open(path, "r") as toread:
        begin = False
        for line in toread:
            if line == "---\n":
                begin = True
            elif begin:
                mddata += line
    return mddata

def mdrender(data):
    """Render markdown data"""
    return render(data)

def claw_filters():
    # pylint: disable=missing-docstring
    return [markdown, header, mdrender]
