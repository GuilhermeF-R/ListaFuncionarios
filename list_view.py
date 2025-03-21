import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class ListaFornecedoresApp:
    def __init__(self, usuario):
        self.usuario = usuario
        self.root = tk.Tk()
        self.root.title("Lista de Fornecedores")
        self.root.state('zoomed')
        self.root.configure(bg="#003366")

        # Lista de fornecedores (simulando um banco de dados)
        self.fornecedores = []

        # Frame para data/hora e usuário
        frame_data_usuario = tk.Frame(self.root, bg="#003366")
        frame_data_usuario.pack(pady=10, fill="x")

        # Data e hora
        self.label_data_hora = tk.Label(frame_data_usuario, font=("Arial", 14), bg="#003366", fg="white")
        self.label_data_hora.pack(side="left", padx=10)

        # Usuário logado
        tk.Label(frame_data_usuario, text=f"Usuário: {usuario}", font=("Arial", 14), bg="#003366", fg="white")\
            .pack(side="left", padx=10)

        # Botões (ADM ou Funcionário)
        self.frame_botoes = tk.Frame(self.root, bg="#003366")
        self.frame_botoes.pack(pady=10, fill="x")

        if self.usuario == "adm":
            tk.Button(self.frame_botoes, text="Adicionar", font=("Arial", 12), command=self.abrir_janela_adicionar)\
                .pack(side="right", padx=5)
            tk.Button(self.frame_botoes, text="Editar", font=("Arial", 12), command=self.editar_fornecedor)\
                .pack(side="right", padx=5)
            tk.Button(self.frame_botoes, text="Deletar", font=("Arial", 12), command=self.deletar_fornecedor)\
                .pack(side="right", padx=5)
        tk.Button(self.frame_botoes, text="Imprimir", font=("Arial", 12), command=self.imprimir_lista)\
            .pack(side="right", padx=5)

        # Treeview para exibir a lista de fornecedores
        self.tree = ttk.Treeview(self.root, columns=("Nome", "Função", "Telefone"), show="headings")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Função", text="Função")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.pack(pady=10, padx=10, fill="both", expand=True)

        # Atualiza a data e hora
        self.atualizar_data_hora()

        self.root.mainloop()

    def atualizar_data_hora(self):
        agora = datetime.now()
        data_hora = agora.strftime("%d/%m/%Y %H:%M:%S")
        self.label_data_hora.config(text=data_hora)
        self.root.after(1000, self.atualizar_data_hora)

    def abrir_janela_adicionar(self):
        """Abre uma janela para adicionar um novo fornecedor."""
        janela_adicionar = tk.Toplevel(self.root)
        janela_adicionar.title("Adicionar Fornecedor")
        janela_adicionar.configure(bg="#003366")

        # Campos do formulário
        tk.Label(janela_adicionar, text="Nome:", font=("Arial", 12), bg="#003366", fg="white")\
            .grid(row=0, column=0, padx=10, pady=10)
        entry_nome = tk.Entry(janela_adicionar, font=("Arial", 12))
        entry_nome.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(janela_adicionar, text="Telefone:", font=("Arial", 12), bg="#003366", fg="white")\
            .grid(row=1, column=0, padx=10, pady=10)
        entry_telefone = tk.Entry(janela_adicionar, font=("Arial", 12))
        entry_telefone.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(janela_adicionar, text="Função:", font=("Arial", 12), bg="#003366", fg="white")\
            .grid(row=2, column=0, padx=10, pady=10)
        combo_funcao = ttk.Combobox(janela_adicionar, values=[
            "Pintor", "Pedreiro", "Ajudante", "Armador", "Eletricista", "Encanador",
            "Gesseiro", "Azulejista", "Vidraceiro", "Serralheiro", "Marceneiro",
            "Carpinteiro", "Arquiteto", "Engenheiro Civil"
        ], font=("Arial", 12))
        combo_funcao.grid(row=2, column=1, padx=10, pady=10)

        # Botão de adicionar
        tk.Button(janela_adicionar, text="Adicionar", font=("Arial", 12),
                  command=lambda: self.adicionar_fornecedor(entry_nome.get(), combo_funcao.get(), entry_telefone.get(), janela_adicionar))\
            .grid(row=3, column=0, columnspan=2, pady=10)

    def adicionar_fornecedor(self, nome, funcao, telefone, janela):
        """Adiciona um novo fornecedor à lista."""
        if nome and funcao and telefone:
            self.fornecedores.append((nome, funcao, telefone))
            self.atualizar_treeview()
            janela.destroy()
        else:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")

    def editar_fornecedor(self):
        """Edita um fornecedor selecionado."""
        selecionado = self.tree.selection()
        if selecionado:
            item = self.tree.item(selecionado)
            nome, funcao, telefone = item["values"]
            self.abrir_janela_adicionar()  # Reutiliza a janela de adicionar para editar
        else:
            messagebox.showwarning("Aviso", "Selecione um fornecedor para editar!")

    def deletar_fornecedor(self):
        """Deleta um fornecedor selecionado."""
        selecionado = self.tree.selection()
        if selecionado:
            self.tree.delete(selecionado)
        else:
            messagebox.showwarning("Aviso", "Selecione um fornecedor para deletar!")

    def imprimir_lista(self):
        """Simula a impressão da lista."""
        messagebox.showinfo("Imprimir", "Lista de fornecedores impressa com sucesso!")

    def atualizar_treeview(self):
        """Atualiza a Treeview com os fornecedores."""
        self.tree.delete(*self.tree.get_children())
        for fornecedor in self.fornecedores:
            self.tree.insert("", "end", values=fornecedor)