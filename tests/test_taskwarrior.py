from dashboard import Task
import unittest, subprocess, json

class TestTaskWarrior(unittest.TestCase):

    def setUp(self):
        self.task = Task()

    def test_get_all_tasks(self):
        self.task.load_tasks()

    def test_get_pending_tasks(self):
        tasks = self.task.pending_tasks_list()
        for task in tasks:
            print(task)

    def test_active_tasks_list(self):
        tasks = self.task.active_tasks_list()
        for task in tasks:
            print(task)
