from .result import Ok, Err

status_code = {
    200: '200 OK',
    302: '302 Found'
}

class Request(object):
    def __init__(self, env):
        self.env = env
        self.method = env['REQUEST_METHOD'].upper()
        self.path = env['PATH_INFO'].lower()
        self.uri = env['RAW_URI']
        self.body = env['wsgi.input']
        self.next = (
            lambda path: ["{}/".format(x) for x in path[:-1]]+path[-1:]
        )(self.path.split('/'))

#       TODO 解析 env
        self.headers = {}
        self.rest = {}

class Response(object):
    def __init__(self, start_res):
        self.start_res = start_res
        self.headers = {}
        self.body = ""
        self.status = 200

    def set_status(self, code):
        self.status = code
        return self

    def set_header(self, name, value):
        self.headers.update({name: value})
        return self

    def format(self):
#       TODO 格式化 headers
        return [('Content-Type', 'text/html')]

    def push(self, body):
        self.body += body
        return self

    def ok(self, T=None):
        self.start_res(
            status_code[self.status],
            self.format()
        )
        return Ok(
            (lambda body: body.encode() if isinstance(body, str) else body )(T or self.body)
        )

    def err(self, E):
        return Err(E)

    def redirect(self, url, *, code=302):
        self.set_status(code)
        return Err(url)
