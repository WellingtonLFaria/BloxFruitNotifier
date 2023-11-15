import time
from threading import Thread
from dotenv import load_dotenv
from os import getenv
from mail import send_email
from wscraping import WebScraping

load_dotenv()

wscraping = WebScraping()

wscraping.setUp()

def mostrarFrutas(frutas):
    c = 1
    for fruta in frutas:
        print(f"[{c}] {fruta}")
        c += 1

frutasDesejadas = []
encerrar_thread = False
userEmail = None

def verificarFrutas():
    """
    This function checks if the desired fruits are available in the store and sends an email notification to the user if any of the fruits are found.

    Parameters:
    None

    Return:
    None
    """
    global frutasDesejadas
    global encerrar_thread
    global userEmail
    while not encerrar_thread:
        for fruta in frutasDesejadas:
            if userEmail == None: pass
            else:
                if fruta in wscraping.estoque:
                    subject = "Wishlist fruit is in store!"
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
    print("[1] See fruits on wish list\n[2] Add fruit to wish list\n[3] Remove fruit from wishlistt\n[4] See all fruits in the store\n[5] View fruits in stock\n[6] Configure notification email\n[0] Exit")
    opcao = int(input(":"))
    if opcao == 0:
        print("Leaving... wait a few moments!")
        encerrar_thread = True
        verificar.join()
        wscraping.endThreads()
        break
    elif opcao == 1:
        if len(frutasDesejadas) == 0: print("No fruit on the wish list yet!")
        else: mostrarFrutas(frutasDesejadas)
    elif opcao == 2:
        mostrarFrutas(wscraping.todas_frutas)
        fruta = int(input("Enter which fruit you want to add to the wish list:"))
        if wscraping.todas_frutas[fruta-1] in frutasDesejadas: print("Fruit is already on the wish list")
        else: frutasDesejadas.append(wscraping.todas_frutas[fruta-1])
    elif opcao == 3:
        mostrarFrutas(frutasDesejadas)
        fruta = int(input("Enter which fruit you want to remove from your wish list:"))
        try:
            frutasDesejadas.pop(fruta-1)
        except:
            print("An error occurred while removing the fruit!")
    elif opcao == 4:
        mostrarFrutas(wscraping.todas_frutas)
    elif opcao == 5:
        mostrarFrutas(wscraping.estoque)
    elif opcao == 6:
        userEmail = input("Enter your email:")
        print("Email configured!")
    else: print("Invalid option!")