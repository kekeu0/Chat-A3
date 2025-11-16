import threading
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 5454))
server.listen()

clients = []
nomes = []

print("Servidor Iniciado\nEsperando conexão com clientes...")


def transmissao(msg, remetente=None):
    for client in clients:
        if client != remetente:
            client.send(msg)


def tratar(client):
    def remover_client():
        index = clients.index(client)
        nome = nomes[index]
        clients.remove(client)
        nomes.remove(nome)
        client.close()
        transmissao(f"{nome} saiu do chat!".encode())

    while True:
        try:
            msg = client.recv(4096)
            if not msg:
                remover_client()
                return

           
            transmissao(msg, remetente=client)

        except:
            remover_client()
            return


def recebe():
    while True:
        client, addr = server.accept()
        print(f'Conectado com {addr}')

        client.send(b'NOME')
        nome = client.recv(4096).decode()
        nomes.append(nome)
        clients.append(client)

        print(f'O nome do client é {nome}')
        transmissao(f'{nome} Entrou no chat'.encode())
        client.send('Conectado ao servidor!'.encode())

        thread = threading.Thread(target=tratar, args=(client,))
        thread.start()


recebe()