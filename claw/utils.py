"""Claw helper functions"""

from importlib import util as iul
from os.path import join, dirname, realpath, relpath, isdir
from os import unlink, listdir, sep, linesep
from shutil import rmtree
import sys

def import_module(path: str):
    """Utility function to load up and import a module"""
    name = relpath(path, dirname(dirname(realpath(__file__))))
    name = name.replace(sep, ".")[:-3]
    spec = iul.spec_from_file_location(name, path)
    mod = iul.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# Taken from PEP
# https://www.python.org/dev/peps/pep-0257/
def trim_docstring(docstring: str):
    """
    Handles trimming docstrings, according to the PEP

    https://www.python.org/dev/peps/pep-0257/
    """
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxsize
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxsize:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)

def indent_block(text: str, indent="\t", count=1):
    """Indents a block of text"""
    return linesep.join([(indent*count + line).rstrip() for line in text.splitlines()])

def clean_directory(directory: str):
    """Cleans a directory but keeps the directory itself"""
    for filename in listdir(directory):
        path = join(directory, filename)
        if isdir(path):
            rmtree(path)
        else:
            unlink(path)
