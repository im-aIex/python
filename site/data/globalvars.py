LINKS = {
         'index' : { 'link' : '', 'title' : 'Home', 'template' : 'templates/index.pt', 'route_name' : None, 'context' : None},
         'about' : { 'link' : 'about', 'title' : 'About', 'template' : 'templates/about.pt', 'route_name' : None, 'context' : None },
         'about_list' : { 'link' : '', 'title' : 'About - listing names', 'template' : 'templates/about_list.pt', 'route_name' : 'about_list', 'context' : None },
         'files' : { 'link' : 'files', 'title' : 'Files', 'template' : 'templates/files.pt', 'route_name' : None, 'context' : None },
         'files_list' : { 'link' : '', 'title' : 'Files - listing', 'template' : 'templates/files_list.pt', 'route_name' : 'files_list', 'context' : None },
         'login' : { 'link' : 'login', 'title' : 'Login', 'template' : 'templates/login.pt', 'route_name' : None, 'context' : None},
         'school' : { 'link' : 'school', 'title' : 'School', 'template' : 'templates/school.pt', 'route_name' : None, 'context' : None},
         'calendar' : { 'link' : 'calendar', 'title' : 'Calendar', 'template' : 'templates/calendar.pt', 'route_name' : None, 'context' : None},
         'cal_update' : { 'link' : '', 'title' : 'Calendar Update', 'template' : 'templates/calendar.pt', 'route_name' : 'cal_update', 'context' : None},
         'notes' : {'link' : '', 'title' : 'Notes', 'template' : 'templates/notes.pt', 'route_name' : 'notes', 'context' : None },

         'error404' : { 'link' : '', 'title' : 'Error 404 - Not found', 'template' : 'templates/error404.pt', 'route_name' : None, 'context' : 'pyramid.httpexceptions.HTTPNotFound' }
}

USB_LOCATION = '/media/'
