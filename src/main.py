import time
from threading import Thread
from dotenv import load_dotenv
from os import getenv
from mail import send_email
from wscraping import WebScraping

load_dotenv()

wscraping = WebScraping()

Thread(target=wscraping.todasFrutas).start()
Thread(target=wscraping.buscarFrutas).start()

def mostrarFrutas(frutas):
    c = 1
    for fruta in frutas:
        print(f"[{c}] {fruta}")
        c += 1

frutasDesejadas = []
encerrar_thread = False
userEmail = None

def verificarFrutas():
    global frutasDesejadas
    global encerrar_thread
    global userEmail
    while not encerrar_thread:
        for fruta in frutasDesejadas:
            if userEmail == None: pass
            else:
                if fruta in wscraping.estoque:
                    subject = "Fruta desejada está na loja!"
                    message = ""
                    from_email = getenv("FROM_EMAIL")
                    to_email = userEmail
                    password = getenv("FROM_EMAIL_PASSWORD")

                    send_email(subject, message, from_email, to_email, password)
        time.sleep(25)

verificar = Thread(target=verificarFrutas)
verificar.start()

while True:
    print("="*50)
    print("[1] Ver frutas na lista de desejos\n[2] Adicionar fruta a lista de desejos\n[3] Remover fruta desejada\n[4] Ver todas as frutas da loja\n[5] Ver frutas no estoque\n[6] Configurar email de notificação\n[0] Sair")
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
        mostrarFrutas(wscraping.todas_frutas)
        fruta = int(input("Informe qual fruta deseja adicionar a lista de desejos: "))
        if wscraping.todas_frutas[fruta-1] in frutasDesejadas: print("Fruta já está na lista de desejos")
        else: frutasDesejadas.append(wscraping.todas_frutas[fruta-1])
    elif opcao == 3:
        mostrarFrutas(frutasDesejadas)
        fruta = int(input("Informe qual fruta deseja remover da lista de desejos: "))
        try:
            frutasDesejadas.pop(fruta-1)
        except:
            print("Ocorreu um erro ao remover a fruta!")
    elif opcao == 4:
        mostrarFrutas(wscraping.todas_frutas)
    elif opcao == 5:
        mostrarFrutas(wscraping.estoque)
    elif opcao == 6:
        userEmail = input("Insira seu email: ")
        print("Email configurado!")
    else: print("Opcao inválida!")