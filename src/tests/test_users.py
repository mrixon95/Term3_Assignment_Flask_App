import os
import unittest
from main import create_app, db


class TestUsers(unittest.TestCase):    
    
    @classmethod
    def setUp(cls) -> None:
        os.environ["FLASK_ENV"] = "testing"
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

        cls.client = cls.app.test_client()

        cls.reg_response = cls.client.post(
            "/user/", json= {
            "city": "melbounre",
            "country": "Australia",
            "created_at": "2020-12-26 20:45:09",
            "dob": "1995-08-06 00:00:00",
            "email": "user1@hotmail.com",
            "first_name": "Michael",
            "last_name": "Rixon",
            "mobile": "001-380-382-7166x368",
            "username": "user1",
            "password": "secret1"
            }
        )
        print("initialise users")
        print(cls.reg_response.status_code)
        print(cls.reg_response.get_json())

        cls.client.post(
            "/user/", json= {
            "city": "melbourne",
            "country": "Australia",
            "created_at": "2020-12-26 20:45:09",
            "dob": "1995-08-06 00:00:00",
            "email": "user2@hotmail.com",
            "first_name": "Michael",
            "last_name": "Rixon",
            "mobile": "001-380-382-7166x368",
            "username": "user2",
            "password": "secret2"
            }
        )

    def test_user_register(self):
        self.assertEqual(self.reg_response.status_code, 200,
                         "valid register returns 200")

        status_code = self.reg_response.status_code
        self.assertEqual(status_code, 200)

        json_received = self.reg_response.get_json()

        self.assertEqual(json_received["username"], "user1",
                         "should receive json with username user1")

        

    def test_user_login(self): 
        response = self.client.post("/user/login", json={
            "username": "unknown@test.com",
            "password": "unknown"
        })

        self.assertEqual(response.status_code, 401,
                         "unauthorized")



        response2 = self.client.post("/user/login", json={
            "username": "user1",
            "password": "secret1"
        })

        self.assertEqual(response2.status_code, 200,
                         "successfully logged in")
        
        data2 = response2.get_json()
        print("Login response json is ")
        print(data2)
        self.assertIn("token", data2)
        self.assertIsInstance(data2["token"], str)

    @classmethod
    def tearDown(cls) -> None:
        db.session.remove()
        db.drop_all()

        cls.app_context.pop()