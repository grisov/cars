"""
    Update the existing driver in the database.
    HTTP method: PATCH
    URI: /drivers/driver/{id}/
    path parameters: id
    request body: first_name, last_name
"""

import requests

# URL example:
id = 7
url = f"http://localhost:8000/drivers/driver/{id}/"
data = {"first_name": "Joseph", "last_name": "Backer"}

# Make request
response = requests.patch(url, json=data)

# View HTTP status code
print(response.status_code)

# View the deserialized response from the server
print(response.json())
