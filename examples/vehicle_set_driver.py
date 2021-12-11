"""
    Set driver in to the vehicle or remove driver from the vehicle.
    HTTP method: POST
    URI: /vehicles/set_driver/{id}/
    path parameters: id (vehicle ID in the database)
    request body: driver_id (possible values: positive integer or None)
"""

import requests

# URL example:
id = 7
url = f"http://localhost:8000/vehicles/set_driver/{id}/"
data1 = {"driver_id": 8}  # set driver with ID == 8 in to the vehicle
data2 = {"driver_id": None}  # remove driver from the vehicle

# Make request
response = requests.post(url, json=data1)

# View HTTP status code
print(response.status_code)

# View the deserialized response from the server
print(response.json())
