#! python3
""" Duplicate Clean-up v.1.0 """

from datetime import datetime
from collections import defaultdict
import os
import re
import time
import sys
from classes import Config, File, FileGroup, loading

DEBUG = True
CONFIG = ''

def debug(x):
    if DEBUG:
        print(x)

def get_config():
    if CONFIG != '':
        return CONFIG
    else:
        return -1

""" Checks if criteria for file1 and file2 matches """
def match(file1, file2):
    c = get_config()
    if c:
        integ = True
        criteria = c.get_fileattr()
        for cr in criteria:
            if cr == 'mod_date':
                if file1.modified != file2.modified:
                    integ = False
                    break
            elif cr == 'create_date':
                if file1.created != file2.created:
                    integ = False
                    break
            elif cr == 'same_name':
                if file1.name != file2.name:
                    integ = False
                    break
        return integ
    else:
        raise Exception("No config file has been set.")

""" search for duplicates """
def search(config):
    # file types
    extensions = defaultdict(list)
    extensions = {
        'image' : ['.png', '.jpg', '.jpeg', '.bmp', '.gif'],
        'audio' : ['.wav', '.aif', '.mp3', '.mid']
    }
    
    extensions['regular'] = extensions['image'] + extensions['audio']
    audio_ext = extensions['audio']
    image_ext = extensions['image']
    reg_ext = False
    all_ext = False

    def check_ft(t):
        if t in audio_ext:
            return 'audio'
        elif t in image_ext:
            return 'image'
        else:
            return 'regular'
    
    loc = config.get_location()
    filetype = config.get_filetype()
    fileattr = config.get_fileattr()
    if not(os.path.exists(loc)):
        raise Exception("Location does not exist")
        return

    # file type settings
    ext_domain = []
    if 'audio' in filetype and 'image' in filetype and 'regular' in filetype:
        all_ext = True
    else:
        if 'audio' in filetype:
            ext_domain.extend(audio_ext)
        if 'image' in filetype:
            ext_domain.extend(image_ext)
        if 'regular' in filetype:
            reg_ext = True

    files_list = []
    
    ## START
    for root, dirs, files in os.walk(loc):
        i = 0
        sys.stdout.write("\rSearching at {} ... ".format(str(root)))
        sys.stdout.flush()
        time.sleep(0.5)
        for f in files:
            i += 1
            filename, file_ext = os.path.splitext(f)
            mod_date = time.ctime(os.path.getmtime(os.path.join(root, f)))
            create_date = time.ctime(os.path.getctime(os.path.join(root, f)))
            # print(os.path.join(root, f), '\t', mod_date, create_date)
            
            # if all file extensions to be checked
            if all_ext:
                files_list.append(File(filename, file_ext, root, check_ft(file_ext), created=create_date, mod=mod_date))
            else:
                # add file to list if regular file-checking is enabled and file ext is not audio/image
                # or if file ext is in domain of ext to be checked
                if (reg_ext and file_ext not in extensions['regular']) or (file_ext in ext_domain):
                    files_list.append(File(filename, file_ext, root, check_ft(file_ext), created=create_date, mod=mod_date))
            
        print('done')

    group_id = 1
    duplicates = []
    for i in range(len(files_list)):
        if files_list[i]:
            current = files_list[i]
            # print("\ncurrent:", current, end="\n\n")
            temp_fg = FileGroup(group_id=group_id)
            temp_fg.add_files(current)
            for j in range(i+1, len(files_list)):
                if files_list[j]:
                    # print("\tcomp:", files_list[j], end=' ')
                    matched = match(current, files_list[j])
                    # print(matched)
                    if matched:
                        temp_fg.add_files(files_list[j])
                        files_list[j] = None
            if len(temp_fg) > 1:
                duplicates.append(temp_fg)
                group_id += 1

    print()
    for d in duplicates:
        d.get_files()

    print("\n\nSearch done.")






    
    
         
if __name__ == '__main__':
    # variables
    criteria = {
        'audio' : False,
        'image' : False,
        'regular' : False,
        'mod_date' : False,
        'create_date' : False,
        'same_name' : False
    }

    inp_dict = {
        '1a' : 'audio',
        '1b' : 'image',
        '1c': 'regular',
        '3a' : 'mod_date',
        '3b': 'create_date',
        '3c' : 'same_name'
    }

    # Welcome screen
    print("\n#####################################")
    print("\nWelcome to Duplicate Clean-up v. 1.0\n")
    print("#####################################\n")
    print("Configure your settings below:\n")
    print("1. File type to scan for")
    print("\ta. audio\n\tb. image\n\tc. regular\n")
    print("(Press enter to check all.)")

    k = 0
    while True:
        menu = '1'
        i = input()
        if i:
            # debug(inp_dict)
            criteria[inp_dict[menu + str(i)]] = True
            # debug(criteria)
            k += 1
        else: 
            if k == 0:
                criteria[inp_dict[menu + 'a']] = True
                criteria[inp_dict[menu + 'b']] = True
                criteria[inp_dict[menu + 'c']] = True
                print("Selected all.\n")
                break
            else:
                break

    print("2. Location to search in\n")

    path = input()
    while not(os.path.exists(path)):
        print("Location doesn't exist!\n")
        path = input()

    print("Selected " + path + " as search location.")
    criteria['location'] = path

    print("\n3. Criteria for scan")
    print("\ta. Same date modified\n\tb. Same date created\n\tc. Same file name")

    k = 0
    while True:
        menu = '3'
        i = input()
        if i:
            # debug(inp_dict)
            criteria[inp_dict[menu + str(i)]] = True
            # debug(criteria)
            k += 1
        else: 
            if k == 0:
                criteria[inp_dict[menu + 'a']] = True
                criteria[inp_dict[menu + 'b']] = True
                criteria[inp_dict[menu + 'c']] = True
                print("Selected all.\n")
                break
            else:
                break

    print("Your setting is as follows:")
    for k, v in criteria.items():
        if v:
            print(k, v)
    ## confirmation message ##

    # create config file
    loc = criteria['location']
    ft = [k for k, v in list(criteria.items())[:3] if v]
    c = [k for k, v in list(criteria.items())[3:-1] if v]
    CONFIG = Config(loc, ft, c)

    print("\n")
    search(CONFIG)
