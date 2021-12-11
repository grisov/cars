"""
    Get the list of vehicles from the database.
    HTTP method: GET
    URI: /vehicles/vehicle/
"""

import requests

url = "http://localhost:8000/vehicles/vehicle/"

# Make request
response = requests.get(url)

# View HTTP status code
print(response.status_code)

# View the deserialized response from the server
print(response.json())
