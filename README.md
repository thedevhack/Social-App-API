### Steps to Run using Docker
1. Git clone using this command (must have git installed in your PC) and it will clone in current directory
```bash
git clone https://github.com/thedevhack/Social-App-API.git .
```

2. Run docker using compose(must have docker installed and Docker Engine RUNNING)
```bash
docker compose up --build
```
3. 💯 Now you can check your apis on [Sign up URL](https://localhost:8000/users/signup/)

> Please Use localhost:8000 for testing

5. You can shutdown the docker fully using this command
```bash
docker compose down
```
### POSTMAN COLLECTION IS PRESENT IN THE REPO ITSELF
For Testing using Postman (Some Instructions)
* For Testing Sign Up and Login API - you do not require any authentication but any other apis require Token Authentication which you get in Response when you login
* For Testing Authenticated APIs include token in headers in this Format (also included in Postman Collection)
```json
{"Authorization": "token {your_login_token}"}
```
