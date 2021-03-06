import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import myshows
from test_config import token
from myshows.exceptions import *
from unittest import TestCase, main

class MyShowsV2APITestCase(TestCase):
    def setUp(self):
        self.api = myshows.apiv2_beta()
        self.token = token

    # test connect
    def test_connect(self):
        response = self.api.shows.GetById(showId=1)
        self.assertEqual(response['title'], 'Доктор Хаус')

    # test with auth NOT WORK
    def test_with_auth(self):
        response = self.api.auth()
        print(response)
        response = self.api.manage.SetShowStatus(id=37473, status='later')
        self.assertEqual(401, response['code'])
        
if __name__ == '__main__':
    main(warnings='ignore')
