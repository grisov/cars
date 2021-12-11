"""
    Create a new vehicle in the database.
    HTTP method: POST
    URI: /vehicles/vehicle/
    request body: make, model, plate_number
    plate number example: "AA 1234 OO"
"""

import requests

# URL example:
url = "http://localhost:8000/vehicles/vehicle/"
data = {"make": "Audi", "model": "A10", "plate_number": "QL 7415 DZ"}

# Make request
response = requests.post(url, json=data)

# View HTTP status code
print(response.status_code)

# View the deserialized response from the server
print(response.json())
