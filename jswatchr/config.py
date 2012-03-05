import re
# what file extensions should we monitor
source_ext = 'xjs'
exts = ['js', source_ext]
# TODO: support ignoring pre-minified and output files
#ignore_exts = ['min.js']
sources = {}
source_dir = None
dest_dir = None
import_regex = '(?P<command>@import|@require) (?P<script>\S+(.\S+)(?!.min)(.xjs|.js))'
file_regex = '([a-zA-Z/]*.(?!min)(xjs|js))'
