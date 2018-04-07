"""
Provides os.path interface for filters
"""

import os.path as p

# pylint: disable=missing-docstring
def basename(path):
    return p.basename(path)

def dirname(path):
    return p.dirname(path)

def relpath(path, start):
    return p.relpath(path, start)

def splitext(path):
    return p.splitext(path)

def claw_filters():
    return [basename, dirname, relpath, splitext]
