import os
import config
import re

class Script:
    def __init__(self,filepath):
        self.parents = []
        self.path = filepath
        self.filename = os.path.basename(filepath)
        self.dir = os.path.dirname(filepath)
        self.extension = os.path.splitext(filepath)[1][1:]
        self.basename = os.path.splitext(os.path.split(filepath)[1])[0]
        self.parents = []
