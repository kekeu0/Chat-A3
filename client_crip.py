import socket
import threading
from cryptography.fernet import Fernet
import gera_key_crip
from pathlib import Path

import time
import pyfiglet

# Gerar chave e 
caminho = Path('key.key')
if caminho.exists():
    print("O arquivo já existe")
else:
    gera_key_crip.gerar_chave()

# Carregar chave 
with open("key.key", "rb") as f:
    key = f.read()

fernet = Fernet(key)

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


def recebe():
    while True:
        try:
            dados = client.recv(4096)

            if not dados:
                break

            if dados == b'NOME':
                client.send(nome.encode())
                continue

            # descriptografar
            try:
                texto = fernet.decrypt(dados).decode()
                texto_efeito(texto, delay=0.06)
            except:
                print(dados.decode())

        except:
            texto_efeito("Fechando chat...", delay=0.08)
            client.close()
            break


def escrever():
    while True:
        msg = input("\n")

        if msg.upper() == "TT":
            # TT
            encrypted = fernet.encrypt("TT".encode())
            client.send(encrypted)
            client.close()
            break

        texto = f"{nome}: {msg}".encode()

        #  criptografando
        encrypted = fernet.encrypt(texto)
        client.send(encrypted)


recebe_thread = threading.Thread(target=recebe)
recebe_thread.start()

escrever_thread = threading.Thread(target=escrever)
escrever_thread.start()