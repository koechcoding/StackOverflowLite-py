import unittest
from run import create_app
from v1 import clear
from v1.models import User
import json


class BaseTestCase(unittest.TestCase):
    url_prefix = "/api/v1"

    def setUp(self):
        self.app = create_app("TESTING")
        self.client = self.app.test_client
        self.headers = {'Content-Type': 'application/json'}
        self.no_json_headers = {}

    def full_endpoint(self, path=""):
        return self.url_prefix + path

    def tearDown(self):
        clear()


class AutheticatedTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        """create access token for the test cases"""
        self.user = User()
        self.user.first_name = "Ogutu"
        self.user.last_name = "Brian"
        self.user.email = "codingbrian58@gmail.com"
        self.user.password = "password"

        self.client().post(
            self.full_endpoint('users/signup'),
            data=self.user.to_json_str(False),
            headers=self.headers
        )