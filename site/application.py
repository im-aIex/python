from wsgiref.simple_server import make_server
from werkzeug.serving import run_simple

from pyramid.config import Configurator

from pyramid.session import UnencryptedCookieSessionFactoryConfig

def main():
    config = Configurator(session_factory=UnencryptedCookieSessionFactoryConfig('eyedstuffs'))
    config.scan("views")
    config.add_static_view('static', 'static/', cache_max_age=86400)
    config.add_route('about_list', '/about/*list')
    config.add_route('files_list', '/files/{home}/*list')
    config.add_route('cal_update', '/calupdate/*data')
    app = config.make_wsgi_app()
    return app

if __name__ == '__main__':
    app = main()
    run_simple('192.168.0.8', 80, app, threaded=True)
