# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from api.models.course import Course
from api.models.error import Error
from api.test import BaseTestCase


class TestAddController(BaseTestCase):
    """AddController integration test stubs."""

    def test_add_get(self):
        """Test case for add_get.
        Add new course via a URL parameter.
        """
        query_string = [('name', 'Technologies'),
                        ('start', '2021-06-12'),
                        ('end', '2021-09-17'),
                        ('amount', 20)]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/add',
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_add_post(self):
        """Test case for add_post.
        Add new course via a request body.
        """
        course = {
  "amount" : 21,
  "name" : "name",
  "start" : "2000-01-23",
  "end" : "2023-05-27",
  "id" : 6
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/add',
            method='POST',
            headers=headers,
            data=json.dumps(course),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
