#!/usr/bin/env python3
"""
Claw is a website compiler built to be light, fast, and modern.

The idea behind claw is to just do it.
Claw takes an input folder, such as:
    /
    +-- /src
    |   +-- /index.md                   --> output/index.html
    |   +-- /posts
    |       +-- /posts/hello-world.md   --> output/posts/hello-world.html
    |       +-- /posts/how-are-ya.md    --> output/posts/how-are-ya.html
    +-- /Clawfile
    +-- /resources
        +-- index.tml
        +-- post.tml
        +-- style.css                   --> output/static/style.css

An example Clawfile would be:
    template index.md index.tml
    template posts/* post.tml
    static *.css

Compilation is as simple as `claw build'
You can take /output and slap it in your nginx server

Default project directory is the current working directory but it can be changed with -c
"""

from claw.claw import main

if __name__ == "__main__":
    main()
