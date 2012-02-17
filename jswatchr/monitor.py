import os
import time
import argparse
import jsmin
from fsevents import Observer, Stream

# what file extensions should we monitor
source_ext = 'xjs'
exts = ['js', source_ext]
groups = []
source_dir = ''
dest_dir = ''

def main():
    global source_dir
    global dest_dir
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
    """
    initialize parameters and start the scanner
    """
    print 'Initializing...'
    source_dir = os.path.abspath(args.src)
    if args.dest != None:
        dest_dir = os.path.abspath(args.dest)
    init_sources(source_dir)
    start_scanner(source_dir)

def dir_list(dir_name):
    outputList = []
    for root, dirs, files in os.walk(dir_name):
        outputList.append(root)
        for d in dirs:
            outputList.append(''.join([root, d]))
        for f1 in files:
            outputList.append('/'.join([root, f1]))
    return outputList

def init_group(group):
    global groups
    group_config = open(group);
    scripts = []
    for line in group_config.readlines():
        segs = line.split()
        if segs[0] == '@import':
            scripts.append(os.path.abspath(os.path.dirname(group) + '/' + segs[1]))
    groups.append((group,scripts))

def init_sources(path):
    """
    initializes array of groups and their associated js files
    """
    global groups
    global source_ext
    for f in dir_list(source_dir):
        if(os.path.splitext(f)[1][1:] == source_ext):
            print "Source file discovered: %s" % (f)
            init_group(f)

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
    path, ext = os.path.splitext(event.name)
    if ext[1:] in exts:
        print "Change detected to: %s" % (event.name)
        parse_file(path + ext)

# perform action on matched file
def parse_file(path):
    """
    parse arguments and make go
    """
    global source_dir
    global dest_dir
    for (group,scripts) in groups:
        if path in scripts:
            if dest_dir == '':
                rel_dest = os.path.dirname(group)
            else:
                rel_dest = dest_dir
            group_name = os.path.basename(os.path.splitext(group)[0])
            minify_scripts = '';
            for script in scripts:
                #open file and minify
                js = open(script).read()
                minify_scripts += js
            group_file = group_name + '.min.js'
            f = open(group_file,'w')
            f.write(jsmin.jsmin(minify_scripts))
            f.close()
            print "Wrote combined and minified file to: %s" % (rel_dest + '/' + group_file)

if __name__ == "__main__":
    main()
