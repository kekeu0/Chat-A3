from cryptography.fernet import Fernet

def gerar_chave():
    key = Fernet.generate_key()
    with open("key.key", "wb") as f:
        f.write(key)

    print("Chave gerada e salva em key.key")