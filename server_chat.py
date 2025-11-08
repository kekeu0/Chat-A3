import threading
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria socket TCP
server.bind(('127.0.0.1', 5454)) # host, port
server.listen()

clients = []
nomes =  []
print("Servidor Iniciado\nEsperando conexão com clientes...")

def transmissao(msg, remetende=None): # Envia uma mensagem para todos os clientes
    for client in clients:
        if client != remetende:
            client.send(msg)

def tratar(client):   # Mantém a comunicação com um cliente específico
    def remover_client(): # Para sair
         index = clients.index(client)
         nome = nomes[index]
         clients.remove(client)
         nomes.remove(nome)
         client.close()
         transmissao(f'{nome} saiu do chat!'.encode('utf-8'))

    while True:
        try:
            msg = client.recv(1024)
            if msg.decode('utf-8').upper() == "TT":
                remover_client()
                return
            else:
                transmissao(msg, remetende=client)
        except:
            remover_client()
            return

def recebe(): # Fica em loop aceitando novas conexões
    while True:
        client, addrs = server.accept()
        print(f'Conectado com {str(addrs)}')

        client.send('NOME'.encode('utf-8'))
        nome = client.recv(1024).decode('utf-8')
        nomes.append(nome)
        clients.append(client)

        print(f'O nome do client é {nome}!')
        transmissao(f'{nome} Entrou no chat\n'.encode('utf-8'))
        client.send('Conectado ao servidor!'.encode('utf-8'))

        thread = threading.Thread(target=tratar, args=(client,))
        thread.start()

recebe()