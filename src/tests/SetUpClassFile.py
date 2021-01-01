import os
import unittest
from main import create_app, db


class SetUpClass(unittest.TestCase):

    setup = False

    @classmethod
    def setUp(cls):

        if not cls.setup:
            os.environ["FLASK_ENV"] = "testing"
            cls.app = create_app()
            cls.app_context = cls.app.app_context()
            cls.app_context.push()
            db.drop_all()
            db.create_all()

            cls.client = cls.app.test_client()
            cls.setup = True
        return cls