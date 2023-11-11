import requests

def login():
    username = input("Username: ")
    password = input("Password: ")
    dados = {"username": username, "password": password}
    return requests.post("http://127.0.0.1:8080/login", json=dados).text
