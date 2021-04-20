"""
    Add an entry to the database
    using the HTTP-method GET
    all parameters are passed via URL.
"""

import requests


url = "http://localhost:5000/api/v1/add?name={name}&start={start}&end={end}&amount={amount}".format(
    name="Test",
    start="2021-05-01",
    end="2021-07-31",
    amount=12
)

# Make request
response = requests.get(url)

# View HTTP status code
print(response.status_code)

# View the deserialized response from the server
print(response.json())
