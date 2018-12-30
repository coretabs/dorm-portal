import datetime

from django.conf import settings

import i18n


class CrossDomainSessionMiddleware:

    def __init__(self, process_request):
        self.process_request = process_request

    def __call__(self, request):
        response = self.process_request(request)
        if response.cookies:
            try:
                host = request.META['HTTP_ORIGIN']
                # check if it's a different domain
                if host in settings.COOKIE_DOMAINS:
                    for cookie in response.cookies:
                        if cookie == 'csrftoken' or cookie == 'sessionid':
                            response.cookies[cookie]['domain'] = settings.COOKIE_DOMAINS[host]
            except KeyError:
                pass

        return response
