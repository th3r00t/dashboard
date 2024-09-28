from pathlib import Path
import unittest
from src.lib.config import Config

class TestConfig(unittest.TestCase):
    def test_mkconfig(self):
        config = Config.file_path = Path(Path().cwd().name + "tests/config/dashboard.ini")
