"""
    Update an entry in the database
    using the HTTP-method POST
    ID parameter is passed via URL
    and data to update is passed via request body.
"""

import requests
from json import dumps


url = "http://localhost:5000/api/v1/course/{id}".format(
    id=1
)
request_body = {
    "name": "Super-duper training course",
    "start": "2021-07-07",
    "end": "2021-08-08",
    "amount": 115
}

# Make request
response = requests.put(
    url,
    data=dumps(request_body),
    headers={"Content-Type": "application/json"}
)

# View HTTP status code
print(response.status_code)

# View the deserialized response from the server
print(response.json())
