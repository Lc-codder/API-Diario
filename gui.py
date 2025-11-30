import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_URL = "http://127.0.0.1:8000"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Tarefas")
        self.root.geometry("750x500")

        self.tasks = []
        self.categories = []

        frame_top = tk.Frame(root)
        frame_top.pack(fill="x", pady=10)

        tk.Label(frame_top, text="Título da Tarefa:").grid(row=0, column=0, padx=5)
        self.entry_title = tk.Entry(frame_top, width=30)
        self.entry_title.grid(row=0, column=1, padx=5)

        tk.Label(frame_top, text="Descrição:").grid(row=1, column=0, padx=5)
        self.entry_desc = tk.Entry(frame_top, width=30)
        self.entry_desc.grid(row=1, column=1, padx=5)

        tk.Label(frame_top, text="Categoria:").grid(row=0, column=2, padx=5)
        self.combo_category = ttk.Combobox(frame_top, width=20, state="readonly")
        self.combo_category.grid(row=0, column=3, padx=5)

        tk.Button(frame_top, text="Adicionar Tarefa", command=self.add_task).grid(row=1, column=3, padx=5)

        frame_list = tk.Frame(root)
        frame_list.pack(fill="both", expand=True, pady=10)

        self.listbox = tk.Listbox(frame_list, font=("Arial", 12))
        self.listbox.pack(fill="both", expand=True)

        frame_bottom = tk.Frame(root)
        frame_bottom.pack(fill="x", pady=10)

        tk.Button(frame_bottom, text="Marcar como Concluída", command=self.mark_done).pack(side="left", padx=5)
        tk.Button(frame_bottom, text="Excluir Tarefa", command=self.delete_task).pack(side="left", padx=5)
        tk.Button(frame_bottom, text="Recarregar", command=self.refresh_all).pack(side="right", padx=5)

        self.refresh_categories()
        self.refresh_tasks()

    #  CATEGORIAS
    def refresh_categories(self):
        try:
            r = requests.get(f"{API_URL}/categories")
            self.categories = r.json()
        except:
            messagebox.showerror("Erro", "API não está rodando!")
            return

        # Atualiza o combobox
        self.combo_category["values"] = [c["name"] for c in self.categories]

    # TAREFAS
    def refresh_tasks(self):
        try:
            r = requests.get(f"{API_URL}/tasks")
            self.tasks = r.json()
        except:
            messagebox.showerror("Erro", "API não está rodando!")
            return

        self.listbox.delete(0, tk.END)

        for t in self.tasks:
            prefix = "✔️ Finalizada - " if t["done"] else "⏺ Em aberto - "
            cat_name = next((c["name"] for c in self.categories if c["id"] == t["category_id"]), "Sem categoria")
            self.listbox.insert(tk.END, f"{prefix}{t['title']} ({cat_name})")

    #  ADICIONAR
    def add_task(self):
        title = self.entry_title.get().strip()
        desc = self.entry_desc.get().strip()

        if not title:
            messagebox.showwarning("Aviso", "O título não pode estar vazio!")
            return

        category = self.combo_category.get()
        category_id = None

        if category:
            for c in self.categories:
                if c["name"] == category:
                    category_id = c["id"]

        try:
            requests.post(f"{API_URL}/tasks", json={
                "title": title,
                "description": desc,
                "category_id": category_id
            })
        except:
            messagebox.showerror("Erro", "API não está rodando!")
            return

        self.refresh_tasks()
        self.entry_title.delete(0, tk.END)
        self.entry_desc.delete(0, tk.END)


    # MARCAR CONCLUÍDA
    def mark_done(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Aviso", "Selecione uma tarefa.")
            return

        task = self.tasks[sel[0]]
        task_id = task["id"]

        try:
            requests.put(f"{API_URL}/tasks/{task_id}", json={
                "title": task["title"],
                "description": task["description"],
                "done": True,
                "category_id": task["category_id"]
            })
        except:
            messagebox.showerror("Erro", "API não está rodando!")
            return

        self.refresh_tasks()

    #  EXCLUIR TAREFA
    def delete_task(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showinfo("Aviso", "Selecione uma tarefa.")
            return

        task_id = self.tasks[sel[0]]["id"]

        try:
            requests.delete(f"{API_URL}/tasks/{task_id}")
        except:
            messagebox.showerror("Erro", "API não está rodando!")
            return

        self.refresh_tasks()

    #  RECARREGAR TUDO
    def refresh_all(self):
        self.refresh_categories()
        self.refresh_tasks()


#  EXECUÇÃO DO APP
if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()