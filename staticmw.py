import mimetypes, os

STATIC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))

class StaticMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        """
        WSGI app/middleware to serve files from /static endpoint.
        """

        if not environ['SCRIPT_NAME']:
            environ['SCRIPT_NAME'] = '/' + environ['PATH_INFO'].split('/')[1]

        if environ['SCRIPT_NAME'] != '/static':
            return self.app(environ, start_response)
        else:
            path = os.path.abspath(
                os.path.join(
                    STATIC_PATH, environ['PATH_INFO'].lstrip('/')
                )
            )

            if not path.startswith(STATIC_PATH) or not os.path.exists(path):
                start_response("404 not found", [('Content-type', 'text/plain')])
                return [
                    'File Not Found: %s\n' % environ['PATH_INFO'],
                    'STATIC_PATH: %s\n' % STATIC_PATH,
                    'Joined path: %s' % path
                ]
            else:
                filetype = mimetypes.guess_type(path, strict=True)[0]
                if not filetype:
                    filetype = 'text/plain'
                start_response("200 OK", [('Content-type', filetype)])
                return environ['wsgi.file_wrapper'](open(path, 'rb'), 4096)
