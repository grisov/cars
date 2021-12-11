"""
    Get the list of vehicles from the database,
    filtered by the presence of the driver.
    HTTP method: GET
    URI: /vehicles/vehicle/
    query parameters: with_drivers
    possible values: yes/no
"""

import requests

# URL examples:
url1 = "http://localhost:8000/vehicles/vehicle/?with_drivers=yes"  # only vehicles with drivers
url2 = "http://localhost:8000/vehicles/vehicle/?with_drivers=no"  # only vehicles without drivers

# Make request
response = requests.get(url1)

# View HTTP status code
print(response.status_code)

# View the deserialized response from the server
print(response.json())
