# auth_api
This API provides user authentication and authorization functionalities with two roles: admin and user. By default, new users are assigned the user role. The API supports user registration, login, accessing and updating account details, logging out, account deletion, and password changes. Admin users have additional privileges to access user-specific endpoints.

### 1. Endpoint: /sign-up
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
print(response.Json())
```


### 2. Endpoint: /login
This endpoint allows an existing user to log in by providing their email and password. The input must be in JSON format and must pass validation checks. After successfull login in return user gets a token.

### Request Body Example
Method POST
```
{
    "email": "example@gmail.com",
    "password": "Exa@mp1e"
}
```

### Python Example
```
import requests

url = "https://api.example.com/login"
payload = {
    "email": "example@gmail.com",
    "password": "Exa@mp1e"
}
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```


### 3. Endpoint: /user/profile/edit
This endpoint allows an authenticated, authorized user to edit/update users personal details.Access to resources are allowed based on ```Authorization``` header with ```Bearer``` token. The input must be in JSON format and must pass validation checks.

### Request Body Example
Method PATCH
```
{
    "first_name":"demo value",
    "last_name":"demo value",
    "country":"demo value",
    "phone_number":"demo value",
    "date_of_birth":"demo value",
    "gender":"demo value"
}
```

### Python Example
```
import requests

url = "https://api.example.com/user/profile/edit"
payload = {
    "first_name":"demo value",      # only alphanumeric characters are allowed.
    "last_name":"demo value",       # only alphanumeric characters are allowed.
    "country":"demo value",         # only country codes are allowed e.g IND, USD, etc.
    "phone_number":"demo value",    # only numbers are allowed.
    "date_of_birth":"demo value",   # allowed date format "%Y-%m-%d"
    "gender":"demo value"           # Male, Female, others.
}
headers = {
    "Authorization":"Bearer token_here"
    "Content-Type": "application/json"
}

response = requests.patch(url, json=payload, headers=headers)
print(response.json())
```

### 4. Endpoint: /user/profile/edit/avatar
This endpoint allows an authenticated, authorized user to update users avatar. Access to this endpoint allowed based on ```Authorization``` header with ```Bearer``` token. The input must be a image file and must pass validation checks.

### Request Body Example
Method PATCH
```
Upload your avatar image.
```

### Python Example
```
import requests

url = "https://api.example.com/user/profile/edit/avatar"

# Assuming the image file path is 'avatar.jpg'
files = {
    "avatar": ("avatar.jpg", open("avatar.jpg", "rb"), "image/jpeg")
}

headers = {
    "Authorization":"Bearer token_here"
}

response = requests.patch(url, files=files, headers=headers)
print(response.json())
```


### 5. Endpoint: /logout
Logout endpoint ```/logout``` allows an authenticated user to log out. Access to this endpoint allowed based on ```Authorization``` header with ```Bearer``` token. Authorization_token is blacklisted after successful logout.

### Request Body Example
Method GET
```
{
    "token": "demo value",  # user authorization token
    "id": "demo value"      # user id
}
```

### Python Example
```
import requests

url = "https://api.example.com/logout"
payload = {
    "token": "demo value",  # user authorization token
    "id": "demo value"      # user id
}
headers = {
    "Authorization": "Bearer token_here",
    "Content-Type": "application/json"
}

response = requests.get(url, json=payload, headers=headers)
print(response.json())
```


### .6 Endpoint: /user/dashboard
Using endpoint ```/user/dashboard``` an authorized user can view account related data. Access to this endpoint allowed based on ```Authorization``` header with ```Bearer``` token. 

### Request Body Example
Method GET
```
None
```

### Python Example
```
import requests

url = "https://api.example.com/user/dashboard"
headers = {
    "Authorization": "Bearer token_here",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
print(response.json())
```


### .7 Endpoint: /user/delete-account
This endpoit allow an authorized user to permanently delete there account. Access to this endpoint allowed based on ```Authorization``` header with ```Bearer``` token. 

### Request Body Example
Method GET
```
{
    "username":"demo value"  # unique username of user
    "user_id":"demo value"   # unique user_id of user
    "role":"demo value"      # role of user. (i.e user, by default)
}
```

### Python Example
```
import requests

url = "https://api.example.com/logout"
payload = {
    "username":"demo value"  # unique username of user
    "user_id":"demo value"   # unique user_id of user
    "role":"demo value"      # role of user. (i.e user, by default)
}
headers = {
    "Authorization": "Bearer token_here",
    "Content-Type": "application/json"
}

response = requests.get(url, json=payload, headers=headers)
print(response.json())
```

