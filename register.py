import requests

def register():
    username = input("Username: ")
    password = input("Password: ")
    email = input("Email: ")
    dados = {"username": username, "password": password, "email": email}
    return requests.post("http://127.0.0.1:8080/register", json=dados).text