import requests
import time
from threading import Thread, Event
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from os import getenv

load_dotenv()

def send_email(subject, message, from_email, to_email, password):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

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

    while not encerrar_thread:
        for fruta in frutasDesejadas:
            if fruta in eval(requests.get("http://127.0.0.1:8080/inStock").text):
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
        allFruits = eval(requests.get("http://127.0.0.1:8080/allBloxFruits").text)
        mostrarFrutas(allFruits)
        fruta = int(input("Informe qual fruta deseja adicionar a lista de desejos: "))
        if allFruits[fruta-1] in frutasDesejadas: print("Fruta já está na lista de desejos")
        else: frutasDesejadas.append(allFruits[fruta-1])
    elif opcao == 3:
        mostrarFrutas(frutasDesejadas)
        fruta = int(input("Informe qual fruta deseja remover da lista de desejos: "))
        try:
            frutasDesejadas.pop(fruta-1)
        except:
            print("Ocorreu um erro ao remover a fruta!")
    elif opcao == 4:
        allFruits = eval(requests.get("http://127.0.0.1:8080/allBloxFruits").text)
        mostrarFrutas(allFruits)
    elif opcao == 5:
        estoque = eval(requests.get("http://127.0.0.1:8080/inStock").text)
        mostrarFrutas(estoque)
    else: print("Opcao inválida!")