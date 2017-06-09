import webbrowser
import traceback
import sys
import time
import json
from urllib import parse
from requests_oauthlib import OAuth2Session
from  myshows.urls import *
from myshows.exceptions import *
import myshows.config as config

def _login(client_id, client_secret):
    '''Opens myshows authorization page'''
    session = OAuth2Session(client_id, redirect_uri=REDIRECT_URL)
    authorization_url, state = session.authorization_url(AUTH_BASE_URL)
    config.setsetting("client_id", client_id)
    config.setsetting("client_secret", client_secret)
    webbrowser.open(authorization_url)

def _extracttoken(browser_response):
    '''Gets authorization token from server and saves to config file'''
    client_id = config.getsetting("client_id")
    client_secret = config.getsetting("client_secret")
    session = OAuth2Session(client_id, redirect_uri=REDIRECT_URL)
    query = parse.urlsplit(browser_response).query
    code = parse.parse_qs(query)['code'][0]
    token = session.fetch_token(TOKEN_URL, code, client_secret=client_secret)
    config.setsetting("token", json.dumps(token))

def gettoken(client_id, client_secret):
    '''Gets authorization token'''
    tokenstring = config.getsetting("token")
    if tokenstring is not None:
        token = json.loads(tokenstring)
        if token["expires_in"] > 3600:
            return token
        else:
            config.removesetting("token")
    _login(client_id, client_secret)
    for i in range(0, 5):
        tokenstring = config.getsetting("token")
        if tokenstring is not None:
            config.removesetting("client_id")
            config.removesetting("client_secret")
            return json.loads(tokenstring)
        time.sleep(i * 5)
    raise MyShowsRetrieveTokenException()
