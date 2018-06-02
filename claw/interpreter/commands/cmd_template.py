"""
Compiles all files matching a glob and puts them into the output directory.

The command will loop over all files matching a provided glob, compile them with markdown,
and insert them into the template's `body' slot,
while also providing the values of all variables defined in the header to the templating engine.

An example of an input file would be:
    title: My Very Own Website
    ---
    # My Website
    Welcome to my website!
    ##### h5

With an example template:
    <head><title>{{ title }}</title></head>
    <body>{{ body }}</body>

Would result in:
    <head><title>My Very Own Website</title></head>
    <body><h1>My Website</h1>
    <p>Welcome to my website!</p>
    <h5>h5</h5></body>
"""
# pylint: disable=invalid-name,W0702,W0622

from glob import glob
from os import makedirs
from os.path import dirname, join, relpath, realpath, splitext
import yaml
from claw.errors import ClawParserError
from claw.renderer import render

def claw_exec(claw, args):
    """Does the templating"""
    if len(args) != 3:
        raise ClawParserError("template takes two arguments. template <source_glob> <template_in>")
    files = glob(join(claw.source_dir, args[1]))
    for file in files:
        output_file = splitext(join(claw.output_dir, relpath(file, claw.source_dir)))[0] + ".html"
        makedirs(dirname(output_file), exist_ok=True)
        markdown_data = ""
        header_data = ""
        with open(file, "r") as input:
            writing_header = True
            for line in input:
                if line.strip() == "---":
                    writing_header = False
                    continue
                if writing_header:
                    header_data += line
                else:
                    markdown_data += line

        header = yaml.load(header_data)
        if not header:
            header = {}
        header["body"] = render(markdown_data)
        header["file"] = realpath(file)
        header = {**claw.context, **header}
        with open(join(claw.resource_dir, args[2]), "r") as template:
            with open(output_file, "w") as output:
                output.write(claw.jinja.from_string(template.read()).render(header))
