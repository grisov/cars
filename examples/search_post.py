"""
    Search for records in the database
    using the HTTP-method POST
    all parameters are passed via request body.
"""

import requests
from json import dumps


url = "http://localhost:5000/api/v1/search"
request_body = {
    "name": "thon",
    "end": "2021-12-15"
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
