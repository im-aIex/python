from os import listdir, remove, renames, makedirs
from os.path import isfile, isdir, join, getsize
from shutil import rmtree, copyfileobj

def list_dir(directory):
    return listdir(directory)

def read(directory):
    f = open(directory)
    return f.read()

def write(directory, content):
    f = open(directory, 'w')
    f.write(content)
    return

def get_url(parts):
    temp = ''
    for part in parts:
        temp += part + '/'
    return temp

def is_file(directory):
    return isfile(directory)

def is_dir(directory):
    return isdir(directory)

def delete(directory):
    if(is_file(directory)):
        remove(directory)
    else:
        rmtree(directory)

def rename(file_old, file):
    file = '/'.join(file_old.split('/')[:-1]) + '/' + file
    renames(file_old, file)

def upload(input_file, url, filename):
    file_path = join(url, filename)
    with open(file_path, 'wb') as output_file:
        copyfileobj(input_file, output_file)

def make_dir(dir_name, url):
    if not isdir(url + dir_name):
        makedirs(url + dir_name)

def size(directory):
    return getsize(directory)

def fix_cal(year, month, info):
    file = open('/media/storage/site/data/calendar.txt')
    file_info = list()
    final_cal = ()
    replace = False
    delete = False
    year_found = False
    for line in file:
        file_info += (line,)
    for part in file_info:
        if part[:1] == '+':
            final_cal += (part,)
            if part[1:-1] == year + '':
                year_found = True
                replace = True
                continue
            continue
        elif replace:
            if part[:2] == '//':
                if part[2:-1] == month:
                     delete = True
                elif part[2:-1] > month:
                    replace = False
                    delete = False
                    for p in info:
                        final_cal += (p + '\n',)
                    final_cal += (part,)
                    continue
                final_cal += (part,)
                continue
            elif delete:
                continue
        final_cal += (part,)
    if not year_found:
        final_cal += ('+' + year + '\n',)
        for i in range(12):
            final_cal += ('//' + str(i) + '\n',)
            if str(i) == month:
                for part in info:
                    final_cal += (part + '\n',)
    with open('/media/storage/site/data/calendar.txt', 'w') as file:
        for part in final_cal:
            file.write(part)
