"""Importações."""
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk  # Para redimensionar a imagem

# Função para verificar o login
def verificar_login():
    """Verifica se o nome de usuário e a senha estão corretos."""
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    if (usuario == "adm" and senha == "007") or (usuario == "func" and senha == "funclars"):
        abrir_janela_principal(usuario)  # Passa o nome do usuário logado
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos!")

# Função para abrir a janela principal
def abrir_janela_principal(usuario):
    """Abre a janela principal após o login bem-sucedido."""
    janela_login.destroy()  # Fecha a janela de login

    # Cria a janela principal
    janela_principal = tk.Tk()
    janela_principal.title("Lista de Fornecedores")
    janela_principal.state('zoomed')  # Tela cheia
    janela_principal.configure(bg="#003366")  # Cor de fundo azul escuro

    # Exibe o texto "Lista de Fornecedores"
    label_lista = tk.Label(janela_principal, text="Lista de Fornecedores",
                           font=("Arial", 24), bg="#003366", fg="white")
    label_lista.pack(pady=50)

    # Frame para exibir a data, hora e o usuário logado
    frame_data_usuario = tk.Frame(janela_principal, bg="#003366")
    frame_data_usuario.pack(pady=10)

    # Exibe a data e hora
    label_data_hora = tk.Label(frame_data_usuario, font=("Arial", 14), bg="#003366", fg="white")
    label_data_hora.pack(side="left", padx=10)

    # Exibe o usuário logado
    label_usuario = tk.Label(frame_data_usuario, text=f"Usuário: {usuario}",
                             font=("Arial", 14), bg="#003366", fg="white")
    label_usuario.pack(side="left", padx=10)

    # Atualiza a data e hora na janela principal
    def atualizar_data_hora():
        agora = datetime.now()
        data_hora = agora.strftime("%d/%m/%Y %H:%M:%S")
        label_data_hora.config(text=data_hora)
        janela_principal.after(1000, atualizar_data_hora)  # Atualiza a cada 1 segundo

    atualizar_data_hora()

    janela_principal.mainloop()

# Cria a janela de login
janela_login = tk.Tk()
janela_login.title("Login")
janela_login.configure(bg="#003366")  # Cor de fundo azul escuro
janela_login.minsize(500, 500)  # Tamanho mínimo da janela

# Função para atualizar a data e hora na janela de login
def atualizar_data_hora_login():
    """Atualiza a data e hora exibidas na janela de login."""
    agora = datetime.now()
    data_hora = agora.strftime("%d/%m/%Y %H:%M:%S")
    label_data_hora_login.config(text=data_hora)
    janela_login.after(1000, atualizar_data_hora_login)  # Atualiza a cada 1 segundo

# Exibe a data e hora no canto superior esquerdo
label_data_hora_login = tk.Label(janela_login, font=("Arial", 14), bg="#003366", fg="white")
label_data_hora_login.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
atualizar_data_hora_login()

# Frame para centralizar os campos de entrada
frame_central = tk.Frame(janela_login, bg="#003366")
frame_central.grid(row=1, column=0, sticky="nsew")

# Carrega e redimensiona a imagem
try:
    # Abre a imagem usando Pillow
    imagem_pillow = Image.open(r"logo.png")
    # Redimensiona a imagem (ajuste o tamanho conforme necessário)
    imagem_pillow = imagem_pillow.resize((250, 250), Image.Resampling.LANCZOS)  # Tamanho 250x250
    # Converte a imagem para o formato do Tkinter
    imagem = ImageTk.PhotoImage(imagem_pillow)
    # Exibe a imagem
    label_imagem = tk.Label(frame_central, image=imagem, bg="#003366")
    label_imagem.pack(pady=0)
except Exception as e:
    print(f"Erro ao carregar a imagem: {e}")

# Texto "Faça Login!"
label_faca_login = tk.Label(frame_central, text="Faça Login!",
                            font=("Arial", 18), bg="#003366", fg="white")
label_faca_login.pack(pady=10)

# Campo de entrada para o nome de usuário com placeholder
entry_usuario = tk.Entry(frame_central, font=("Arial", 14), fg="grey", width=30)# Aumentei a largura
entry_usuario.insert(0, "Digite seu nome de usuário")
entry_usuario.bind("<FocusIn>", lambda args: entry_usuario.delete('0', 'end')
                   if entry_usuario.get() == "Digite seu nome de usuário" else None)
entry_usuario.bind("<FocusOut>", lambda args: entry_usuario.insert(0, "Digite seu nome de usuário")
                   if entry_usuario.get() == "" else None)
entry_usuario.pack(pady=10)

# Campo de entrada para a senha com placeholder
entry_senha = tk.Entry(frame_central, font=("Arial", 14), fg="grey", width=30)  # Aumentei a largura
entry_senha.insert(0, "Digite sua senha")
entry_senha.bind("<FocusIn>", lambda args: entry_senha.delete('0', 'end')
                 if entry_senha.get() == "Digite sua senha" else None)
entry_senha.bind("<FocusOut>", lambda args: entry_senha.insert(0, "Digite sua senha")
                 if entry_senha.get() == "" else None)
entry_senha.bind("<Key>", lambda args: entry_senha.config(show="*")# Oculta caracteres após digitar
                 if entry_senha.get() != "Digite sua senha" else None)
entry_senha.pack(pady=10)

# Botão de login fixado na parte inferior
botao_login = tk.Button(janela_login, text="Login",
                        font=("Arial", 14), command=verificar_login, bg="#0052cc", fg="white")
botao_login.grid(row=2, column=0, sticky="sew", padx=10, pady=10)

# Configuração do grid para manter a responsividade
janela_login.grid_rowconfigure(1, weight=1)
janela_login.grid_columnconfigure(0, weight=1)

janela_login.mainloop()
