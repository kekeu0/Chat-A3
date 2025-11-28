import socket
import threading

import time
import pyfiglet

def texto_efeito(text, delay=0.1):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()
    
ascii_banner = pyfiglet.figlet_format("CHAT CLIENT", font="slant")
print(ascii_banner)
print("----------- A3 - pr. Alberlan - Unifacs -----------\n")

texto_efeito("Qual seu nome: ", delay=0.08)
nome = input()
texto_efeito('\nDigite "TT" para sair e fechar o chat', delay=0.04)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5454))

def recebe(): # Fica escutando mensagens do servidor
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            if msg == 'NOME':
                client.send(nome.encode('utf-8'))
            else:
                texto_efeito(msg, delay=0.06)
        except:
            print("Fechando chat...")
            client.close()
            break

def escrever():  # Fica esperando o usuário digitar mensagens
    while True:
        msg = input("\n")
        if msg.upper() == "TT":
            client.send("TT".encode('utf-8'))
            client.close()
            break
        else:
            client.send(f"{nome}: {msg}".encode('utf-8'))

recebe_thread = threading.Thread(target=recebe)
recebe_thread.start()

escrever_thread = threading.Thread(target=escrever)
escrever_thread.start()
