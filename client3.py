import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox

import pyfiglet

HOST = "127.0.0.1"
PORT = 5454


class ChatGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chat A3")
        self.root.geometry("800x550")
        self.root.configure(bg="#1e1e1e")

        # Nome do usuário
        self.nome = simpledialog.askstring("Identificação", "Digite seu nome:")
        if not self.nome:
            self.root.destroy()
            return

        # Área de mensagens (somente leitura)
        self.chat_box = scrolledtext.ScrolledText(
            self.root,
            bg="#2b2b2b",
            fg="white",
            state="disabled",
            wrap=tk.WORD,
            font=("Consolas", 12)
        )
        self.chat_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Campo de digitação
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
        send_button = tk.Button(
            self.root,
            text="Enviar",
            command=self.send_message,
            bg="#4b4b4b",
            fg="white",
            font=("Consolas", 12)
        )
        send_button.pack(pady=5)

        # Socket do cliente
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.client.connect((HOST, PORT))
        except:
            messagebox.showerror("Erro", "Não foi possível conectar ao servidor.")
            self.root.destroy()
            return

        # Envia o nome ao servidor
        self.client.send(self.nome.encode("utf-8"))

        # Mostra no chat local
        ascii_banner = pyfiglet.figlet_format("CHAT CLIENT", font="slant")
        self._add_message(ascii_banner)
        self._add_message("----------- A3 - pr. Alberlan - Unifacs -----------\n")
        self._add_message("Clint conectado ao servidor!")

        # Thread de escuta
        threading.Thread(target=self.receive_messages, daemon=True).start()

        self.root.mainloop()


    def _add_message(self, msg):
        """Adiciona mensagem na área de chat."""
        self.chat_box.config(state="normal")
        self.chat_box.insert(tk.END, msg + "\n")
        self.chat_box.config(state="disabled")
        self.chat_box.yview(tk.END)


    def send_message(self, event=None):
        msg = self.entry.get().strip()
        if not msg:
            return
        
        if msg.upper() == "TT":
            self.client.send("TT".encode('utf-8'))
            self.root.destroy()
            return

        final_msg = f"{self.nome}: {msg}"

        try:
            self.client.send(final_msg.encode("utf-8"))
        except:
            messagebox.showerror("Erro", "Conexão perdida!")
            self.root.destroy()
            return

        # MOSTRA para o próprio usuário também
        self._add_message(final_msg)

        # Limpa o campo
        self.entry.delete(0, tk.END)


    def receive_messages(self):
        while True:
            try:
                msg = self.client.recv(1024).decode("utf-8")
                if not msg:
                    break
                if msg == b"NOME":
                    self.client.send(self.nome.encode())
                    continue
                # Mostra mensagens recebidas
                self._add_message(msg)

            except:
                break

        self.client.close()


if __name__ == "__main__":
    ChatGUI()
