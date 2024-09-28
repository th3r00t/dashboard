from pathlib import Path
import unittest
from src.lib.config import Config
from src.lib.logging import LogSetup
from src.lib.io import File

test_logger = LogSetup(File('test/test-log.txt'))

class TestConfig(unittest.TestCase):
    def test_mkconfig(self):
        config = Config(file_path="test/config/dashboard.ini")
        config.mkconfig()
