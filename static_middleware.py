import mimetypes, os

static_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))

class StaticMiddleware(object):
    def __init__(self, app, static_dir='', url_prefix='/static'):
        self.app = app
        self.static_dir = static_dir.strip('/')
        self.url_prefix = url_prefix

    def __call__(self, environ, start_response):
        """
        WSGI middleware to serve files from /static endpoint.
        """

        # Setting the SCRIPT_NAME
        if not environ['SCRIPT_NAME']:
            environ['SCRIPT_NAME'] = '/' + environ['PATH_INFO'].split('/')[1]

        if environ['SCRIPT_NAME'] != self.url_prefix:
            return self.app(environ, start_response)
        else:
            # Geterating the full path of the static resource
            path = os.path.abspath(
                os.path.join(
                    static_path,
                    self.static_dir,
                    environ['PATH_INFO'].lstrip('/')
                )
            )

            if not path.startswith(static_path) or not os.path.exists(path):
                return self.app(environ, start_response)
            else:
                filetype = mimetypes.guess_type(path, strict=True)[0]
                if not filetype:
                    filetype = 'text/plain'
                start_response("200 OK", [('Content-type', filetype)])
                return environ['wsgi.file_wrapper'](open(path, 'rb'), 4096)
