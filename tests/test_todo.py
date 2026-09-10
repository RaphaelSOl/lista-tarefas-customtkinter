import unittest
from unittest.mock import Mock

from lista_tarefas_customtkinter import TodoApp


class TestTodoApp(unittest.TestCase):

    def create_app(self):
        """
        Cria uma instância da classe sem abrir a janela gráfica.
        """
        app = TodoApp.__new__(TodoApp)
        app.tasks = []
        app.task_entry = Mock()

        # Impede que os testes tentem salvar arquivo ou atualizar a interface.
        app.save_tasks = Mock()
        app.refresh_tasks = Mock()

        return app

    def test_add_task(self):
        app = self.create_app()

        app.task_entry.get.return_value = "Estudar Docker"

        app.add_task()

        self.assertEqual(len(app.tasks), 1)
        self.assertEqual(app.tasks[0]["text"], "Estudar Docker")
        self.assertFalse(app.tasks[0]["done"])

    def test_toggle_task(self):
        app = self.create_app()

        app.tasks = [
            {
                "text": "Estudar Python",
                "done": False
            }
        ]

        app.toggle_task(0)

        self.assertTrue(app.tasks[0]["done"])

    def test_delete_task(self):
        app = self.create_app()

        app.tasks = [
            {
                "text": "Fazer atividade",
                "done": False
            }
        ]

        app.delete_task(0)

        self.assertEqual(len(app.tasks), 0)

    def test_clear_completed(self):
        app = self.create_app()

        app.tasks = [
            {
                "text": "Tarefa concluída",
                "done": True
            },
            {
                "text": "Tarefa pendente",
                "done": False
            }
        ]

        app.clear_completed()

        self.assertEqual(len(app.tasks), 1)
        self.assertEqual(app.tasks[0]["text"], "Tarefa pendente")
        self.assertFalse(app.tasks[0]["done"])


if __name__ == "__main__":
    unittest.main()