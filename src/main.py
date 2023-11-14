import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from threading import Thread
from dotenv import load_dotenv
from os import getenv
from mail import send_email

load_dotenv()

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

def mostrarFrutas(frutas):
    c = 1
    for fruta in frutas:
        print(f"[{c}] {fruta}")
        c += 1

frutasDesejadas = []
encerrar_thread = False

def verificarFrutas():
    global frutasDesejadas
    global encerrar_thread
    global estoque
    while not encerrar_thread:
        for fruta in frutasDesejadas:
            if fruta in estoque:
                subject = "Fruta desejada está na loja!"
                message = ""
                from_email = getenv("FROM_EMAIL")
                to_email = "wellingtonll.faria@gmail.com"
                password = getenv("FROM_EMAIL_PASSWORD")

                send_email(subject, message, from_email, to_email, password)
        time.sleep(25)

verificar = Thread(target=verificarFrutas)
verificar.start()

while True:
    print("="*50)
    print("[1] Ver frutas na lista de desejos\n[2] Adicionar fruta a lista de desejos\n[3] Remover fruta desejada\n[4] Ver todas as frutas da loja\n[5] Ver frutas no estoque\n[0] Sair")
    opcao = int(input(":"))
    if opcao == 0:
        print("Saindo... aguarde alguns instantes!")
        encerrar_thread = True
        verificar.join()
        break
    elif opcao == 1:
        if len(frutasDesejadas) == 0: print("Nenhuma fruta na lista de desejos ainda!")
        else: mostrarFrutas(frutasDesejadas)
    elif opcao == 2:
        mostrarFrutas(todas_frutas)
        fruta = int(input("Informe qual fruta deseja adicionar a lista de desejos: "))
        if todas_frutas[fruta-1] in frutasDesejadas: print("Fruta já está na lista de desejos")
        else: frutasDesejadas.append(todas_frutas[fruta-1])
    elif opcao == 3:
        mostrarFrutas(frutasDesejadas)
        fruta = int(input("Informe qual fruta deseja remover da lista de desejos: "))
        try:
            frutasDesejadas.pop(fruta-1)
        except:
            print("Ocorreu um erro ao remover a fruta!")
    elif opcao == 4:
        mostrarFrutas(todas_frutas)
    elif opcao == 5:
        mostrarFrutas(estoque)
    else: print("Opcao inválida!")