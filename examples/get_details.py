"""
    Get data from the database by ID
    using the HTTP-method GET
    all parameters are passed via URL.
"""

import requests


url = "http://localhost:5000/api/v1/course/{id}".format(
    id=1
)

# Make request
response = requests.get(url)

# View HTTP status code
print(response.status_code)

# View the deserialized response from the server
print(response.json())
