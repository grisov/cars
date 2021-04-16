from __future__ import absolute_import
import unittest
from flask import json
from six import BytesIO
from api.models.course import Course
from api.models.error import Error
from api.models.search_data import SearchData
from api.test import BaseTestCase


class TestSearchController(BaseTestCase):
    """SearchController integration test stubs"""

    def test_search_get(self):
        """Test case for search_get

        Searching of courses on the properties specified in URL
        """
        query_string = [('name', 'Technologies'),
                        ('start', '2021-06-12'),
                        ('end', '2021-09-17')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/search',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_search_post(self):
        """Test case for search_post

        Searching of courses on the properties specified in request body
        """
        search_data = {
  "name" : "name",
  "start" : "2000-01-23",
  "end" : "2000-01-23"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/search',
            method='POST',
            headers=headers,
            data=json.dumps(search_data),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
