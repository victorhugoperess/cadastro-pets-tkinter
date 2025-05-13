import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Funções principais
def cadastrar_pet():
    nome = entry_nome.get()
    idade = entry_idade.get()
    raca = entry_raca.get()
    porte = combo_porte.get()
    status = combo_status.get()

    if nome == "":
        messagebox.showwarning("Atenção", "O nome do pet é obrigatório.")
        return

    conn = sqlite3.connect("pets.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pet (nome, idade, raca, porte, status) VALUES (?, ?, ?, ?, ?)",
                   (nome, idade, raca, porte, status))
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Pet cadastrado com sucesso!")
    limpar_campos()
    listar_pets()

def atualizar_pet():
    item = tree.selection()
    if not item:
        messagebox.showwarning("Seleção", "Selecione um pet na lista para atualizar.")
        return

    pet_id = tree.item(item[0])['values'][0]
    conn = sqlite3.connect("pets.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE pet SET nome = ?, idade = ?, raca = ?, porte = ?, status = ?
        WHERE id = ?
    """, (entry_nome.get(), entry_idade.get(), entry_raca.get(), combo_porte.get(), combo_status.get(), pet_id))
    conn.commit()
    conn.close()

    messagebox.showinfo("Atualizado", "Pet atualizado com sucesso!")
    limpar_campos()
    listar_pets()

def excluir_pet():
    item = tree.selection()
    if not item:
        messagebox.showwarning("Erro", "Selecione um pet na lista para excluir.")
        return

    pet_id = tree.item(item[0])['values'][0]
    if messagebox.askyesno("Confirmação", "Deseja realmente excluir este pet?"):
        conn = sqlite3.connect("pets.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pet WHERE id = ?", (pet_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Excluído", "Pet removido com sucesso!")
        limpar_campos()
        listar_pets()

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_idade.delete(0, tk.END)
    entry_raca.delete(0, tk.END)
    combo_porte.set("")
    combo_status.set("")

def listar_pets():
    for item in tree.get_children():
        tree.delete(item)
    conn = sqlite3.connect("pets.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pet")
    pets = cursor.fetchall()
    conn.close()
    for pet in pets:
        tree.insert("", "end", values=pet)

def buscar_pet():
    termo = entry_busca.get()
    for item in tree.get_children():
        tree.delete(item)

    conn = sqlite3.connect("pets.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pet WHERE nome LIKE ?", ('%' + termo + '%',))
    pets = cursor.fetchall()
    conn.close()
    for pet in pets:
        tree.insert("", "end", values=pet)

def selecionar_pet(event):
    item = tree.selection()
    if item:
        pet = tree.item(item[0])['values']
        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, pet[1])
        entry_idade.delete(0, tk.END)
        entry_idade.insert(0, pet[2])
        entry_raca.delete(0, tk.END)
        entry_raca.insert(0, pet[3])
        combo_porte.set(pet[4])
        combo_status.set(pet[5])

# Janela
janela = tk.Tk()
janela.title("Cadastro de Pets")
janela.configure(bg="#f0f4f7")
janela.geometry("720x600")

# Buscar
tk.Label(janela, text="Buscar por nome:", bg="#f0f4f7", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="e", padx=10, pady=5)
entry_busca = tk.Entry(janela, font=("Segoe UI", 10))
entry_busca.grid(row=0, column=1, padx=5)

btn_buscar = tk.Button(janela, text="Buscar", command=buscar_pet,
                       bg="#4caf50", fg="white", font=("Segoe UI", 10), width=12)
btn_buscar.grid(row=0, column=2, padx=5)

btn_ver_todos = tk.Button(janela, text="Ver Todos", command=listar_pets,
                          bg="gray", fg="white", font=("Segoe UI", 10), width=12)
btn_ver_todos.grid(row=0, column=3, padx=5)

# Título
titulo = tk.Label(janela, text="Cadastro de Pets", bg="#f0f4f7", fg="#2a3f5f", font=("Segoe UI", 14, "bold"))
titulo.grid(row=1, column=0, columnspan=4, pady=10)

# Formulário
def criar_label(texto, linha):
    tk.Label(janela, text=texto, bg="#f0f4f7", font=("Segoe UI", 10)).grid(row=linha, column=0, sticky="e", padx=10, pady=5)

criar_label("Nome:", 2)
entry_nome = tk.Entry(janela, font=("Segoe UI", 10))
entry_nome.grid(row=2, column=1, padx=10)

criar_label("Idade:", 3)
entry_idade = tk.Entry(janela, font=("Segoe UI", 10))
entry_idade.grid(row=3, column=1, padx=10)

criar_label("Raça:", 4)
entry_raca = tk.Entry(janela, font=("Segoe UI", 10))
entry_raca.grid(row=4, column=1, padx=10)

criar_label("Porte:", 5)
combo_porte = ttk.Combobox(janela, values=["Pequeno", "Médio", "Grande"], font=("Segoe UI", 10))
combo_porte.grid(row=5, column=1, padx=10)

criar_label("Status:", 6)
combo_status = ttk.Combobox(janela, values=["Disponível", "Adotado"], font=("Segoe UI", 10))
combo_status.grid(row=6, column=1, padx=10)

# Botões principais
btn_cadastrar = tk.Button(janela, text="Cadastrar Pet", command=cadastrar_pet,
                          bg="blue", fg="white", font=("Segoe UI", 10), width=18)
btn_cadastrar.grid(row=7, column=0, pady=10, padx=10)

btn_atualizar = tk.Button(janela, text="Atualizar Pet", command=atualizar_pet,
                          bg="blue", fg="white", font=("Segoe UI", 10), width=18)
btn_atualizar.grid(row=7, column=1, pady=10, padx=10)

btn_excluir = tk.Button(janela, text="Excluir Pet", command=excluir_pet,
                        bg="red", fg="white", font=("Segoe UI", 10), width=18)
btn_excluir.grid(row=7, column=2, columnspan=2, pady=10)

# Tabela
tree = ttk.Treeview(janela, columns=("ID", "Nome", "Idade", "Raça", "Porte", "Status"), show="headings")
for col in ("ID", "Nome", "Idade", "Raça", "Porte", "Status"):
    tree.heading(col, text=col)
    tree.column(col, width=100 if col == "ID" else 120)

tree.grid(row=8, column=0, columnspan=4, padx=10, pady=10)
tree.bind("<ButtonRelease-1>", selecionar_pet)

listar_pets()
janela.mainloop()
