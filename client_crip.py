import socket
import threading
from cryptography.fernet import Fernet
import gera_key_crip
from pathlib import Path

# Gerar chave e 
caminho = Path('key.key')
if caminho.exists():
    print("O arquivo já existe.")
else:
    gera_key_crip.gerar_chave()

# Carregar chave 
with open("key.key", "rb") as f:
    key = f.read()

fernet = Fernet(key)

nome = input("Qual seu nome: ")
print('\nDigite "TT" para sair e fechar o chat')

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
                print(texto)
            except:
               
                print(dados.decode())

        except:
            print("Fechando chat...")
            client.close()
            break


def escrever():
    while True:
        msg = input()

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