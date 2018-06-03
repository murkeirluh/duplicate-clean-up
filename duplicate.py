#! python3
""" Duplicate Clean-up v.1.0 """

import os
import re

DEBUG = True

def debug(x):
    if DEBUG:
        print(x)

class Config:
    def __init__(self, loc):
        self.location = loc or None
        self.filetype = ft or None
        self.criteria = c or None
        check()

    def set_location(self, loc):
        self.location = loc

    def set_filetype(self, ft):
        self.filetype = ft
    
    def set_criteria(self, c):
        self.criteria = c

    def check(self):
        debug(self)
    
    def __str__(self):
        return '<' + self.location, self.filetype, self.criteria + '>'

    def __repr__(self):
        return '<' + self.location, self.filetype, self.criteria + '>'
    

""" A File object """
class File:
    def __init__(self):
        self.name = ''
        self.path = ''
        self.modified = ''
        self.created = ''
        self.file_type = ''
    
    def create(self, name, path, ft, created=None, mod=None):
        self.name = name
        self.path = path
        self.file_type = ft
        self.modified = mod or None
        self.created = created or None

    def __str__(self):
        return '<' + self.name + '>'
    
    def __repr__(self):
        return '<' + self.name + '>'

""" Groups of File objects """
class FileGroup:
    def __init__(self):
        self.group_id = 0
        self.fileset = []
        self.length = 0

    def set_id(self, i):
        self.group_id = i
    
    def set_config(self, files):
        # if input is a list, assign to fileset
        if str(type(files)) == "<class 'list'>":
            self.fileset = files
            self.length = len(self.fileset)
        elif bool(re.search("([\w \.]+(\, )?)+", files)):
            f = files.split(", ")
            self.fileset = f
            self.length = len(self.fileset)
        check()
    
    """ Integrity check """
    def check(self):
        for i in range(self.length):
            for j in range(i+1, self.length):
                current = self.fileset[i]


            

    