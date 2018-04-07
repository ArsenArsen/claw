"""
Transfers a static file over into the output static folder

This command takes one argument,
which is the resource glob to insert into the statics folder.

Examples:
    static style.css
Would result in style.css in output/static/style.css
    static *.png
Would result in all png files being copied to output/static/
"""

from os import makedirs as mkdirs
from os.path import relpath, join, dirname
from shutil import copy
from glob import glob
from claw.errors import ClawParserError

def claw_exec(claw, args):
    """Copies the static resource"""
    if len(args) != 2:
        raise ClawParserError("static command did not receive exactly one argument")
    for f in glob(join(claw.resource_dir, args[1])):
        f = relpath(f, claw.resource_dir)
        source = join(claw.resource_dir, f)
        target = join(claw.output_dir, "static/", f)
        mkdirs(dirname(target), exist_ok=True)
        copy(source, target)
