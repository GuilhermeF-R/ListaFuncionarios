import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import sqlite3
import re  # Para validação de expressões regulares
import os
import subprocess  # Para abrir o PDF automaticamente

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

        # Título "LISTA DE FUNCIONÁRIOS"
        tk.Label(self.root, text="LISTA DE FUNCIONÁRIOS", font=("Arial", 24, "bold"), bg="#003366", fg="white")\
            .pack(pady=10)

        # Frame para a barra de pesquisa
        frame_pesquisa = tk.Frame(self.root, bg="#003366")
        frame_pesquisa.pack(pady=10, fill="x")

        # Campo de pesquisa
        self.entry_pesquisa = tk.Entry(frame_pesquisa, font=("Arial", 12), width=40)
        self.entry_pesquisa.pack(side="left", padx=10)

        # Botão de pesquisa com ícone "🔍"
        tk.Button(frame_pesquisa, text="🔍", font=("Arial", 12), command=self.pesquisar_fornecedor)\
            .pack(side="left")

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

        # Centralizar o conteúdo da lista
        for col in self.tree["columns"]:
            self.tree.column(col, anchor="center")

        # Atualiza a data e hora
        self.atualizar_data_hora()

        # Carrega os fornecedores na Treeview
        self.atualizar_treeview()

        self.root.mainloop()

    def formatar_telefone(self, event):
        """Formata o telefone automaticamente no formato (xx) xxxx-xxxx ou (xx) xxxxx-xxxx."""
        entry = event.widget
        texto = entry.get().replace("(", "").replace(")", "").replace(" ", "").replace("-", "")  # Remove formatação existente
        novo_texto = ""

        if len(texto) > 0:
            novo_texto += f"({texto[:2]}"  # Adiciona os dois primeiros dígitos entre parênteses
        if len(texto) > 2:
            novo_texto += f") {texto[2:6]}"  # Adiciona espaço e os próximos 4 dígitos
        if len(texto) > 6:
            novo_texto += f"-{texto[6:]}"  # Adiciona hífen e os dígitos restantes

        # Limita o número de caracteres
        if len(novo_texto) > 15:  # (xx) xxxxx-xxxx tem 15 caracteres
            novo_texto = novo_texto[:15]

        entry.delete(0, tk.END)
        entry.insert(0, novo_texto)

    def pesquisar_fornecedor(self):
        """Filtra a lista de fornecedores com base no termo de pesquisa."""
        termo = self.entry_pesquisa.get().lower()  # Converte o termo para minúsculas
        if termo:
            # Filtra os fornecedores que contêm o termo no nome, função ou telefone
            resultados = [
                fornecedor for fornecedor in self.fornecedores
                if termo in fornecedor[0].lower() or  # Nome
                   termo in fornecedor[1].lower() or  # Função
                   termo in fornecedor[2].lower()     # Telefone
            ]
            self.atualizar_treeview(resultados)
            self.label_status.config(text=f"{len(resultados)} resultado(s) encontrado(s).")
        else:
            # Se o campo de pesquisa estiver vazio, exibe todos os fornecedores
            self.atualizar_treeview(self.fornecedores)
            self.label_status.config(text="Digite um termo para pesquisar.")

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
            # Validação do nome e função (não podem conter números)
            if not self.validar_nome_funcao(nome):
                self.label_status.config(text="Erro: O nome não pode conter números!")
                return
            if not self.validar_nome_funcao(funcao):
                self.label_status.config(text="Erro: A função não pode conter números!")
                return

            # Validação do telefone (formato (xx) xxxx-xxxx ou (xx) xxxxx-xxxx)
            if not self.validar_telefone(telefone):
                self.label_status.config(text="Erro: Telefone deve estar no formato (xx) xxxx-xxxx ou (xx) xxxxx-xxxx!")
                return

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

    def validar_nome_funcao(self, texto):
        """Valida se o nome ou função não contém números."""
        return texto.replace(" ", "").isalpha() 

    def validar_telefone(self, telefone):
        """Valida se o telefone está no formato (xx) xxxx-xxxx ou (xx) xxxxx-xxxx."""
        return re.match(r"^\(\d{2}\) \d{4}-\d{4,5}$", telefone) is not None

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
        entry_telefone.bind("<KeyRelease>", self.formatar_telefone)  # Formata o telefone automaticamente

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
            # Validação do nome e função (não podem conter números)
            if not self.validar_nome_funcao(nome_novo):
                self.label_status.config(text="Erro: O nome não pode conter números!")
                return
            if not self.validar_nome_funcao(funcao_novo):
                self.label_status.config(text="Erro: A função não pode conter números!")
                return

            # Validação do telefone (formato (xx) xxxx-xxxx ou (xx) xxxxx-xxxx)
            if not self.validar_telefone(telefone_novo):
                self.label_status.config(text="Erro: Telefone deve estar no formato (xx) xxxx-xxxx ou (xx) xxxxx-xxxx!")
                return

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

        # Define o nome padrão do arquivo e o diretório do desktop
        desktop_path = os.path.expanduser("~/Desktop")  # Caminho para o desktop
        default_filename = os.path.join(desktop_path, "lista_de_fornecedores.pdf")

        # Solicita ao usuário o local e nome do arquivo (com o nome padrão pré-definido)
        pdf_filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Salvar Lista de Fornecedores",
            initialfile=default_filename,  # Nome padrão do arquivo
            initialdir=desktop_path  # Diretório inicial (desktop)
        )

        if not pdf_filename:  # Se o usuário cancelar
            self.label_status.config(text="Baixar PDF cancelado pelo usuário.")
            return

        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

        # Cria o arquivo PDF
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

        # Abre o PDF automaticamente
        subprocess.Popen([pdf_filename], shell=True)

        self.label_status.config(text=f"Lista de fornecedores salva em {pdf_filename}")

    def atualizar_treeview(self, fornecedores=None):
        """Atualiza a Treeview com os fornecedores."""
        self.tree.delete(*self.tree.get_children())
        fornecedores = fornecedores if fornecedores is not None else self.fornecedores
        for fornecedor in fornecedores:
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
        entry_telefone.bind("<KeyRelease>", self.formatar_telefone)  # Formata o telefone automaticamente

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
