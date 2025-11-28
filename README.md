# Chat A3 Criptografado com Interface Gráfica 🎓

Este repositório contém um projeto desenvolvido como **trabalho acadêmico** para a faculdade, com o objetivo de aplicar conceitos de **redes, segurança da informação** em Python.  

O sistema implementa um **chat cliente-servidor** onde as mensagens são criptografadas antes de serem transmitidas, garantindo uma segurança de ponta a ponta na comunicação.

---

## 🚀 Tecnologias Utilizadas

- **Python 3** → linguagem principal do projeto
- **Socket** → comunicação cliente-servidor via TCP
- **Threading** → suporte a múltiplos clientes simultâneos
- **Cryptography (Fernet)** → criptografia simétrica para proteger mensagens
- **Tkinter** → interface gráfica para o cliente
- **PyInstaller** → geração de executáveis para distribuição
- **PyFiglet** → banners ASCII para identidade visual

---

## 📂 Estrutura do Projeto

- `server_chat_crip.py` → código do servidor
- `client.py` → código do cliente em modo terminal
- `client_crip.py` → código do cliente em modo terminal com criptografia
- `client3.py` → versão do cliente com interface gráfica (Tkinter)
- `client3_crip.py` → versão do cliente com interface gráfica e criptografia (Tkinter)
- `gera_key_crip.py` → utilitário para gerar a chave de criptografia (`key.key`)
- `README.md` → documentação do projeto
- `\dist` → pasta com os arquivos em formato executavel
  
