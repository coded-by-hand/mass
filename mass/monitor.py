import re
import sys
import os
import time
import argparse
import parse
import config
from script import Script

try:
    from fsevents import Observer, Stream
except ImportError:
    from pyinotify import *


def main():
    cmd = sys.argv
    cmd.pop(0)
    """
    parse arguments and make go
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s',
        '--src',
        help='source folder to watch',
        default='.',
        dest='src',
        metavar='folder'
    )
    parser.add_argument(
        '-d',
        '--dest',
        help='source folder to watch',
        default=None,
        dest='dest',
        metavar='folder'
    )
    args = parser.parse_args()
    print 'Initializing...'
    config.source_dir = os.path.abspath(args.src)
    if args.dest != None:
        config.dest_dir = os.path.abspath(args.dest)
    init_sources(config.source_dir)
    if cmd:
        c = cmd[0]
        commands = globals()
        if c in commands:
            commands[c]() 

def compile(): 
    for key,source in config.sources.iteritems():
        if source.extension == config.source_ext:
            parse.parse_file(source)

def watch():
    """
    initialize parameters and start the scanner
    """
    start_scanner(config.source_dir)

def dir_list(dir_name):
    outputList = []
    for root, dirs, files in os.walk(dir_name):
        outputList.append(root)
        for d in dirs:
            outputList.append(''.join([root, d]))
        for f1 in files:
            outputList.append('/'.join([root, f1]))
    return outputList

def init_sources(path):
    """
    initializes array of groups and their associated js files
    """
    for f in dir_list(path):
        if(os.path.splitext(f)[1][1:] == config.source_ext):
            print "Source file discovered: %s" % (f)
            script = Script(f)
            if (script.filename not in config.sources.keys()):
                config.sources[script.path] = script
                parse.parse_dependencies(script,script)

def start_scanner(path):
    """
    watch for file events in the supplied path
    """
    try:
        observer = Observer()
        observer.start()
        stream = Stream(file_modified, path, file_events=True)
        observer.schedule(stream)
        print "Watching for changes. Press Ctrl-C to stop."
        while 1:
          pass
    except (KeyboardInterrupt, OSError, IOError):
        observer.unschedule(stream)
        observer.stop()

def file_modified(event):
    """
    react to file events
    """
    if re.match(config.file_regex,event.name) or (event.name in config.sources.keys()):
        print "Change detected to: %s" % (event.name)
        config.stack = []
        script = config.sources[event.name]
        if script.extension == config.source_ext:
            parse.parse_file(script)
        else:
            parse.parse_parents(script)

if __name__ == "__main__":
    main()
