# wsgi-static-middleware

A simple WSGI middleware that I wrote for my Falcon app, with some help online ofcourse, to serve static files.

To use this middleware in your Falcon app:

```
import falcon

from static_middleware import StaticMiddleware

app = falcon.API()
app = StaticMiddleware(app)
```

By default, all static files are assumed to be stored in the `static` directory in the root of the app. You can optionally set the keyword argument `static_dir` to the directory in which the `static` directory is present.

For example, if the static directory is present inside the `files` directory of the `static` directory:

```
import falcon

from static_middleware import StaticMiddleware

app = falcon.API()
app = StaticMiddleware(app, static_dir='files')
```

Hope this works! Tested with Python3.5. Hopefully it works in other versions of Python too.

## Pull requests are welcome.
