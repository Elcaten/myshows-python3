from myshows.urls import *
from myshows.exceptions import *

from urllib.error import HTTPError
from urllib.parse import urljoin, urlencode

VERSION = '0.0.2'
SHOW_STATUS = ['watching', 'cancelled', 'later', 'remove']

class myshowsloginbase(object):
    def __init__(self):
        self._opener = None
        self._login_url = ''
        self._credentials = {}

    def login(self):        
        try:
            url = urljoin(HOST, self._login_url) + '?' + urlencode(self._credentials)
            r = self._opener.open(url)
        except HTTPError as error:
            raise MyShowsAuthentificationFailedException()

    def md5(self, string):
        from hashlib import md5
        return md5(string.encode('utf-8')).hexdigest()

class myshowslogin(myshowsloginbase):
    def __init__(self, login, password, opener):
        super(myshowslogin, self).__init__()
        self._login_url = LOGIN
        self._opener = opener

        if not login:
            raise ValueError('Empty login')
        if not password:
            raise ValueError('Empty password')

        self._credentials['login'] = login
        self._credentials['password'] = self.md5(password)

class session(object):
    def __init__(self):
        from http.cookiejar import CookieJar
        from urllib.request import build_opener, HTTPCookieProcessor
        self._opener = build_opener(HTTPCookieProcessor(CookieJar()))

    def login(self, login, password):
        self._login = myshowslogin(login, password, self._opener)
        self.__login()

    def __login(self):
        if not self._login:
            raise MyShowsAuthentificationRequiredException()
        self._login.login()

    def __call(self, url, credentials=None, json=True):
        if credentials:
            data = urlencode(credentials)
            url = url + '?' + data
        try:
            r = self._opener.open(url)
        except HTTPError as error:
            code = error.getcode()
            if code == 401:
                raise MyShowsAuthentificationRequiredException()
            elif code == 404:
                raise MyShowsInvalidParametersException()
            else:
                raise MyShowsException()
        except:
            raise MyShowsException()

        if json == False:
            return True
            
        from json import loads
        data = r.read().decode('utf-8')
        return loads(data)

    def __join(self, path):
        if not path:
            return None
        return urljoin(HOST, path)

    def profile(self):
        url = self.__join(PROFILE)
        return self.__call(url)

    def profile_shows(self, shows_id=None):
        url = self.__join(PROFILE_SHOWS) + str(shows_id) + '/' if shows_id else self.__join(PROFILE_SHOWS)
        return self.__call(url)

    # status = ['watching', 'cancelled', 'later', 'remove']
    def profile_shows_status(self, shows_id, status):
        if status not in SHOW_STATUS:
            return None
        if not shows_id:
            return None
        url = self.__join(PROFILE_SHOWS) + str(shows_id) + '/' + status
        r = self.__call(url, json=False)
        return True

    def profile_next(self):
        url = self.__join(PROFILE_NEXT)
        return self.__call(url)

    def profile_unwatched(self):
        url = self.__join(PROFILE_UNWATCHED)
        return self.__call(url)

    # without auth methods 
    def shows(self, shows_id):
        url = self.__join(SHOWS) + str(shows_id)
        return self.__call(url)

    def user_profile(self, username):
        if not username:
            return None
        url = self.__join(PROFILE) + username
        return self.__call(url)

    def search(self, q):
        url = self.__join(SEARCH)
        data = {'q':q}
        return self.__call(url, data)

    def genres(self):
        url = self.__join(GENRES)
        return self.__call(url)
