import os
from configparser import ConfigParser
import appdirs

SECTION = 'SETTINGS'
_configfolder = appdirs.user_data_dir('myshows', 'myshows')
_configfilepath = os.path.join(_configfolder, 'settings.ini')

if not os.path.exists(_configfolder):
    os.makedirs(_configfolder, exist_ok=True)
if not os.path.exists(_configfilepath):
    with open(_configfilepath, 'w') as configfile:
        configfile.write(f'[{SECTION}]')

_parser = ConfigParser()

def getsetting(name):
    _parser.read(_configfilepath)
    return _parser.get(SECTION, name, fallback=None)

def setsetting(name, value):
    _parser.read(_configfilepath)
    _parser.set(SECTION, name, value)
    with open(_configfilepath, 'w') as configfile:
        _parser.write(configfile)

def removesetting(name):
    _parser.read(_configfilepath)
    _parser.remove_option(SECTION, name)
    with open(_configfilepath, 'w') as configfile:
        _parser.write(configfile)
