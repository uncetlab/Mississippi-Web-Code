"""Django Request login Middleware."""
# import logging
import requests
import jwt

from django.conf import settings
# from django.urls import resolve, Resolver404


class JwtTokenMiddleware(object):
    """Logging Middleware."""

    def __init__(self, get_response=None):
        """constructor."""
        self.get_response = get_response

    def __call__(self, request):
        """call."""
        self.process_request(request)
        response = self.get_response(request)
        self.process_response(request, response)
        return response

    def _get_jwt_token(self, request):
        url = settings.API_URL + 'api/token/'
        r = requests.post(url=url, data={'username': settings.SILENT_LOGIN_USERNAME,
                                         'password': settings.SILENT_LOGIN_PASSWORD})
        if r.status_code == 200 and 'access' in r.json():
            request.session['token'] = r.json()['access']
        print("Info : New Token ", r.json()['access'])
        return request

    def _check_token_status(self, request):
        url = settings.API_URL + 'api/user_types/'
        if 'token' not in request.session:
            self._get_jwt_token(request)
        else:
            headers = {"Authorization": "Bearer %s" % request.session['token']}
            r = requests.get(url, headers=headers)
            if r.status_code != 200:
                self._get_jwt_token(request)
        return True

    def _jwt_decode_status(self, request):
        """
        jwt decode & check status
        :param request:
        :return:
        """

        try:
            if 'token' not in request.session:
                self._get_jwt_token(request)
            else:
                token = request.session['token']
                decode_token = jwt.decode(token, verify=False)
                print("decode_token : ", decode_token)
            print("Info : Token is still valid and active")
        except jwt.ExpiredSignatureError:
            self._get_jwt_token(request)
            print("Info : Token expired. Get new one")
        except jwt.InvalidTokenError:
            self._get_jwt_token(request)
            print("Info : Invalid Token")

    def process_request(self, request):
        """process_request."""
        # self._check_token_status(request)
        self._jwt_decode_status(request)
        return request

    def process_response(self, request, response):
        """process_response."""
        return response
