"""
    Create a new driver in the database.
    HTTP method: POST
    URI: /drivers/driver/
    request body: first_name, last_name
"""

import requests

# URL example:
url = "http://localhost:8000/drivers/driver/"
data = {"first_name": "Joseph", "last_name": "Backer"}

# Make request
response = requests.post(url, json=data)

# View HTTP status code
print(response.status_code)

# View the deserialized response from the server
print(response.json())
