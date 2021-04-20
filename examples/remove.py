"""
    Delete the entry in the database by the specified ID
    using the HTTP-method DELETE
    ID parameter is passed via URL.
"""

import requests


url = "http://localhost:5000/api/v1/course/{id}".format(
    id=1
)

# Make request
response = requests.delete(url)

# View HTTP status code
print(response.status_code)

# View the deserialized response from the server
print(response.json())
