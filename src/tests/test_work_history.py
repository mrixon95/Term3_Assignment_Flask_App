import os
import unittest
from main import create_app, db


class TestWorkHistory(unittest.TestCase):    


    @classmethod
    def create_user(cls, username, email):

        response = cls.client.post("/user/", json={
            "city": "melbounre",
            "country": "Australia",
            "created_at": "2020-12-26T20:45:09",
            "dob": "1995-08-06T00:00:00",
            "first_name": "Michael",
            "last_name": "Rixon",
            "mobile": "001-380-382-7166x368",
            "username": f"{username}",
            "email": f"{email}",
            "password": "123456"
        })

        if response.status_code != 200:
            raise ValueError("Error when getting test user token.")


    @classmethod
    def auth_user(cls, username):
        """Returns a user token for the test user as well
        as a header dictionary for authorization."""

        response = cls.client.post("/user/login", json={
            "username": f"{username}",
            "password": "123456"
        })

        print(response)

        if response.status_code != 200:
            raise ValueError("Error when getting user token.")

        token = response.json["token"]
        auth_header = {
            "Authorization": f"Bearer {token}"
        }

        return token, auth_header




    
    @classmethod
    def setUp(cls) -> None:
        os.environ["FLASK_ENV"] = "testing"
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

        cls.client = cls.app.test_client()

        cls.create_user("user1", "user1@gmail.com")
        cls.create_user("user2", "user2@gmail.com")
        cls.create_user("user3", "user3@gmail.com")
        cls.create_user("user4", "user4@gmail.com")

        cls.user1_auth_header = cls.auth_user("user1")[1]
        cls.user2_auth_header = cls.auth_user("user2")[1]
        cls.user3_auth_header = cls.auth_user("user3")[1]
        cls.user4_auth_header = cls.auth_user("user4")[1]







    def test_workhistory_post(self):

        user1_work_history = {
            "city": "The city stuff",
            "company": "Company name",
            "country": "Gambia",
            "date_end": "2005-01-03 00:00:00",
            "date_start": "1956-11-10 00:00:00",
            "job_title": "cool job",
            "last_updated": "2020-11-10 00:00:00"
        }

        response = self.client.post("/workhistory/", json=user1_work_history, headers=self.user1_auth_header)

        self.assertEqual(response.status_code, 200,
                         "post work history")


    def test_workhistory_get(self):

        user2_work_history = {
            "city": "The city stuff",
            "company": "Company name",
            "country": "Gambia",
            "date_end": "2005-01-03 00:00:00",
            "date_start": "1956-11-10 00:00:00",
            "job_title": "cool job",
            "last_updated": "2020-11-10 00:00:00"
        }

        response3 = self.client.post("/workhistory/", json=user2_work_history, headers=self.user2_auth_header)

        response4 = self.client.get("/workhistory/user/user2")

        self.assertEqual(response4.status_code, 200,
                         "valid workhistory returns 200")

        response5 = self.client.get("workhistory/user/blahblahblah", json=user2_work_history, headers=self.user2_auth_header)

        self.assertEqual(response5.status_code, 401,
                         "invalid user returns 401")


    def test_workhistory_update(self):

        user3_work_history = {
            "city": "The city stuff",
            "company": "Company name",
            "country": "Gambia",
            "date_end": "2005-01-03 00:00:00",
            "date_start": "1956-11-10 00:00:00",
            "job_title": "cool job",
            "last_updated": "2020-12-26 04:11:15.390409"
        }

        response3 = self.client.post("/workhistory/", json=user3_work_history, headers=self.user3_auth_header)
        id = response3.get_json()["id"]

        print(id)


        user3_work_history_update = {
            "city": "Some new city",
            "company": "A different name"
        }

        response4 = self.client.put(f"/workhistory/{id}", json=user3_work_history_update, headers=self.user3_auth_header)

        self.assertEqual(response4.status_code, 200,
                         "Update work history returns 200")
        
        id += 10
        
        response4 = self.client.put(f"/workhistory/{id}", json=user3_work_history_update, headers=self.user3_auth_header)

        self.assertEqual(response4.status_code, 401,
                         f"Can't update since no workhistory has id of {id}")

        
    def test_workhistory_delete(self):

        user4_work_history = {
            "city": "The city stuff",
            "company": "Company name",
            "country": "Gambia",
            "date_end": "2005-01-03 00:00:00",
            "date_start": "1956-11-10 00:00:00",
            "job_title": "cool job",
            "last_updated": "2020-12-26 04:11:15.390409"
        }

        response1 = self.client.post("/workhistory/", json=user4_work_history, headers=self.user4_auth_header)
        id = response1.get_json()["id"]


        response2 = self.client.delete(f"/workhistory/{id}", headers=self.user4_auth_header)

        self.assertEqual(response2.status_code, 200,
                         "Update work history returns 200")
        
        id += 10
        
        response4 = self.client.delete(f"/workhistory/{id}", headers=self.user4_auth_header)

        self.assertEqual(response4.status_code, 401,
                         f"Can't update since no workhistory has id of {id}")



    

    @classmethod
    def tearDown(cls) -> None:
        db.session.remove()
        db.drop_all()

        cls.app_context.pop()