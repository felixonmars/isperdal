class ServerAdapter(object):
    def __init__(self, host, port, debug, ssl):
        self.host = host
        self.port = port
        self.debug = debug
        self.ssl = ssl

    def run(self, handler):
        pass


class AioHTTPServerAdapter(ServerAdapter):
    def run(self, handler):
        import asyncio
        from aiohttp.wsgi import WSGIServerHttpProtocol

        loop = asyncio.get_event_loop()

        loop.run_until_complete(
            loop.create_server(
                lambda: WSGIServerHttpProtocol(
                    handler,
                    readpayload=True,
                    debug=self.debug,
                    is_ssl=self.ssl
                ),
                self.host,
                self.port
            )
        )

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            loop.stop()


class PulsarServerAdapter(ServerAdapter):
    def run(self, handler):
        from pulsar.apps import wsgi
        from pulsar.apps.wsgi.middleware import (
            middleware_in_executor, wait_for_body_middleware
        )
#       FIXME pulsar clone error, use copy

        wsgi_handler = wsgi.WsgiHandler([
            wait_for_body_middleware,
            middleware_in_executor(handler)
        ])

        wsgi.WSGIServer(
            callable=wsgi_handler,
            bind="{}:{}".format(self.host, self.port)
        ).start()


#   :( Python2 is bad
class GeventServerAdapter(ServerAdapter):
    def run(self, handler):
        from gevent.pywsgi import WSGIServer

        WSGIServer((self.host, self.port), handler).serve_forever()


class WSGIRefServerAdapter(ServerAdapter):
    def run(self, handler):
        from wsgiref.simple_server import make_server

        httpd = make_server(self.host, self.port, handler)
        httpd.serve_forever()

adapter = {
    'aiohttp': AioHTTPServerAdapter,
    'pulsar': PulsarServerAdapter,
    'gevent': GeventServerAdapter,
    'wsgiref': WSGIRefServerAdapter
}
