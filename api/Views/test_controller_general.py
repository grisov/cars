# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from api.models.course import Course  # noqa: E501
from api.models.error import Error  # noqa: E501
from api.test import BaseTestCase


class TestGeneralController(BaseTestCase):
    """GeneralController integration test stubs"""

    def test_get_details(self):
        """Test case for get_details

        Detailed information about the training course
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/course/{id}'.format(id=-1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_remove(self):
        """Test case for remove

        Delete a course with the specified ID
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/course/{id}'.format(id=-1),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update(self):
        """Test case for update

        Update a course with the specified ID
        """
        course = {
  "amount" : 21,
  "name" : "name",
  "start" : "2000-01-23",
  "end" : "2000-01-23",
  "id" : 6
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/course/{id}'.format(id=-1),
            method='PUT',
            headers=headers,
            data=json.dumps(course),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
