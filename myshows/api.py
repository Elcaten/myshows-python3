from myshows.urls import *
from myshows.exceptions import *

from urllib.parse import urljoin
from urllib.error import HTTPError

VERSION = '0.0.1'

class session(object):
	def login(self, login, password):
		self._login = myshowslogin(login, password)
		self.__login()

	def __login(self):
		if not self.login:
			raise MyShowsAuthentificationFailedException()
		self._login.login()
		self._opener = _login.opener()

	def __call(self, url):
		try:
			r = self._opener.open(url)
		except HTTPError as error:
			code = error.getcode()
			if code == 401:
				raise MyShowsAuthentificationRequiredException()
			else:
				raise MyShowsException()
		except:
			raise MyShowsException()

		from json import loads
		data = r.read().decode('utf-8')
		return loads(data)

	def profile(self):
		url = urljoin(HOST, PROFILE)
		return self.__call(url)

	def profile_shows(self, episode_id=None):
		url = urljoin(HOST, PROFILE_SHOWS) + str(episode_id) + '/' if episode_id else urljoin(HOST, PROFILE_SHOWS)
		return self.__call(url)

	def profile_next(self):
		url = urljoin(HOST, PROFILE_NEXT)
		return self.__call(url)

	def profile_unwatched(self):
		url = urljoin(HOST, PROFILE_UNWATCHED)
		return self.__call(url)

	def shows(self, episode_id):
		url = urljoin(HOST, SHOWS) + str(episode_id)
		return self.__call(url)

class myshowsloginbase(object):
	def __init__(self):
		from http.cookiejar import CookieJar
		from urllib.request import build_opener, HTTPCookieProcessor

		self._login_url = ''
		self._credentials = {}
		self._opener = build_opener(HTTPCookieProcessor(CookieJar()))

	def opener(self):
		return self._opener

	def login(self):
		from urllib.error import HTTPError
		from urllib.parse import urljoin, urlencode
		
		try:
			url = urljoin(HOST, self._login_url) + '?' + urlencode(self._credentials)
			r = self._opener.open(url)
		except HTTPError as error:
			raise MyShowsAuthentificationFailedException()

	def md5(self, string):
		from hashlib import md5
		return md5(string.encode('utf-8')).hexdigest()

class myshowslogin(myshowsloginbase):
	def __init__(self, login, password):
		super(myshowslogin, self).__init__()
		self._login_url = LOGIN

		if not login:
			raise ValueError('Empty login')
		if not password:
			raise ValueError('Empty password')

		self._credentials['login'] = login
		self._credentials['password'] = self.md5(password)