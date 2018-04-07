"""
Globs the given directory and stores the found files in a list

The command takes three parameters, namely target, directory, and glob:
    glob <directory> <target> <glob>
The directory parameter is either source or resource, depending on which you want globbed.
The target parameter is how would you like to call the list in the final context
The glob parameter is the pattern for the glob matches

For example, to find all files in src/posts you could do:
    glob source post_index posts/*.md
And to use this example in a template later, you can:
    ...
    <ul>
        {% for post in post_index %}
            <a href="posts/{{ (post|basename|splitext)[1] }}.html">{{ (post|header).title }}</a>
        {% endfor %}
    </ul>
    ...
And that would result in a list of posts
"""

from glob import glob
from os.path import join
from claw.errors import ClawParserError

def claw_exec(claw, args):
    # pylint: disable=missing-docstring
    if len(args) != 4:
        raise ClawParserError("glob command expects three arguments.")

    if args[1] == "source":
        claw.context[args[2]] = glob(join(claw.source_dir, args[3]))
    elif args[1] == "resource":
        claw.context[args[2]] = glob(join(claw.resource_dir, args[3]))
    else:
        raise ClawParserError("glob's first argument must be one of source or resource")
