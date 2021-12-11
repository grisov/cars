"""
    Get the list of drivers from the database,
    filtered by account creation date
    HTTP method: GET
    URI: /drivers/driver/
    query parameters: created_at__gte, created_at__lte
    input date format: %d-%m-%Y
"""

import requests

# URL examples:
url1 = "http://localhost:8000/drivers/driver/?created_at__gte=11-12-2021"  # Drivers that registered after 11-12-2021
url2 = "http://localhost:8000/drivers/driver/?created_at__gte=29-11-2021&created_at__lte=31-12-2021"  # between dates
url3 = "http://localhost:8000/drivers/driver/?created_at__lte=31-12-2021"  # after 31-12-2021

# Make request
response = requests.get(url1)

# View HTTP status code
print(response.status_code)

# View the deserialized response from the server
print(response.json())
