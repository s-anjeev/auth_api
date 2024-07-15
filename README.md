# auth_api
This API provides user authentication and authorization functionalities with two roles: admin and user. By default, new users are assigned the user role. The API supports user registration, login, accessing and updating account details, logging out, account deletion, and password changes. Admin users have additional privileges to access user-specific endpoints.

### Endpoint: /sign-up
This endpoint allows a new user to create an account by providing an email, username, and password. All input fields must meet specific validation criteria.

### Request Body Example
Method POST
```
{
"email": "user@example.com",
    "username": "example",
    "password": "exacp1eP@ssW0rd"
}
```

### Python Example
```
import requests

url = "https://api.example.com/sign-up" 
payload = {
    "email": "user@example.com",    # Must be a valid email address format.
    "username": "example",          # username must be 5-12 characters long and contain only alphanumeric characters
    "password": "exacp1eP@ssW0rd"   # Must be at least 8 characters long and no more than 36 characters, Must contain at least one lowercase letter, one uppercase letter, one number, and one special character.
}
headers = {
    "Content-Type": "application/json"
}
response = requests.post(url, json=payload, headers=headers)
print(response. Json())
```