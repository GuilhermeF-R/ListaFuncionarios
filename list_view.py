import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3

class ListaFornecedoresApp:
    def __init__(self, usuario):
        self.usuario = usuario
        self.root = tk.Tk()
        self.root.title("Lista de Fornecedores")
        self.root.state('zoomed')
        self.root.configure(bg="#003366")

        # Conectar ao banco de dados SQLite
        self.conn = sqlite3.connect('fornecedores.db')
        self.criar_tabela()

        # Lista de fornecedores (carregada do banco de dados)
        self.fornecedores = self.carregar_fornecedores()

        # Frame para data/hora e usuário
        frame_data_usuario = tk.Frame(self.root, bg="#003366")
        frame_data_usuario.pack(pady=10, fill="x")

        # Data e hora
        self.label_data_hora = tk.Label(frame_data_usuario, font=("Arial", 14), bg="#003366", fg="white")
        self.label_data_hora.pack(side="left", padx=10)

        # Usuário logado
        tk.Label(frame_data_usuario, text=f"Usuário: {usuario}", font=("Arial", 14), bg="#003366", fg="white")\
            .pack(side="left", padx=10)

        # Label de status (vermelho)
        self.label_status = tk.Label(self.root, text="", font=("Arial", 12), bg="#003366", fg="red")
        self.label_status.pack(pady=5)

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
        tk.Button(self.frame_botoes, text="Baixar Lista", font=("Arial", 12), command=self.baixar_lista_pdf)\
            .pack(side="right", padx=5)

        # Treeview para exibir a lista de fornecedores
        self.tree = ttk.Treeview(self.root, columns=("Nome", "Função", "Telefone"), show="headings")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Função", text="Função")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.pack(pady=10, padx=10, fill="both", expand=True)

        # Atualiza a data e hora
        self.atualizar_data_hora()

        # Carrega os fornecedores na Treeview
        self.atualizar_treeview()

        self.root.mainloop()

    def criar_tabela(self):
        """Cria a tabela de fornecedores se não existir."""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fornecedores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                funcao TEXT NOT NULL,
                telefone TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def carregar_fornecedores(self):
        """Carrega os fornecedores do banco de dados."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT nome, funcao, telefone FROM fornecedores")
        return cursor.fetchall()

    def adicionar_fornecedor(self, nome, funcao, telefone, janela):
        """Adiciona um novo fornecedor ao banco de dados."""
        if nome and funcao and telefone:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO fornecedores (nome, funcao, telefone) VALUES (?, ?, ?)", 
                           (nome, funcao, telefone))
            self.conn.commit()
            self.fornecedores = self.carregar_fornecedores()
            self.atualizar_treeview()
            self.label_status.config(text="Fornecedor adicionado com sucesso!")
            janela.destroy()
        else:
            self.label_status.config(text="Erro: Preencha todos os campos!")

    def editar_fornecedor(self):
        """Edita um fornecedor selecionado."""
        selecionado = self.tree.selection()
        if selecionado:
            item = self.tree.item(selecionado)
            nome, funcao, telefone = item["values"]
            self.abrir_janela_editar(nome, funcao, telefone)
        else:
            self.label_status.config(text="Erro: Selecione um fornecedor para editar!")

    def abrir_janela_editar(self, nome, funcao, telefone):
        """Abre uma janela para editar um fornecedor existente."""
        janela_editar = tk.Toplevel(self.root)
        janela_editar.title("Editar Fornecedor")
        janela_editar.configure(bg="#003366")

        # Campos do formulário pré-preenchidos
        tk.Label(janela_editar, text="Nome:", font=("Arial", 12), bg="#003366", fg="white")\
            .grid(row=0, column=0, padx=10, pady=10)
        entry_nome = tk.Entry(janela_editar, font=("Arial", 12))
        entry_nome.insert(0, nome)
        entry_nome.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(janela_editar, text="Telefone:", font=("Arial", 12), bg="#003366", fg="white")\
            .grid(row=1, column=0, padx=10, pady=10)
        entry_telefone = tk.Entry(janela_editar, font=("Arial", 12))
        entry_telefone.insert(0, telefone)
        entry_telefone.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(janela_editar, text="Função:", font=("Arial", 12), bg="#003366", fg="white")\
            .grid(row=2, column=0, padx=10, pady=10)
        combo_funcao = ttk.Combobox(janela_editar, values=[
            "Pintor", "Pedreiro", "Ajudante", "Armador", "Eletricista", "Encanador",
            "Gesseiro", "Azulejista", "Vidraceiro", "Serralheiro", "Marceneiro",
            "Carpinteiro", "Arquiteto", "Engenheiro Civil"
        ], font=("Arial", 12))
        combo_funcao.set(funcao)
        combo_funcao.grid(row=2, column=1, padx=10, pady=10)

        # Botão de salvar edição
        tk.Button(janela_editar, text="Salvar", font=("Arial", 12),
                  command=lambda: self.salvar_edicao(nome, entry_nome.get(), combo_funcao.get(), entry_telefone.get(), janela_editar))\
            .grid(row=3, column=0, columnspan=2, pady=10)

    def salvar_edicao(self, nome_antigo, nome_novo, funcao_novo, telefone_novo, janela):
        """Salva as alterações do fornecedor no banco de dados."""
        if nome_novo and funcao_novo and telefone_novo:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE fornecedores SET nome = ?, funcao = ?, telefone = ? WHERE nome = ?", 
                           (nome_novo, funcao_novo, telefone_novo, nome_antigo))
            self.conn.commit()
            self.fornecedores = self.carregar_fornecedores()
            self.atualizar_treeview()
            self.label_status.config(text="Fornecedor editado com sucesso!")
            janela.destroy()
        else:
            self.label_status.config(text="Erro: Preencha todos os campos!")

    def deletar_fornecedor(self):
        """Deleta um fornecedor selecionado após confirmação."""
        selecionado = self.tree.selection()
        if selecionado:
            item = self.tree.item(selecionado)
            nome, funcao, telefone = item["values"]

            # Pop-up de confirmação
            confirmacao = messagebox.askyesno(
                "Confirmar Exclusão",
                f"Você tem certeza que deseja deletar o fornecedor {nome}?\nEsta ação é irreversível!"
            )

            if confirmacao:  # Se o usuário confirmar
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM fornecedores WHERE nome = ? AND funcao = ? AND telefone = ?", 
                            (nome, funcao, telefone))
                self.conn.commit()
                self.fornecedores = self.carregar_fornecedores()
                self.atualizar_treeview()
                self.label_status.config(text="Fornecedor deletado com sucesso!")
        else:
            self.label_status.config(text="Erro: Selecione um fornecedor para deletar!")

    def imprimir_lista(self):
        """Simula a impressão da lista."""
        self.label_status.config(text="Lista de fornecedores impressa com sucesso!")

    def baixar_lista_pdf(self):
        """Gera um PDF com a lista de fornecedores."""
        if not self.fornecedores:
            self.label_status.config(text="Erro: A lista de fornecedores está vazia!")
            return

        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

        # Cria o arquivo PDF
        pdf_filename = "lista_fornecedores.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        c.setFont("Helvetica", 12)

        # Título do PDF
        c.drawString(100, 750, "Lista de Fornecedores")

        # Cabeçalho da tabela
        c.drawString(100, 730, "Nome")
        c.drawString(300, 730, "Função")
        c.drawString(450, 730, "Telefone")

        # Conteúdo da tabela
        y = 710
        for fornecedor in self.fornecedores:
            nome, funcao, telefone = fornecedor
            c.drawString(100, y, nome)
            c.drawString(300, y, funcao)
            c.drawString(450, y, telefone)
            y -= 20  # Espaçamento entre linhas

        # Finaliza o PDF
        c.save()
        self.label_status.config(text=f"Lista de fornecedores salva em {pdf_filename}")

    def atualizar_treeview(self):
        """Atualiza a Treeview com os fornecedores."""
        self.tree.delete(*self.tree.get_children())
        for fornecedor in self.fornecedores:
            self.tree.insert("", "end", values=fornecedor)

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
            