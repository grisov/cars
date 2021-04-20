"""
    Search for records in the database
    using the HTTP-method GET
    all parameters are passed via URL.
"""

import requests


url = "http://localhost:5000/api/v1/search?name={name}&start={start}".format(
    name="thon",
    start="2021-06-12"
)

# Make request
response = requests.get(url)

# View HTTP status code
print(response.status_code)

# View the deserialized response from the server
print(response.json())
