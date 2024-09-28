#!/usr/bin/env python
from lib.io import File
from lib.logging import LogSetup

config_file = File(path="~/.config/dashboard/config.ini")
logging_file = File(path="~/.config/dashboard/log.txt")

dashboard_logger = LogSetup(name='dashboard', file=logging_file).get_logger()

def main() -> None:
    dashboard_logger.info('Initializing the Dashboard.')
    print("Compiled")

if __name__ == "__main__":
    main()
