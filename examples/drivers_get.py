"""
    Get the list of drivers from the database.
    HTTP method: GET
    URI: /drivers/driver/
"""

import requests

url = "http://localhost:8000/drivers/driver/"

# Make request
response = requests.get(url)

# View HTTP status code
print(response.status_code)

# View the deserialized response from the server
print(response.json())
