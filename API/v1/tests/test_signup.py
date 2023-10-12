from v1.tests.base_test import BaseTestCase
from v1.models import User
import json


class SignUptest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = User()
        self.user.first_name = "Ogutu"
        self.user.last_name = "Brian"
        self.user.email = "codingbrian58@gmail.com"
        self.user.password = "password"

    def test_user_can_sign_up(self):
        result = self.client().post(self.full_endpoint(
            'users/signup'), headers=self.no_json_headers)
        self.assertEqual(result.status_code, 400)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result, ["message", "Request shold be in JSON"])

        result = self.client().post(self.full_endpoint('users/signup'), data=self.user.to_json_str(False),
                                    headers=self.headers)
        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(result.status_code, 201)
        self.assertEqual(json_result["status"], "success")

    def test_user_cannot_sign_up_with_invalid_details(self):
        self.user.email = ""
        result = self.client().post(self.full_endpoint('users/signup'), data=self.user.to_json_str(False),
                                    headers=self.headers)
        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(result.status_code, 400)
        self.assertEqual(json_result['status'], "error")

    def tearDown(self):
        super().tearDown()
