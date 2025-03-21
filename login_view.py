import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.configure(bg="#003366")
        self.root.minsize(500, 500)

        # Configurações iniciais
        self.setup_ui()

    def setup_ui(self):
        # Data e hora
        self.label_data_hora = tk.Label(self.root, font=("Arial", 14), bg="#003366", fg="white")
        self.label_data_hora.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        self.atualizar_data_hora()

        # Frame central
        self.frame_central = tk.Frame(self.root, bg="#003366")
        self.frame_central.grid(row=1, column=0, sticky="nsew")

        # Carregar imagem
        try:
            imagem_pillow = Image.open(r"logo.png")
            imagem_pillow = imagem_pillow.resize((250, 250), Image.Resampling.LANCZOS)
            self.imagem = ImageTk.PhotoImage(imagem_pillow)
            tk.Label(self.frame_central, image=self.imagem, bg="#003366").pack(pady=0)
        except Exception as e:
            print(f"Erro ao carregar a imagem: {e}")

        # Texto "Faça Login!"
        tk.Label(self.frame_central, text="Faça Login!", font=("Arial", 18), bg="#003366", fg="white").pack(pady=10)

        # Campo de usuário
        self.entry_usuario = tk.Entry(self.frame_central, font=("Arial", 14), fg="grey", width=30)
        self.entry_usuario.insert(0, "Digite seu nome de usuário")
        self.entry_usuario.bind("<FocusIn>", lambda args: self.entry_usuario.delete('0', 'end')
                               if self.entry_usuario.get() == "Digite seu nome de usuário" else None)
        self.entry_usuario.bind("<FocusOut>", lambda args: self.entry_usuario.insert(0, "Digite seu nome de usuário")
                               if self.entry_usuario.get() == "" else None)
        self.entry_usuario.pack(pady=10)

        # Campo de senha
        self.entry_senha = tk.Entry(self.frame_central, font=("Arial", 14), fg="grey", width=30)
        self.entry_senha.insert(0, "Digite sua senha")
        self.entry_senha.bind("<FocusIn>", lambda args: self.entry_senha.delete('0', 'end')
                             if self.entry_senha.get() == "Digite sua senha" else None)
        self.entry_senha.bind("<FocusOut>", lambda args: self.entry_senha.insert(0, "Digite sua senha")
                             if self.entry_senha.get() == "" else None)
        self.entry_senha.bind("<Key>", lambda args: self.entry_senha.config(show="*")
                             if self.entry_senha.get() != "Digite sua senha" else None)
        self.entry_senha.pack(pady=10)

        # Botão de login
        tk.Button(self.root, text="Login", font=("Arial", 14), command=self.verificar_login, bg="#0052cc", fg="white")\
            .grid(row=2, column=0, sticky="sew", padx=10, pady=10)

        # Configuração do grid
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def atualizar_data_hora(self):
        agora = datetime.now()
        data_hora = agora.strftime("%d/%m/%Y %H:%M:%S")
        self.label_data_hora.config(text=data_hora)
        self.root.after(1000, self.atualizar_data_hora)

    def verificar_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        if (usuario == "adm" and senha == "007") or (usuario == "func" and senha == "funclars"):
            self.root.destroy()  # Fecha a janela de login
            from list_view import ListaFornecedoresApp  # Importa a classe ListaFornecedoresApp
            ListaFornecedoresApp(usuario)  # Abre a lista de fornecedores
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")