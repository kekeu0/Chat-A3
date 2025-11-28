import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
from cryptography.fernet import Fernet
from pathlib import Path
import gera_key_crip

import pyfiglet


HOST = "127.0.0.1"
PORT = 5454


class ChatCriptoGUI:
    def __init__(self):

        # ----- Carrega a chave ou cria -----
        caminho = Path("key.key")
        if not caminho.exists():
            gera_key_crip.gerar_chave()

        try:
            with open("key.key", "rb") as f:
                key = f.read()
            self.fernet = Fernet(key)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar key.key:\n{e}")
            return

        # ----- Interface -----
        self.root = tk.Tk()
        self.root.title("Chat Criptografado")
        self.root.geometry("800x550")
        self.root.configure(bg="#1e1e1e")

        # Nome
        self.nome = simpledialog.askstring("Nome", "Digite seu nome:")
        if not self.nome:
            self.root.destroy()
            return

        # Área de mensagens
        self.chat_box = scrolledtext.ScrolledText(
            self.root,
            state="disabled",
            bg="#2b2b2b",
            fg="white",
            font=("Consolas", 12),
            wrap=tk.WORD
        )
        self.chat_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Campo para digitar
        self.entry = tk.Entry(
            self.root,
            bg="#333333",
            fg="white",
            font=("Consolas", 12),
            insertbackground="white"
        )
        self.entry.pack(fill=tk.X, padx=10, pady=5)
        self.entry.bind("<Return>", self.send_message)

        # Botão enviar
        enviar_btn = tk.Button(
            self.root,
            text="Enviar",
            command=self.send_message,
            bg="#4b4b4b",
            fg="white",
            font=("Consolas", 12)
        )
        enviar_btn.pack(pady=5)

        # ----- Conectar ao servidor -----
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.client.connect((HOST, PORT))
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível conectar ao servidor:\n{e}")
            self.root.destroy()
            return

        # Exibe mensagem local
        ascii_banner = pyfiglet.figlet_format("CHAT CLIENT", font="slant")
        self._add_message(ascii_banner)
        self._add_message("----------- A3 - pr. Alberlan - Unifacs -----------\n")
        self._add_message("Clint conectado ao servidor! (criptografado)!")

        # Thread de recepção
        threading.Thread(target=self.receive_messages, daemon=True).start()

        self.root.mainloop()

    # ---------- Função para exibir mensagens localmente ----------
    def _add_message(self, msg):
        self.chat_box.config(state="normal")
        self.chat_box.insert(tk.END, msg + "\n")
        self.chat_box.config(state="disabled")
        self.chat_box.yview(tk.END)

    # ---------- Envio de mensagens ----------
    def send_message(self, event=None):
        msg = self.entry.get().strip()
        if not msg:
            return

        # Comando de saída
        if msg.upper() == "TT":
            encrypted = self.fernet.encrypt("TT".encode())
            self.client.send(encrypted)
            self.root.destroy()
            return

        final = f"{self.nome}: {msg}"

        # Exibe para o próprio usuário
        self._add_message(final)

        # Criptografa e envia
        try:
            encrypted = self.fernet.encrypt(final.encode())
            self.client.send(encrypted)
        except:
            messagebox.showerror("Erro", "Conexão perdida!")
            self.root.destroy()

        self.entry.delete(0, tk.END)

    # ---------- Recepção de mensagens ----------
    def receive_messages(self):
        while True:
            try:
                dados = self.client.recv(4096)
                if not dados:
                    break

                # Pedido de nome do servidor
                if dados == b"NOME":
                    self.client.send(self.nome.encode())
                    continue

                # Tenta descriptografar
                try:
                    texto = self.fernet.decrypt(dados).decode()
                except:
                    try:
                        texto = dados.decode()
                    except:
                        continue

                self._add_message(texto)

            except:
                break

        try:
            self.client.close()
        except:
            pass


if __name__ == "__main__":
    ChatCriptoGUI()
