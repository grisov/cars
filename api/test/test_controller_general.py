from __future__ import absolute_import
import unittest
from flask import json
from six import BytesIO
from api.models.course import Course
from api.models.error import Error
from api.test import BaseTestCase


class TestGeneralController(BaseTestCase):
    """GeneralController integration test stubs"""

    @unittest.skip("Controller is under development")
    def test_get_details(self):
        """Test case for get_details

        Detailed information about the training course
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/course/{id}'.format(id=1),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @unittest.skip("Controller is under development")
    def test_remove(self):
        """Test case for remove

        Delete a course with the specified ID
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/course/{id}'.format(id=1),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    @unittest.skip("Controller is under development")
    def test_update(self):
        """Test case for update feature.
        Update a course data with the specified ID.
        """
        course = {
  "amount" : 21,
  "name" : "name",
  "start" : "2003-04-27",
  "end" : "2005-01-03",
  "id" : 6
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/course/{id}'.format(id=1),
            method='PUT',
            headers=headers,
            data=json.dumps(course),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
