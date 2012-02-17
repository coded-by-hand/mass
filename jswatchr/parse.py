import jsmin
import os
# perform action on matched file
def parse_file(groups, src, dest):
    """
    parse arguments and make go
    """
    for (group,scripts) in groups:
        if src in scripts:
            #split extension off of file
            (root,ext) = os.path.splitext(group)
            #split root into path,group name
            (source_path,group_name) = os.path.split(root)
            #if destination directory was defined in CLI use it, otherwise place next to xjs file
            if dest == None:
                dest = source_path
            min_scripts = '';
            for script in scripts:
                #open file and minify
                js = open(script).read()
                min_scripts += js
            output_file = dest + '/' + group_name + '.min.js'
            f = open(output_file,'w')
            f.write(jsmin.jsmin(min_scripts))
            f.close()
            print "Wrote combined and minified file to: %s" % (output_file)
