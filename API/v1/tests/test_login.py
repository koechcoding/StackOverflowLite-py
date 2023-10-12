from v1.models import User
import json
from v1.tests.base_test import BaseTestCase


class TestLogin(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = User()
        self.user.first_name = "Ogutu"
        self.user.last_name = "Brian"
        self.user.email = "codingbrian58@gmail.com"
        self.user.password = "password"

    def sign_up(self):
        return self.client().post(self.full_endpoint('users/signup'), data=self.user.to_json_str(False),
                                  headers=self.headers)

    def user_login(self):
        return self.client().post(self.full_endpoint('users/login'), data=self.user.to_json_str(False),
                                  headers=self.headers)

    def test_user_can_login(self):
        result = self.sign_up()
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result["status"], "success")

        result = self.client().post(self.full_endpoint('users/login'),
                                    headers=self.no_json_headers)
        self.assertEqual(result.status_code, 400)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result["message"], "Request should be in JSON")

        result = self.user_login()
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result["status"], "success")

    def test_user_canno_login_without_email(self):
        result = self.sign_up()
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result["status"], "success")

        self.user.email = ""
        result = self.user_login()
        self.assertEqual(result.status_code, 400)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result["status"], "error")

    def test_user_cannot_login_without_password(self):
        result = self.sign_up()
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result["status"], "success")

        self.user.password = ""
        result = self.user_login()
        self.assertEqual(result.status_code, 400)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result["status"], "error")

    def test_user_cannot_login_with_unknown_email(self):
        result = self.sign_up()
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result["status"], "success")

        self.email = "fakeusername@gmail.com"
        result = self.user_login()
        self.assertEqual(result.status_code, 400)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result["status"], "error")

    def test_user_can_logout(self):
        result = self.sign_up()
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result["status"], "success")

        result = self.user_login()
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result["status"], "success")

        result = self.client().delete(self.full_endpoint('users/logout'), headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(json_result['data']['token'])
        })
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result["status"], "succes")

    def tearDown(self):
        super().tearDown()
