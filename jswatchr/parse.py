from script import Script
import re
import jsmin
import os
import config

cmds = ['@import'] # TODO: support other commands '@require'

def parse_file(src):
    """
    find file in config and output to dest dir
    """
    for (master,scripts) in config.sources:
        if src == master or src in scripts:
            # split extension off of file
            (root,ext) = os.path.splitext(master)
            # split root into path, base file name
            (source_path,base_file) = os.path.split(root)
            # if destination directory was defined in CLI use it, otherwise place next to xjs file
            if config.dest_dir == None:
                dest = source_path
            else:
                dest = config.dest_dir
            output = get_output(master)
            output_file = dest + '/' + base_file + '.min.js'
            f = open(output_file,'w')
            f.write(jsmin.jsmin(output))
            f.close()
            print "Wrote combined and minified file to: %s" % (output_file)

def get_output(src):
    """
    parse lines looking for commands
    """
    output = ''
    lines = open(src, 'rU').readlines()
    for line in lines:
        segs = line.split()
        if len(segs) > 0 and segs[0] in cmds:
            # determine file path, recurse
            (source_path,base_file) = os.path.split(src)
            # TODO: handle user adding a new import line to dependency
            # file, need to rebuild config.sources for this 'master'
            output += get_output(os.path.abspath(source_path + '/' + segs[1]))
        else:
            output += line
    return output

def execute(cmd, line):
    """
    get output from command
    """
    return

def compile(output, src, dest):
    """
    write minified compiled output to dest
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
