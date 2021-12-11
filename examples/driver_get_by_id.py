"""
    Get driver details by ID in the database.
    HTTP method: GET
    URI: /drivers/driver/{id}/
    path parameter: id
"""

import requests

id = 7  # the ID of the driver in the database
url = f"http://localhost:8000/drivers/driver/{id}/"

# Make request
response = requests.get(url)

# View HTTP status code
print(response.status_code)

# View the deserialized response from the server
print(response.json())
