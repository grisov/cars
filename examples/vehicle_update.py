"""
    Update the existing vehicle in the database.
    HTTP method: PATCH
    URI: /vehicles/vehicle/{id}/
    path parameters: id
    request body: make, model, plate_number
    plate number example: "AA 1234 OO"
"""

import requests

# URL example:
id = 5
url = f"http://localhost:8000/vehicles/vehicle/{id}/"
data = {"make": "BMW", "model": "Q17", "plate_number": "CZ 9147 JP"}

# Make request
response = requests.patch(url, json=data)

# View HTTP status code
print(response.status_code)

# View the deserialized response from the server
print(response.json())
