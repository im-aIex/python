from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.response import FileResponse, Response

from files import get_url, is_file, is_dir, list_dir, delete, rename, upload, make_dir, fix_cal, size, read, write

from data.globalvars import LINKS, USB_LOCATION
from data.header import TITLE, MENU

from layouts import Layouts

import sys
sys.path.append('/media/storage/crypt/')
from encryption import encrypt, public_key_encrypt, generate_random
from decryption import decrypt, private_key_decrypt

sys.path.append('/media/storage/mail/')
from database import select_from

class ProjectorViews(Layouts):
    
    """
    #Default layout
    @view_config(renderer=LINKS['XXX']['template'], name=LINKS['XXX']['link'], route_name=LINKS['XXX']['route_name'], context=LINKS['XXX']['context'])
    def XXX_view(self):
#        if self.check():
#            return HTTPFound(location='/login')
        re = {'page_title': LINKS['XXX']['title']}
        re.update(self.get_header())
        return re
    """

    def __init__(self, request):
        if 'logout' in request.url or not 'username' in request.session:
            request.session['username'] = ''
        self.request = request
        
    #Index / Home
    @view_config(renderer=LINKS['index']['template'], name=LINKS['index']['link'], route_name=LINKS['index']['route_name'], context=LINKS['index']['context'])
    def index_view(self):
        re = {'page_title': LINKS['index']['title']}
        re.update(self.get_header())
        return re
     
    #About
    @view_config(renderer=LINKS['about']['template'], name=LINKS['about']['link'], route_name=LINKS['about']['route_name'], context=LINKS['about']['context'])
    def about_view(self):
        re = {'page_title': LINKS['about']['title']}
        re.update(self.get_header())
        return re

    #About - list
    @view_config(renderer=LINKS['about_list']['template'], name=LINKS['about_list']['link'], route_name=LINKS['about_list']['route_name'], context=LINKS['about_list']['context'])
    def about_list_view(self):
        if self.request.matchdict['list'] == ():
            return HTTPFound(location='/about')
        re = {'page_title': LINKS['about_list']['title'], 'list' : self.request.matchdict['list']}
        re.update(self.get_header())
        return re
     
    #School
    @view_config(renderer=LINKS['school']['template'], name=LINKS['school']['link'], route_name=LINKS['school']['route_name'], context=LINKS['school']['context'])
    def school_view(self):
        if self.check():
            return HTTPFound(location='/login')
        re = {'page_title': LINKS['school']['title']}
        re.update(self.get_header())
        return re

    #Files
    @view_config(renderer=LINKS['files']['template'], name=LINKS['files']['link'], route_name=LINKS['files']['route_name'], context=LINKS['files']['context'])
    def files_view(self):
        if self.check():
            return HTTPFound(location='/login')
        re = {'page_title': LINKS['files']['title']}
        re.update(self.get_header())
        return re

    #Calendar
    @view_config(renderer=LINKS['calendar']['template'], name=LINKS['calendar']['link'], route_name=LINKS['calendar']['route_name'], context=LINKS['calendar']['context'])
    def calendar_view(self):
        with open('/media/storage/site/data/calendar.txt') as f:
            cal_info = f.readlines()
        cal_dict = {}
        current = ''
#        cal_dict['0'] = ''
        current_month = ''
        for part in cal_info:
            part = part.replace('\n', '')
            if part == '':
                continue
#            cal_dict['0'] += part
            if part[0] == '+':
                current = part[1:]
                cal_dict[current] = {}
            elif '//' in part:
                current_month = part[2:]
                cal_dict[current][current_month] = ''
            else:
                cal_dict[current][current_month] += part + ',,,'
        if self.check():
            return HTTPFound(location='/login')
        re = {'page_title': LINKS['calendar']['title'], 'info' : cal_dict}
        re.update(self.get_header())
        return re

    #Calendar Update
    @view_config(renderer=LINKS['cal_update']['template'], name=LINKS['cal_update']['link'], route_name=LINKS['cal_update']['route_name'], context=LINKS['cal_update']['context'])
    def cal_update_view(self):
        if self.check():
            return HTTPFound(location='/login')
        data = self.request.matchdict['data'][0]
        year = data[:data.find(':')]
        month = data[len(year) + 1:]
        month = month[:month.find(':')]
        info = data[len(year) + len(month) + 2:].split(',,,')
        info.pop()
        fix_cal(year, month, info)
        return HTTPFound(location='/calendar/')
        re = {'page_title': LINKS['cal_update']['title']}
        re.update(self.get_header())
        return re

    #Files - list
    @view_config(renderer=LINKS['files_list']['template'], name=LINKS['files_list']['link'], route_name=LINKS['files_list']['route_name'], context=LINKS['files_list']['context'])
    def files_list_view(self):
        if not 'password' in self.request.POST and self.check():
            print self.request.POST
            return HTTPFound(location='/login')
        url = USB_LOCATION + get_url(self.request.matchdict['list'])
        url_parsed = '/'
        for i in range(len(url.split('/')) - 3):
            url_parsed += url.split('/')[i + 1] + '/'
        action = url.split('/')[-2]
        filename = str(url_parsed.split('/')[-2])
        if 'password' in self.request.POST:
            if self.request.POST['password'] != '':
                password = self.request.POST['password']
#                print password
                content = encrypt(self.request.POST['notecontent'], password)
                write('/'.join(url.split('/')[:-2]), content)
                return HTTPFound(location='/files' + url[:-1])
#                return Response()
        elif 'file' in self.request.POST:
            filename = self.request.POST['file'].filename
            print filename
            input_file = self.request.POST['file'].file
            upload(input_file, url, filename)
            print '/files' + url
            return HTTPFound(location='/files' + url)
        elif 'dir_name' in self.request.POST:
            dirname = self.request.POST['dir_name']
            make_dir(dirname, url)
            return HTTPFound(location='/files' + url)
        elif 'note_name' in self.request.POST:
            write(url + self.request.POST['note_name'], '')
            return HTTPFound(location='/files' + url)
        elif 'notecontent' in self.request.POST:
            content = encrypt(self.request.POST['notecontent'], decrypt(self.request.session['enpass'], self.request.cookies['r']))
            write('/'.join(url.split('/')[:-2]), content)
            return HTTPFound(location='/files' + url)
        elif action == 'edit':
            content = decrypt(read(url_parsed[:-1]), decrypt(self.request.session['enpass'], self.request.cookies['r']))
            re = { 'page_title' : 'Notes', 'edit' : True, 'contents' : content, 'url' : url }
            re.update(self.get_header())
            return re
        elif action == 'rename':
            # file_old = str(url_parsed.split('/')[-3])
            file_old = '/'.join(url_parsed.split('/')[:-2])
            if not is_file('/'.join(url_parsed.split('/')[:-2])) and not is_dir('/'.join(url_parsed.split('/')[:-2])):
                print 'not filename'
                return HTTPFound(location='/files')
            rename(file_old, filename)
            return HTTPFound('/files' + '/'.join(url.split('/')[:-4]))
        elif is_file(url_parsed[:-1]):
            if action == 'download':
                re = FileResponse(url_parsed[:-1])

                re.headers['Content-Disposition'] = 'attachment; filename="' + filename + '"'
                re.headers['Content-Type'] = 'application/force-download'
#                re.headers['filename'] = filename
                re.headers['Accept-Ranges'] = 'bytes'
                return re
            elif action == 'delete':
                delete(url_parsed[:-1])
                return HTTPFound(self.request.url[:-7-len(filename.replace(' ', '%20'))])
        elif is_dir(url[:-7]) and action == 'delete':
            delete(url[:-7])
            return HTTPFound(self.request.url[:-7-len(filename)])
        elif not is_dir(url) or len(url.split('/')) < 5:
            return HTTPFound(location='/files')
        temp = [str(part) for part in list_dir(url)]
        temp.sort(lambda x, y: cmp(x.lower(),y.lower()))
        item_list = [ { 'url' : '/files/' + url[1:] + part if is_dir(url + part) else '/files/' + url[1:] + part + '/download', 'url_ren' : '/files/' + url[1:] + part, 'url_del' : '/files/' + url[1:] + part + '/delete', 'name' : part, 'is_file' : is_file(url + part), 'size' : size(url + part) } for part in temp ]
        
        re = {'page_title': LINKS['files_list']['title'], 'list' : item_list, 'up_dir' : '/files/' + url_parsed[1:], 'url' : url, 'edit' : False }
        re.update(self.get_header())
        return re

    #Login layout
    @view_config(renderer=LINKS['login']['template'], name=LINKS['login']['link'], route_name=LINKS['login']['route_name'], context=LINKS['login']['context'])
    def login_view(self):
        message = ''
        if 'form.submitted' in self.request.params:
            username = self.request.params['login'].lower()
            password = self.request.params['password']
            try:
                r = select_from('user_info', 'username', username)
                if r[2] == encrypt(username, password) and username == r[1]:
                    temp = generate_random()
                    self.request.session['username'] = username
                    self.request.session['enpass'] = encrypt(password, temp)
                    res = HTTPFound(location='/school')
                    res.set_cookie('r', temp)
                    return res
                else:
                    message = 'Failed Login'
            except:
                message = 'Failed Login'
            message = 'Failed Login'
        re = {'page_title': LINKS['login']['title'], 'url' : self.request.application_url + '/login', 'message' : message }
        re.update(self.get_header())
        return re

    #404 error 
    @view_config(renderer=LINKS['error404']['template'], name=LINKS['error404']['link'], route_name=LINKS['error404']['route_name'], context=LINKS['error404']['context'])
    def error_404(self):
        re = {'page_title': LINKS['error404']['title']}
        re.update(self.get_header())
        return re
    


    def check(self):
        end = self.request.url[7:]
        if 'username' in self.request.session:
            if self.request.session['username'] == '':
                return True
        elif end[end.find('/'):] != '/login':
            return True
        return False

    def get_header(self):
        return {'header_menu' : MENU, 'header_title' : TITLE, 'logged_in' : self.request.session['username'] != '', 'page_url' : self.request.url}
