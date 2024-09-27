import subprocess, json
from typing import Any, List

class Task:
    """
    Main Task Interface

    Attributes:
        installed (bool): is task installed?
        command (str): command to be run on the host
        tasks (list): all available task objects unfiltered
        active_tasks (list): all active tasks?
    """
    def __init__(self):
        """
        """
        self.installed: bool = True if subprocess.run(['task'], stdout=subprocess.PIPE, text=True) else False
        self.command = "task"
        self.pending_tasks = self.load_tasks('pending') if self.installed else False
        self.active_tasks = self.load_tasks('active') if self.installed else False

    def load_tasks(self, filter = None) -> Any:
        """:return: Json"""
        if filter is None:
            result = subprocess.run([self.command, 'export'], stdout=subprocess.PIPE, text=True)
        else:
            result = subprocess.run([self.command, f"status:{filter}", 'export'], stdout=subprocess.PIPE, text=True)
        try:
            tasks = json.loads(result.stdout)
            filter = None
            return tasks
        except Exception:
            return {}

    def active_tasks_list(self) -> List:
        _active_tasks = []
        for task in self.active_tasks:
            _active_tasks.append(f"{task["id"]} {task["description"]}")
        return _active_tasks
    
    def pending_tasks_list(self):
        pending_tasks = []
        for task in self.pending_tasks:
            pending_tasks.append(f"{task["id"]} {task["description"]}")
        return pending_tasks
