"""
    Add an entry to the database
    using the HTTP-method POST
    all parameters are passed via request body.
"""

import requests
from json import dumps


url = "http://localhost:5000/api/v1/add"
request_body = {
    "name": "Training course",
    "start": "2021-07-07",
    "end": "2021-08-08",
    "amount": 7
}

# Make request
response = requests.post(
    url,
    data=dumps(request_body),
    headers={"Content-Type": "application/json"}
)

# View HTTP status code
print(response.status_code)

# View the deserialized response from the server
print(response.json())
