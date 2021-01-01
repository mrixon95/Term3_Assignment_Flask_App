import os
import unittest
from main import create_app, db


class TestStudyHistory(unittest.TestCase):    


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

        cls.create_user("user5", "user5@gmail.com")
        cls.create_user("user6", "user6@gmail.com")
        cls.create_user("user7", "user7@gmail.com")
        cls.create_user("user8", "user8@gmail.com")

        cls.user5_auth_header = cls.auth_user("user5")[1]
        cls.user6_auth_header = cls.auth_user("user6")[1]
        cls.user7_auth_header = cls.auth_user("user7")[1]
        cls.user8_auth_header = cls.auth_user("user8")[1]







    def test_studyhistory_post(self):

        user5_study_history = {
            "city": "The city stuff",
            "institution": "University of Melbourne",
            "country": "Gambia",
            "date_end": "2005-01-03 00:00:00",
            "date_start": "1956-11-10 00:00:00",
            "qualification_title": "master",
            "last_updated": "2020-11-10 00:00:00"
        }

        response = self.client.post("/studyhistory/", json=user5_study_history, headers=self.user5_auth_header)

        self.assertEqual(response.status_code, 200,
                         "post study history")


    def test_studyhistory_get(self):

        user6_study_history = {
            "city": "Melbourne",
            "institution": "University of Sydney",
            "country": "Africa",
            "date_end": "2005-01-03 00:00:00",
            "date_start": "1956-11-10 00:00:00",
            "qualification_title": "PhD",
            "last_updated": "2020-11-10 00:00:00"
        }

        response3 = self.client.post("/studyhistory/", json=user6_study_history, headers=self.user6_auth_header)

        response4 = self.client.get("/studyhistory/user/user6")

        self.assertEqual(response4.status_code, 200,
                         "valid studyhistory returns 200")

        response5 = self.client.get("studyhistory/user/blahblahblah", json=user6_study_history, headers=self.user6_auth_header)

        self.assertEqual(response5.status_code, 401,
                         "invalid user returns 401")


    def test_studyhistory_update(self):

        user7_study_history = {
            "city": "The city stuff",
            "company": "Company name",
            "country": "Gambia",
            "date_end": "2005-01-03 00:00:00",
            "date_start": "1956-11-10 00:00:00",
            "job_title": "cool job",
            "last_updated": "2020-12-26 04:11:15.390409"
        }

        response3 = self.client.post("/studyhistory/", json=user7_study_history, headers=self.user7_auth_header)
        id = response3.get_json()["id"]

        print(id)


        user7_study_history_update = {
            "city": "Some new city",
            "company": "A different name"
        }

        response4 = self.client.put(f"/studyhistory/{id}", json=user7_study_history_update, headers=self.user7_auth_header)

        self.assertEqual(response4.status_code, 200,
                         "Update study history returns 200")
        
        id += 10
        
        response4 = self.client.put(f"/studyhistory/{id}", json=user7_study_history_update, headers=self.user7_auth_header)

        self.assertEqual(response4.status_code, 401,
                         f"Can't update since no study history has id of {id}")

        
    def test_studyhistory_delete(self):

        user8_study_history = {
            "city": "The city stuff",
            "company": "Company name",
            "country": "Gambia",
            "date_end": "2005-01-03 00:00:00",
            "date_start": "1956-11-10 00:00:00",
            "job_title": "cool job",
            "last_updated": "2020-12-26 04:11:15.390409"
        }

        response1 = self.client.post("/studyhistory/", json=user8_study_history, headers=self.user8_auth_header)
        id = response1.get_json()["id"]


        response6 = self.client.delete(f"/studyhistory/{id}", headers=self.user8_auth_header)

        self.assertEqual(response6.status_code, 200,
                         "Update study history returns 200")
        
        id += 10
        
        response8 = self.client.delete(f"/studyhistory/{id}", headers=self.user8_auth_header)

        self.assertEqual(response8.status_code, 401,
                         f"Can't update since no study history has id of {id}")



    

    @classmethod
    def tearDown(cls) -> None:
        db.session.remove()
        db.drop_all()

        cls.app_context.pop()