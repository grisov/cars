"""
    Delete the vehicle from the database.
    HTTP method: DELETE
    URI: /vehicles/vehicle/{id}/
    path parameter: id
"""

import requests

id = 5  # the ID of the vehicle in the database
url = f"http://localhost:8000/vehicles/vehicle/{id}/"

# Make request
response = requests.delete(url)

# View HTTP status code
print(response.status_code)

# View the deserialized response from the server
print(response.json())
