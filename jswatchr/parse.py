import sys
from script import Script
import re
import jsmin
import os
import config

def parse_file(src):
    """
    find file in config and output to dest dir
    """
    for parent in src.parents:
        if config.dest_dir == None:
            dest = parent.dir
        else:
            dest = config.dest_dir
        output = get_output(parent)
        output_file = dest + '/' + parent.basename + '.min.js'
        f = open(output_file,'w')
        f.write(jsmin.jsmin(output))
        f.close()
        print "Wrote combined and minified file to: %s" % (output_file)

def get_output(src):
    """
    parse lines looking for commands
    """
    output = ''
    lines = open(src.path, 'rU').readlines()
    for line in lines:
        m = re.match(config.import_regex,line)
        if m:
            # TODO: handle user adding a new import line to dependency
            src_file = config.sources[os.path.abspath(src.dir + '/' + m.group('script'))]
            output += get_output(src_file)
        else:
            output += line
    return output

def execute(cmd, line):
    """
    get output from command
    """
    return

def parse_dependencies(script,context):
    lines = open(script.path).read()
    matches = re.finditer(config.import_regex,lines)
    for match in matches:
        # determine file path, recurse
        src = Script(os.path.abspath(script.dir + '/' + match.group('script')))
        if (src.path not in config.sources.keys()):
            src.parents.append(context)
            config.sources[src.path] = src
            parse_dependencies(src,context)
        elif (context not in config.sources[src.path].parents):
            config.sources[src.path].parents.append(context)
