import customtkinter as ctk
import json
from pathlib import Path


# =========================
# CONFIGURAÇÕES
# =========================
APP_TITLE = "Lista de Tarefas"
WINDOW_SIZE = "750x650"
DATA_FILE = Path("tarefas.json")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(APP_TITLE)
        self.geometry(WINDOW_SIZE)
        self.minsize(600, 500)

        self.tasks = []
        self.load_tasks()

        self.create_widgets()
        self.refresh_tasks()

    # =========================
    # INTERFACE
    # =========================
    def create_widgets(self):
        # Título
        self.title_label = ctk.CTkLabel(
            self,
            text="Minha Lista de Tarefas",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        self.title_label.pack(pady=(25, 10))

        # Área para adicionar tarefa
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(fill="x", padx=25, pady=10)

        self.task_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Digite uma nova tarefa...",
            height=40
        )
        self.task_entry.pack(side="left", fill="x", expand=True, padx=(12, 8), pady=12)

        self.add_button = ctk.CTkButton(
            input_frame,
            text="Adicionar",
            width=110,
            height=40,
            command=self.add_task
        )
        self.add_button.pack(side="right", padx=(0, 12), pady=12)

        self.task_entry.bind("<Return>", lambda event: self.add_task())

        # Contador
        self.counter_label = ctk.CTkLabel(
            self,
            text="0 tarefa(s) cadastrada(s)git add .",
            text_color="gray"
        )
        self.counter_label.pack(anchor="w", padx=30, pady=(5, 5))

        # Lista de tarefas
        self.tasks_frame = ctk.CTkScrollableFrame(
            self,
            label_text="Tarefas",
            label_font=ctk.CTkFont(size=16, weight="bold")
        )
        self.tasks_frame.pack(fill="both", expand=True, padx=25, pady=10)

        # Botão limpar concluídas
        self.clear_button = ctk.CTkButton(
            self,
            text="Limpar concluídas",
            width=160,
            command=self.clear_completed,
            fg_color="#555555",
            hover_color="#444444"
        )
        self.clear_button.pack(pady=(5, 20))

    # =========================
    # FUNCIONALIDADES
    # =========================
    def add_task(self):
        task_text = self.task_entry.get().strip()

        if not task_text:
            return

        self.tasks.append({
            "text": task_text,
            "done": False
        })

        self.task_entry.delete(0, "end")
        self.save_tasks()
        self.refresh_tasks()

    def toggle_task(self, index):
        self.tasks[index]["done"] = not self.tasks[index]["done"]
        self.save_tasks()
        self.refresh_tasks()

    def delete_task(self, index):
        del self.tasks[index]
        self.save_tasks()
        self.refresh_tasks()

    def clear_completed(self):
        self.tasks = [task for task in self.tasks if not task["done"]]
        self.save_tasks()
        self.refresh_tasks()

    # =========================
    # ATUALIZAÇÃO DA LISTA
    # =========================
    def refresh_tasks(self):
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        completed = 0

        if not self.tasks:
            empty_label = ctk.CTkLabel(
                self.tasks_frame,
                text="Nenhuma tarefa cadastrada.",
                text_color="gray"
            )
            empty_label.pack(pady=30)
        else:
            for index, task in enumerate(self.tasks):
                if task["done"]:
                    completed += 1

                self.create_task_row(index, task)

        total = len(self.tasks)
        pending = total - completed

        self.counter_label.configure(
            text=f"{total} tarefa(s) • {pending} pendente(s) • {completed} concluída(s)"
        )

    def create_task_row(self, index, task):
        row = ctk.CTkFrame(self.tasks_frame)
        row.pack(fill="x", pady=5, padx=5)

        checkbox = ctk.CTkCheckBox(
            row,
            text=task["text"],
            command=lambda i=index: self.toggle_task(i)
        )
        checkbox.pack(side="left", fill="x", expand=True, padx=12, pady=10)

        if task["done"]:
            checkbox.select()
            checkbox.configure(text_color="gray")

        delete_button = ctk.CTkButton(
            row,
            text="Excluir",
            width=80,
            command=lambda i=index: self.delete_task(i),
            fg_color="#A83232",
            hover_color="#7D2525"
        )
        delete_button.pack(side="right", padx=10, pady=8)

    # =========================
    # SALVAR / CARREGAR
    # =========================
    # Salva as tarefas para que elas permaneçam após fechar o aplicativo.
    def save_tasks(self):
        try:
            with DATA_FILE.open("w", encoding="utf-8") as file:
                json.dump(self.tasks, file, ensure_ascii=False, indent=2)
        except OSError as error:
            print(f"Erro ao salvar tarefas: {error}")

    def load_tasks(self):
        if not DATA_FILE.exists():
            self.tasks = []
            return

        try:
            with DATA_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, list):
                self.tasks = data
            else:
                self.tasks = []

        except (OSError, json.JSONDecodeError):
            self.tasks = []


if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
