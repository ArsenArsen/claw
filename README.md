# claw
An extensible, simple and powerful static website generation framework

## Getting started
To create a sample project you can simply call `claw init`  
Compiling a finished project is as simple as `claw build`

### Clawfile basics
Think about a clawfile like a script, a simple script with a few commands.  
The commands are defined in `claw/interpreter/commands/`, with a few special cases.  
Commands are handled similar to the Unix shell (as in, `shlex` syntax)  
As of now the following commands are available (**bold** means special):

* **`{resource,output,source}_dir`** - Sets the (re)source/output directories
* `template` (`claw/interpreter/commands/cmd_template.py`) - Calls the template processor and processes all files provided in the first argument with the template in the second one. The file argument is a glob relative to `source_dir`, and the template is relative to `resource_dir`. Example: `template **/*.md page.tml` will render all markdown files in the source directory using `$resource_dir/page.tml`
* `print` (`claw/interpreter/commands/cmd_print.py`) - Equivalent to `echo` in the Unix shell
* `static` (`claw/interpreter/commands/cmd_static.py`) - Copies all files in `resource_dir` matching the provided glob into `output_dir/static/`
* `glob` (`claw/interpreter/commands/cmd_glob.py`) - Finds all files matching the glob (second argument) in the directory (first argument) and stores the resulting list in template variables under the name provided in the third argument. Example: `glob source posts/*.md post_index`. It is worth noting that the directory argument is either source or resource, to switch between the source and resource directory.

### Provided Jinja2 filters
Claw provides some additional Jinja2 filters (defined in `claw/filters/`).

Currently, by default, there are two filter categories: path and source parse filters.  
Path filters are just mapping a few `os.path` methods into Jinja2 filters.  
The source parse category provides two flters: `header` and `markdown`, which read the header and the markdown parts of a source file, respectively.  
Both of these filters take only a path argument.
