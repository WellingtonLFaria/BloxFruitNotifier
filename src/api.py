from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from threading import Thread
import time
from db import DB

db = DB("localhost", "root", "fatec", "notifierusers")
db.setUp()

todas_frutas = []
estoque = []

def todasFrutas():
    global todas_frutas

    frutas = []
    driver = webdriver.Chrome()
    driver.get("https://blox-fruits.fandom.com/wiki/Blox_Fruits_%22Stock%22")
    linhas = driver.find_element(By.CLASS_NAME, "article-table").find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
    for linha in linhas:
        colunas = linha.find_elements(By.TAG_NAME, "td")
        nomeFruta = colunas[1].find_element(By.TAG_NAME, "a").get_attribute("title")
        frutas.append(nomeFruta)
    todas_frutas = frutas
    driver.quit()

    hora = 0
    min = 0
    while True:
        tempo = time.localtime()
        if tempo.tm_min == min and tempo.tm_hour == hora:
            frutas = []
            driver = webdriver.Chrome()
            driver.get("https://blox-fruits.fandom.com/wiki/Blox_Fruits_%22Stock%22")
            linhas = driver.find_element(By.CLASS_NAME, "article-table").find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
            for linha in linhas:
                colunas = linha.find_elements(By.TAG_NAME, "td")
                nomeFruta = colunas[1].find_element(By.TAG_NAME, "a").get_attribute("title")
                frutas.append(nomeFruta)
            todas_frutas = frutas
            driver.quit()
        time.sleep(25)


def buscarFrutas():
    global estoque

    driver = webdriver.Chrome()
    driver.get("https://blox-fruits.fandom.com/wiki/Blox_Fruits_%22Stock%22")
    figures = driver.find_elements(By.CLASS_NAME, "thumb")
    frutas = []
    for e in figures:
        if e.find_element(By.TAG_NAME, "a").get_attribute("href")[36:] in frutas: break
        else: frutas.append(e.find_element(By.TAG_NAME, "a").get_attribute("href")[36:])
    driver.quit()
    estoque = frutas

    horas = [[1, 10], [5, 10], [9, 10], [13, 10], [17, 10], [21, 10]]
    while True:
        tempo = time.localtime()
        if [tempo.tm_hour, tempo.tm_min] in horas:
            driver = webdriver.Chrome()
            driver.get("https://blox-fruits.fandom.com/wiki/Blox_Fruits_%22Stock%22")
            figures = driver.find_elements(By.CLASS_NAME, "thumb")
            frutas = []
            for e in figures:
                if e.find_element(By.TAG_NAME, "a").get_attribute("href")[36:] in frutas: break
                else: frutas.append(e.find_element(By.TAG_NAME, "a").get_attribute("href")[36:])
            driver.quit()
            estoque = frutas
        time.sleep(25)

Thread(target=todasFrutas).start()
Thread(target=buscarFrutas).start()

app = Flask(__name__)

@app.route("/allBloxFruits", methods=["GET"])
def allBloxFruits():
    return todas_frutas

@app.route("/inStock", methods=["GET"])
def inStock():
    return estoque

@app.route("/register", methods=["POST"])
def register():
    if request.method == "POST":
        dados = request.json
        return db.addUser(dados["username"], dados["password"], dados["email"])

@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        dados = request.json
        users = [(user[0], user[1]) for user in db.users()]
        usernames = [user[0] for user in users]
        if dados["username"] in usernames:
            if (dados["username"], dados["password"]) in users: return "Login realizado com sucesso"
            else: return "Senha incorreta"
        else: return "Nome de usuário ainda não cadastrado"

app.run(host="127.0.0.1", port=8080)