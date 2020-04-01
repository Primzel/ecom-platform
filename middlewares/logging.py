import re, logging

req_log = logging.getLogger('primzel.requests')


def log_cond(request):
    return re.search(r'^/(login|logout|auth)', request.path)


class HeadersLoggingMiddleware(object):
    def process_response(self, request, response):
        keys = sorted(filter(lambda k: re.match(r'(HTTP_|CONTENT_)', k), request.META))
        keys = ['REMOTE_ADDR'] + keys
        meta = ''.join("%s=%s\n" % (k, request.META[k]) for k in keys)
        print(meta)
        try:
            status_text = response.status_code
        except KeyError:
            status_text = 'UNKNOWN STATUS CODE'
        status = '%s %s' % (response.status_code, status_text)
        response_headers = [(str(k), str(v)) for k, v in response.items()]
        for c in response.cookies.values():
            response_headers.append(('Set-Cookie', str(c.output(header=''))))
        headers = ''.join("%s: %s\n" % c for c in response_headers)
        req_log.debug('"%s %s\n%s\n%s\n%s' % (request.method, request.build_absolute_uri(), meta,
                                             status, headers))

        return response

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        self.process_response(request, response)
        # Code to be executed for each request/response after
        # the view is called.

        return response
