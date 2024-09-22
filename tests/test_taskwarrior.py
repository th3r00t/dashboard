from dashboard import Task
import unittest, subprocess, json

class TestTaskWarrior(unittest.TestCase):

    def setUp(self):
        self.task = Task()

    def test_get_all_tasks(self):
        self.task.load_tasks()

    def test_active_tasks_list(self):
        for task in self.task.active_tasks_list():
            print(task)
