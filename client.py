import socket
import threading

nome = input("Qual seu nome: ")
print(f'\nDigite "TT" para sair e fechar o chat')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5454))

def recebe(): # Fica escutando mensagens do servidor
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            if msg == 'NOME':
                client.send(nome.encode('utf-8'))
            else:
                print(f'{msg}')
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
