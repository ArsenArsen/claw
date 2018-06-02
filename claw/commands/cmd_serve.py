"""
Sparks a simple HTTP server to serve a compiled output.

Please note that this command will not compile the output.

Usage: serve [--bind ADDRESS] [port]

Positional arguments:
    port        The port to run the server on

Optional arguments:
    --bind ADDRESS, -b ADDRESS
                The address to bind to [default: all interfaces]
"""
# pylint: disable=missing-docstring,invalid-name,unused-argument

import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler
from functools import partial
from os import chdir

def claw_exec(claw):
    args = argparse.ArgumentParser(add_help=False)
    args.add_argument("port", type=int, default=8080, nargs='?')
    args.add_argument("--bind", "-b", default="", type=str)
    p = args.parse_args(claw.args[1:])
    addr = (p.bind, p.port)
    chdir(claw.output_dir)
    with HTTPServer(addr, SimpleHTTPRequestHandler) as httpd:
        sa = httpd.socket.getsockname()
        serve_message = "Serving HTTP on {host} port {port} (http://{host}:{port}/) ..."
        print(serve_message.format(host=sa[0], port=sa[1]))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")

def claw_help(claw, short=False):
    return "Serve the output" if short else __doc__
