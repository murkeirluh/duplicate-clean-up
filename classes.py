from datetime import datetime

DEBUG = False

def debug(x):
    if DEBUG:
        print(x)

class Config:
    def __init__(self, loc=None, ft=None, c=None):
        self.location = loc or None
        self.filetype = ft or None
        self.fileattr = c or None
        self.check()
        self.log()

    def set_location(self, loc):
        self.location = loc

    def set_filetype(self, ft):
        self.filetype = ft
    
    def set_fileattr(self, c):
        self.fileattr = c

    def get_fileattr(self):
        return self.fileattr

    def get_location(self):
        return self.location
    
    def get_filetype(self):
        return self.filetype

    def check(self):
        debug(self)
    
    """ Log config to file """
    def log(self):
        with open('logs/main.log', 'r+') as l:
            i = int(l.read())
        
        try:
            with open('logs/' + str(i) + '.config', 'x') as c:
                c.write(str(datetime.now()) + '\n\n')
                c.write("Location: " + self.location + '\n')
                c.write("File type: ")
                for f in self.filetype:
                    c.write(f)
                    if f != self.filetype[-1]:
                        c.write(", ")
                    else:
                        c.write('\n')
                c.write("File attributes: ")
                for f in self.fileattr:
                    c.write(f)
                    if f != self.fileattr[-1]:
                        c.write(", ")
                    else:
                        c.write('\n')
        except Exception as e:
            debug(e)
        
        with open('logs/main.log', 'w') as l:
            l.write(str(i+1))
        
        debug("Successfully logged to file")

    def __str__(self):
        return '<' + str(self.location) + ', ' +  str(self.filetype) + ', ' + str(self.fileattr) + '>'

    def __repr__(self):
        return '<' + str(self.location) + ', ' +  str(self.filetype) + ', ' + str(self.fileattr) + '>'
    

""" A File object """
class File:
    def __init__(self, name, ext, path, ft, created=None, mod=None):
        self.name = name
        self.ext = ext
        self.path = path
        self.file_type = ft
        self.modified = mod or None
        self.created = created or None

    def __str__(self):
        return '<' + self.name + '>'
    
    def __repr__(self):
        return '<' + self.name + '>'

    def __eq__(self, other):
        return (self.name == other.name and self.ext == other.ext and self.path == other.path and self.file_type == other.file_type)

    def __hash__(self):
        return hash((self.name, self.ext, self.path, self.file_type))

""" Groups of File objects """
class FileGroup:
    def __init__(self, group_id=None, fileset=None, length=None):
        self.group_id = group_id or 0
        self.fileset = fileset or []
        self.length = length or 0

    def set_id(self, i):
        self.group_id = i

    def get_files(self):
        print('GROUP_ID\t\tFILENAME\t\t\t\t\tPATH\n')
        for f in self.fileset:
            print('  ', self.group_id, "\t\t", f.name[:25] + '...\t\t', f.path)
            print()
    
    """ Integrity check """
    def check(self):
        for i in range(self.length):
            for j in range(i+1, self.length):
                current = self.fileset[i]

    def add_files(self, *files):
        self.fileset.extend(list(files))
        self.length += len(list(files))

    def __repr__(self):
        return str(self.fileset)
    
    def __str__(self):
        return str(self.fileset)

    def __len__(self):
        return self.length
    

loading = ['/', '-', '\\', '|']