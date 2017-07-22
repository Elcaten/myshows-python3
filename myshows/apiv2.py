class apiv2(object):
    def __init__(self):
        from requests import Session
        self._session = Session()

    def __getattr__(self, method_name):
        return Call(self, method_name)

    def __call__(self, method_name, **method_kwargs):
        return getattr(self, method_name)(**method_kwargs)

    def login(self, client_id, client_secret):
        if not client_id:
            raise ValueError('Empty client id')
        if not client_secret:
            raise ValueError('Empty client secret')

        from requests_oauthlib import OAuth2Session
        from myshows.auth import gettoken
        token = gettoken(client_id, client_secret)
        self._session = OAuth2Session(client_id, token=token)

    def request(self, request):
        jsonrpc = {
            'jsonrpc': '2.0',
            'method': request._method_name,
            'params': request._method_args,
            'id': 1
        }

        from myshows.urls import APIV2
        response = self._session.post(APIV2, json=jsonrpc).json()

        try:
            return response['result']
        except KeyError:
            return response['error']

class Call(object):
    __slots__ = ('_api', '_method_name', '_method_args')

    def __init__(self, api, method_name):
        self._api = api
        self._method_name = method_name

    def __getattr__(self, method_name):
        return Call(self._api, self._method_name + '.' + method_name)

    def __call__(self, **method_args):
        self._method_args = method_args
        return self._api.request(self)
