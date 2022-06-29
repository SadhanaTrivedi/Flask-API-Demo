from typing import Any, Dict
from unittest import TestCase

from tests.base import BaseFlaskTest


class ExampleApiTest(BaseFlaskTest):

    def test_sample(self):
        response: Dict[str, Any] = self.client.get('/ping').json
        self.assertEqual('pong', response['message'])
        self.assertEqual('testing_site.com', response['site_name'])

class FetchCompanies(BaseFlaskTest):
    def test_fetch_companies(self):
        data = {"name": "test", "domain": "test.com"}
        response: Dict[str, Any] = self.client.post('/companies', json=data).json
        self.assertEqual('The task is recieved', response['response'])
        self.assertNotEqual(5345, response['response'])
        self.assertNotEqual({"test": 43}, response['response'])

    def _company_details(self, name):
        from worker.tasks import fetch_company_data_from_redis
        result = fetch_company_data_from_redis(name)
        return result

    def _get_company_details(self, company_name):
        response: Dict[str, Any] = self.client.get('/companies/'+company_name).json
        result = self._company_details(company_name)
        if 'error' in response:
            self.assertEqual('Data not found', response['error'])
        else:
            assert "result" in response
            self.assertDictEqual(result['result'], response['result'])
            self.assertEqual(result["result"]["employee_count"], response["result"]["employee_count"])
            self.assertEqual(result["result"]["company_age"], response["result"]["company_age"])

    def test_get_company_details(self):
        self._get_company_details("Uber")
        self._get_company_details("xyz")


class ExampleWorkerTest(TestCase):
    def test_worker(self):
        from worker.tasks import fetch_company_details
        self.assertIsNone(fetch_company_details('some input'))

