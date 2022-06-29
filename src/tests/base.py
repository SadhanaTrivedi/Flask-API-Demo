import unittest
from app import create_app
from simple_settings import settings


class BaseFlaskTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.app = create_app(settings.as_dict())
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        # the client acts as a client browser - it can make requests to our app as if a client is making them
        cls.client = cls.app.test_client(use_cookies=True)

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()
