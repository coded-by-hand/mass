# what file extensions should we monitor
source_ext = 'xjs'
exts = ['js', source_ext]
# TODO: support ignoring pre-minified and output files
sources = {}
source_dir = None
dest_dir = None
import_regex = '(//(\s*)(?P<command>import|require)) (\"|\')?(?P<script>\S+(.\S+)(.xjs|.js))(\"|\')?'
file_regex = '([a-zA-Z/]*.(?!min)(xjs|js))'
stack = []
